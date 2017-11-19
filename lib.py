import machine
import struct
import utime

I2C_2 = machine.I2C(2)

LSM6DSL_ADDR = 106

LSM6DSL_REG_CTRL1_XL = 0x10
LSM6DSL_REG_CTRL2_G = 0x11

LSM6DSL_REG_OUT_TEMP_H = 0x21
LSM6DSL_REG_OUT_TEMP_L = 0x20

LSM6DSL_REG_OUTX_L_G = 0x22
LSM6DSL_REG_OUTX_H_G = 0x23
LSM6DSL_REG_OUTY_L_G = 0x24
LSM6DSL_REG_OUTY_H_G = 0x25
LSM6DSL_REG_OUTZ_L_G = 0x26
LSM6DSL_REG_OUTZ_H_G = 0x27

LSM6DSL_REG_OUTX_L_XL = 0x28
LSM6DSL_REG_OUTX_H_XL = 0x29
LSM6DSL_REG_OUTY_L_XL = 0x2A
LSM6DSL_REG_OUTY_H_XL = 0x2B
LSM6DSL_REG_OUTZ_L_XL = 0x2C
LSM6DSL_REG_OUTZ_H_XL = 0x2D

HIGH_PERF_416HZ = b'\x60'
HIGH_PERF_6KHZ = b'\xA0'

XL_SCALE_2G = 0.061

XL_NEG_OFFSET = 3.997739

G_SCALE_245 = 0.00875043752188

G_NEG_OFFSET = 573.46867343388304


def init():
	I2C_2.writeto_mem(LSM6DSL_ADDR, LSM6DSL_REG_CTRL1_XL, HIGH_PERF_6KHZ)
	I2C_2.writeto_mem(LSM6DSL_ADDR, LSM6DSL_REG_CTRL2_G, HIGH_PERF_6KHZ)


def _read_hl_registers(addr, reg_h, reg_l):
	hb = I2C_2.readfrom_mem(LSM6DSL_ADDR, reg_h, 1)
	lb = I2C_2.readfrom_mem(LSM6DSL_ADDR, reg_l, 1)
	byte_value = struct.unpack('>H', hb+lb)[0]
	# value = byte_value / 16.0  #wat?
	return byte_value, hb[0], lb[0]

def get_temp():
	temp, hb, _ = _read_hl_registers(LSM6DSL_ADDR, LSM6DSL_REG_OUT_TEMP_H, LSM6DSL_REG_OUT_TEMP_L)
	temp = temp / 16.0
	if hb & 0x80:
		temp -= 256.0
	return temp

def get_accel():
	x_byte_val, x_hb, x_lb = _read_hl_registers(LSM6DSL_ADDR, LSM6DSL_REG_OUTX_H_XL, LSM6DSL_REG_OUTX_L_XL)
	y_byte_val, y_hb, y_lb = _read_hl_registers(LSM6DSL_ADDR, LSM6DSL_REG_OUTY_H_XL, LSM6DSL_REG_OUTY_L_XL)
	z_byte_val, z_hb, z_lb = _read_hl_registers(LSM6DSL_ADDR, LSM6DSL_REG_OUTZ_H_XL, LSM6DSL_REG_OUTZ_L_XL)
	
	x_val = (x_byte_val * XL_SCALE_2G) / 1000.0 #from milligraviy to gravity (mg -> g)
	y_val = (y_byte_val * XL_SCALE_2G) / 1000.0
	z_val = (z_byte_val * XL_SCALE_2G) / 1000.0

	if x_hb & 0x80:
		x_val -= XL_NEG_OFFSET

	if y_hb & 0x80:
		y_val -= XL_NEG_OFFSET

	if z_hb & 0x80:
		z_val -= XL_NEG_OFFSET

	return x_val, y_val, z_val

def get_gyro():
	x_byte_val, x_hb, x_lb = _read_hl_registers(LSM6DSL_ADDR, LSM6DSL_REG_OUTX_H_G, LSM6DSL_REG_OUTX_L_G)
	y_byte_val, y_hb, y_lb = _read_hl_registers(LSM6DSL_ADDR, LSM6DSL_REG_OUTY_H_G, LSM6DSL_REG_OUTY_L_G)
	z_byte_val, z_hb, z_lb = _read_hl_registers(LSM6DSL_ADDR, LSM6DSL_REG_OUTZ_H_G, LSM6DSL_REG_OUTZ_L_G)

	x_val = (x_byte_val * G_SCALE_245) # measured in degrees per second
	y_val = (y_byte_val * G_SCALE_245)
	z_val = (z_byte_val * G_SCALE_245)

	if x_hb & 0x80:
		x_val -= G_NEG_OFFSET

	if y_hb & 0x80:
		y_val -= G_NEG_OFFSET

	if z_hb & 0x80:
		z_val -= G_NEG_OFFSET

	return x_val, y_val, z_val


def test_LSM6DSL_sensor(duration_sec, sec_resolution, csv_out=False):
	if duration_sec < sec_resolution:
		raise ValueError("Duration cannot be smaller than the Resolution")
	if sec_resolution > 1:
		raise ValueError("sec_resolution cannot be > 1")
	if csv_out:
		data = []
	start_ms = utime.ticks_ms()
	for i in range(duration_sec* (1/sec_resolution)):
		temp = get_temp()
		accel = get_accel()
		gyro = get_gyro()
		print("Temp:\t%08f Degrees Celsius" % temp)
		print("Accel\tX: %08fg\tY:%08fg\tZ:%08fg" % accel)
		print("Gyro\tX: %08fdps\tY:%08fdps\tZ:%08fdps" % gyro)
		if csv_out:
			row = [
				utime.ticks_diff(utime.ticks_ms(), start_ms),
				temp, 
				accel[0],
				accel[1],
				accel[2],
				gyro[0],
				gyro[1],
				gyro[2]
				]
			data.append(row)
		utime.sleep(sec_resolution)
	if csv_out:
		with open('LSM6DSL.csv', 'w') as f:
			for row in data:
				f.write(",".join([str(column) for column in row]) + "\n")
