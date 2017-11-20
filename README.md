# B-L475E-IOT01A MicroPython Toolbox
This is a MicroPython Library to easily access the functionality of the STM32L4 Discovery kit IoT node, model B-L475E-IOT01A

## Board Information
[B-L475E-IOT01A](http://www.st.com/en/evaluation-tools/b-l475e-iot01a.html)

## MicroPython Info
[Main Website](https://micropython.org/)

# MicroPython Installation Instructions
Modified from the following [tutorial](https://forum.micropython.org/viewtopic.php?t=2613)

## OSX
1. git clone https://github.com/micropython/micropython.git
2. Download and unzip the [ARM toolchain](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads) somewhere.
3. go to <micropython_dir>/ports/stm32
4. make BOARD=B_L475E_IOT01A CROSS_COMPILE=/Path/where/you/uncompressed/the/toolchain/.../bin/arm-none-eabi-

That will compile the HEX files needed to flash the board.  The next step however involves a Windows PC.  This is because I had the hardest time getting my Mac to flash the STM32 over stlink or any other system, and all of STM's tools are primarily windows based.

5. Transfer the HEX file to a Windows PC
6. Install [ST-Link Utility](http://www.st.com/en/development-tools/stsw-link004.html)
7. Run ST-Link Utility and Open the HEX file.
8. Connect your B-L475E-IOT01A board to the PC
9. Select TARGET > CONNECT from the ST-Link Utility menu.
10. Once connected select TARGET > PROGRAM...
11. Wait until complete, then eject the Board.
12. Connect the Board to your Mac.
13. ls /dev and look for something like tty.usbmodem1413 (it may have a different number, if so PLEASE use that number)
14. screen /dev/tty.usbmodem1413 115200
15. Press Enter a few times and you should see the Python REPL!

If you need to access the Flash File System, just plug in a second USB cable into the OTG port on the B-L475E-IOT01A board.  You should then see a PYBFLASH drive appear on your system.

# PROPER CARE AND FEEDING
I have accidentially corrupted the Flash filesystem of the board more than once.  To avoid this, make sure you EJECT the PYBFLASH drive before RESETTING the board or UNPLUGGING it.

Also I have had a few instances of the REPL locking up on me.  In these cases I believe I just unplugged and re-pluggin in the board.

# Feature List (and if implemented)
- [ ] Bluetooth® V4.1 module (SPBTLE-RF)
- [ ] Sub-GHz (868 or 915 MHz) low-power-programmable RF module (SPSGRF-868 or SPSGRF-915)
- [ ] Wi-Fi® module Inventek ISM43362-M3G-L44 (802.11 b/g/n compliant)
- [ ] Dynamic NFC tag based on M24SR with its printed NFC antenna
- [ ] 2 digital omnidirectional microphones (MP34DT01)
- [ ] Capacitive digital sensor for relative humidity and temperature (HTS221)
- [ ] High-performance 3-axis magnetometer (LIS3MDL)
- [x] 3D accelerometer and 3D gyroscope (LSM6DSL)
	- [x] 3D Accelerometer (Complete)
	- [x] 3D Gyroscope (Complete)
	- [x] Temperature (Complete)
	- [ ] Pedometer
	- [ ] Significant motion / Inactivity / Tilt
	- [ ] FIFO
	- [ ] Single / Double Tap
	- [ ] Timer
- [ ] 260-1260 hPa absolute digital output barometer (LPS22HB)
- [ ] Time-of-Flight and gesture-detection sensor (VL53L0X)
- [ ] 2 push-buttons (user and reset)
- [ ] Expansion connectors:
	- [ ] Arduino™ Uno V3
	- [ ] PMOD
 
