# Home Assistant 433 devices
Types of devices supported:
1. Light

## Install
`$ pip install dvdp.ha-433`

## Use
### 1 - Record
First you will have to record your 433 signal.

For help:  
`$ record_433 -h`

Minimal command:  
`$ sudo record_433 <your_device_name> <ON or OFF>`

If you want to specify your recording BCM Pin (default is 15):  
`$ sudo record_433 <your_device_name> <ON or OFF> -p <PIN_NR>`
 
Simply follow instructions. All recordings are saved to disk. Use `--help` flag
 for more info.

### 2 - Test transmission
If you used the default recordings directory it is quite simple.

First check what recordings are available by using `--help`:  
```
$ transmit_433 -h 
usage: Transmit signal from recordings.

Recordings available in /usr/local/lib/python3.7/site-packages/dvdp/recordings:
        device: test_device_2, actions: ['ON', 'OFF']
        device: test_device, actions: ['ON', 'OFF']

...
```

Then select the one you want to test from these recordings:  
`$ sudo transmit_433 <your_device_name> <ON or OFF>`  

e.g.:  
`$ sudo transmit_433 test_device_2 ON`

### 3 - Start MQTT Client for Home assistant
For this to work you will have to install:  
Mosquitto broker for Hass.io  
https://github.com/home-assistant/hassio-addons/tree/master/mosquitto

To have Home Assistant Hass.io control your devices:  
`$ ha_433 <BROKER IP>`

or if you require a password:  
`$ ha_433 <BROKER IP> -u <USERNAME> -p <PASSWORD>`

For more options please refer to `-h`
