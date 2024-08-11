## libsoundpeats

This is a BLE program to control my soundpeats capsule3 pro. Like get Battery, change modes between normal, anc and passthrough because i'm too lazy to raise my hand to my ears I'd rather do it from my keyboard.

### Supported devices

- [X] capsule3 pro

### Commands

- connect

```bash
dbus-send --session --dest=tn.aziz.soundpeats.BLEService --print-reply /tn/aziz/soundpeats/BLEService tn.aziz.soundpeats.BLEService.Connect
```

- get battery level

```bash
dbus-send --session --dest=tn.aziz.soundpeats.BLEService --print-reply /tn/aziz/soundpeats/BLEService tn.aziz.soundpeats.BLEService.GetBatteryLevel
```