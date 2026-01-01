---
source: "https://flipper.net/"
author:
published:
created: 2026-04-23
---
## What is Flipper Zero

### Your cyber buddy

Flipper Zero is a tiny piece of hardware with a curious personality of a cyber-dolphin. It can interact with digital systems in real life and grow while you use it. Explore any kind of access control system, RFID, radio protocols, and debug hardware using GPIO pins.

![](https://cdn.flipper.net/zero_landing_what-is_illustration_1.png) ![](https://cdn.flipper.net/zero_landing_what-is_illustration_2.png) ![](https://cdn.flipper.net/zero_landing_what-is_illustration_3.png)

The idea of Flipper Zero is to combine all the hardware tools you'd need for exploration and development on the go. Flipper was inspired by the pwnagotchi project, but unlike other DIY boards, Flipper is designed with the convenience of everyday usage in mind — it has a robust case, handy buttons, and shape, so there are no dirty PCBs or scratchy pins. Flipper turns your projects into a game, reminding you that development should always be fun.

![](https://cdn.flipper.net/zero_landing_what-is_inhand.png) ![](https://cdn.flipper.net/zero_landing_what-is_flipper.gif)

![Flipper Zero top view](https://cdn.flipper.net/zero-landing-features_1.png)

1.4" monochrome LCD display 128x64 px, ultra-low power sunlight-readable 5-button directional pad Back button Status LED

Flipper Zero is completely autonomous and can be controlled with a 5-button directional pad without additional devices, such as computers or smartphones. Main features are available from the Main Menu.

For more control, you can connect to Flipper Zero via USB and Bluetooth. Instead of a TFT, IPS or OLED, we decided to build in a cool old-school LCD.

![Flipper Zero side view](https://cdn.flipper.net/zero-landing-features_2.png)

USB Type-C Power & charging Firmware update MicroSD card slot Lanyard loop

![Flipper Zero bottom view](https://cdn.flipper.net/zero-landing-features_3.png)

GPIO pins 3.3V logic levels (5V tolerant for input) Infrared transceiver 1-Wire pogo pins

## Sub-1 GHz Transceiver

### Sub-1 GHz Range

This is the operating range for a wide class of wireless devices and access control systems, such as garage door remotes, boom barriers, IoT sensors and remote keyless systems. Users can expand their Flipper Zero capabilities by installing additional apps to read data from various devices including weather stations.  
  
Flipper has an integrated multi-band antenna, and a CC1101 chip, making it a powerful transceiver **with a range of up to 50 meters**.

![](https://cdn.flipper.net/zero_landing_subghz_barrier.jpg) ![](https://cdn.flipper.net/zero_landing_subghz_icon_1.png)

Smart sockets and bulbs

![](https://cdn.flipper.net/zero_landing_subghz_icon_2.png)

IoT sensors and doorbells

![](https://cdn.flipper.net/zero_landing_subghz_icon_3.png)

Garage doors and barriers

### Customizable radio platform

CC1101 is a universal transceiver designed for very low-power wireless applications. It supports various types of digital modulations such as 2-FSK, 4-FSK, GFSK and MSK, as well as OOK and flexible ASK shaping. You can perform any digital communication in your applications such as connecting to IoT devices and access control systems.

![](https://cdn.flipper.net/zero_landing_subghz_flipper.jpg)

## 125 kHz RFID

### Low-frequency proximity cards

This type of card is widely used in old access control systems around the world. It's pretty dumb, stores only an N-byte ID and has no authentication mechanism, allowing it to be read, cloned and emulated by anyone. A 125 kHz antenna is located on the bottom of Flipper Zero — it can read low-frequency proximity cards and save them to memory to emulate later.  
  
You can also emulate cards by entering their IDs manually.  
Moreover, Flipper Zero owners can share card IDs remotely with other Flipper Zero users.

![](https://cdn.flipper.net/zero_landing_rfid_writing.png) ![](https://cdn.flipper.net/zero_landing_rfid_emulating.jpg)

## NFC

### High-frequency proximity cards

Flipper Zero has a built-in NFC module (13.56 MHz). Along with the 125 kHz RFID module, it turns Flipper Zero into an ultimate RFID device operating in both low-frequency (LF) and high-frequency (HF) ranges. The NFC module supports all the major standards.  
  
It works pretty much the same as the 125 kHz module, allowing you to interact with NFC-enabled devices — read, write and emulate HF tags.

![](https://cdn.flipper.net/zero_landing_nfc_writing.png)

## Bluetooth

![](https://cdn.flipper.net/zero_landing_bluetooth_showcase.jpg)

Full Bluetooth Low Energy (BLE) support allows Flipper Zero to act as a peripheral device, allowing you to connect your Flipper Zero to 3rd-party devices and smartphones.  
  
Our mobile developers have designed apps for iOS and Android that let you update your Flipper Zero via BLE, remotely control the device, share keys, and manage data on a larger screen.

### Download Mobile Apps

 [![Download on the App Store](https://cdn.flipper.net/zero_landing_appstore_button.svg)](https://apps.apple.com/app/flipper-mobile-app/id1534655259)[![Get it on Google Play](https://cdn.flipper.net/zero_landing_googleplay_button.svg)](https://play.google.com/store/apps/details?id=com.flipperdevices.app)

## Infrared Transceiver

### Infrared Transmitter

The infrared transmitter can transmit signals to control electronics such as TVs, air conditioners (AC), stereo systems, and others.  
  
Flipper Zero has a built-in library of signals for common TVs, ACs, projectors, and stereo systems brands. This library is regularly updated with new signals, thanks to the Flipper Zero community's active contributions to the IR Remote database.

![](https://cdn.flipper.net/zero_landing_infrared_schematic.jpg)

### Infrared learning feature

Flipper Zero also has an IR receiver that can receive signals and save them to the library, so you can store any of your existing remotes to transmit commands later, and add them to the public IR Remote database to share with other Flipper Zero users.

![](https://cdn.flipper.net/zero_landing_infrared_learning.jpg)

## MicroSD card

### External storage for apps and data

There is a variety of data Flipper Zero has to store: remote codes, signal databases, dictionaries, image assets, logs, and more. All this data is stored on a MicroSD card.  
  
The MicroSD card slot has a push-push type connector, so the card is reliably secured inside without sticking out.  
Flipper Zero supports any FAT12, FAT16, FAT32 and exFAT formatted MicroSD cards to store your assets so you'll never have to worry the memory will run out.

## Tool for Hardware Exploration

Flipper Zero is a versatile tool for hardware exploration, firmware flashing, debugging, and fuzzing. It can be connected to any piece of hardware using GPIO to control it with buttons, run your own code and print debug messages to the LCD. It can also be used as a regular USB adapter for UART, SPI, I2C, etc.

**Completely Autonomous**  
Flipper Zero features built-in 5V and 3.3V power pins. Control the device with built-in buttons and display — no PC is needed.

**SPI, UART, I2C to USB converter**  
Communicate with any hardware from your desktop application.

**Flashing and debugging tools**

- SPI Flash Programmer
- AVR ISP Programmer
- OpenDAP

**Fuzzing tool**  
Test any protocols and signals.

![](https://cdn.flipper.net/zero_landing_tool-for_oscilloscope.jpg)

## iButton

### 1-Wire keys (Touch Memory)

Flipper Zero has a built-in 1-Wire connector to read iButton contact keys. This old technology is still widely used around the world. It uses the 1-Wire protocol that doesn't have any authentication. Flipper can easily read these keys, store IDs in the memory, write IDs to blank keys and emulate the key itself.  
  
Flipper Zero has a unique iButton contact pad design — its shape works both as a reader and a probe to connect to iButton sockets.

![](https://cdn.flipper.net/zero_landing_ibutton_emulating.jpg) ![](https://cdn.flipper.net/zero_landing_ibutton_pins.png) ![](https://cdn.flipper.net/zero_landing_whats-inside.jpg)