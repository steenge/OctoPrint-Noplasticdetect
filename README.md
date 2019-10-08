# OctoPrint-Noplasticdetect

Extremely simple plugin that pause the printer if a DIY filament sensor detects that the roll of filament runs out.  

The sensor contain no active electroics and is based on a microswitch.
The default behaviour is, that NO_FILAMENT is detected, if the switch closes.
The sensor must be connected between a GPIO pin and GND, such that the pin is pulled LOW if no filament is present inside the sensor.

The 3d file of the sensor I have designed for this plugin can be downloaded from thingverse.com/XYZ


## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/steenge/OctoPrint-Noplasticdetect/archive/master.zip


## Configuration

**TODO:** Describe your plugin's configuration options (if any).

To be added, but most likely:

Switch-style:
- Closed=Filament out
- Open = Filament out