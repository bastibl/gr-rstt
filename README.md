# RSTT - RadioSonde Telemetry Tool

Recieve and decode telemetry from Vaisala meteorological radiosondes (namely
RS92-SGP/RS92-SGPD).

Further Information
http://brmlab.cz/project/weathersonde/start

See individual files for license, where no explicit license is specified see
LILCENSE.txt for details.

It is based on Gnuradio building blocks with some custom code. Use Python and
C++ as main languagues. Result is tested only on Linux, but add tweaks for other
platforms shoud be easy, feel free to send patches.

## Development

Like GNU Radio, this module uses *master* and *maint* branches for development.
These branches are supposed to be used with the corresponding GNU Radio
branches. This means: the *maint-3.7* branch is compatible with GNU Radio 3.7,
*maint-3.8* is compatible with GNU Radio 3.8, and *master* is compatible with
GNU Radio master, which tracks the development towards GNU Radio 3.9.

## Dependencies
- GNU Radio. See the [GNU Radio
  Wiki](http://gnuradio.org/redmine/projects/gnuradio/wiki/InstallingGR) for
  installation instructions.


## Installation
```
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig
```

## Usage

Start flow graphs in the *apps* folder.


## Demos

Quick example:
https://www.youtube.com/watch?v=B_IbqoJjNLw

[![gr-rstt demo](http://img.youtube.com/vi/B_IbqoJjNLw/0.jpg)](http://www.youtube.com/watch?v=B_IbqoJjNLw "gr-rstt demo")
