## libsoundpeats

This is a BLE program to control my soundpeats capsule3 pro. Like get Battery, change modes between normal, anc and passthrough because i'm too lazy to raise my hand to my ears I'd rather do it from my keyboard.

### Supported devices

I only own a capsule3 pro, should support some QCY models, they have similar firmware.

### Commands

Run the server. Set it to run as a systemd service or whatever.

#### connect

```bash
dbus-send --session --dest=tn.aziz.soundpeats.BLEService --print-reply /tn/aziz/soundpeats/BLEService tn.aziz.soundpeats.BLEService.Connect
```

#### get battery level

```bash
dbus-send --session --dest=tn.aziz.soundpeats.BLEService --print-reply /tn/aziz/soundpeats/BLEService tn.aziz.soundpeats.BLEService.GetBatteryLevel
```

#### get earbud settings

```bash
dbus-send --session --dest=tn.aziz.soundpeats.BLEService --print-reply /tn/aziz/soundpeats/BLEService tn.aziz.soundpeats.BLEService.GetEarbudSettings
```

#### set noise mode

For my setup I set this to a keyboard shortcut in KDE to change between modes.

```bash
# ANC mode
dbus-send --session --dest=tn.aziz.soundpeats.BLEService --print-reply /tn/aziz/soundpeats/BLEService tn.aziz.soundpeats.BLEService.SetNoiseMode string:"ANC"
# normal mode
dbus-send --session --dest=tn.aziz.soundpeats.BLEService --print-reply /tn/aziz/soundpeats/BLEService tn.aziz.soundpeats.BLEService.SetNoiseMode string:"NORMAL"
# passthrough mode
dbus-send --session --dest=tn.aziz.soundpeats.BLEService --print-reply /tn/aziz/soundpeats/BLEService tn.aziz.soundpeats.BLEService.SetNoiseMode string:"PASSTHROUGH"
```
