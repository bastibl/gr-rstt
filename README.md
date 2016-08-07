# RSTT - RadioSonde Telemetry Tool

Recieve and decode telemetry from Vaisala meteorological radiosondes
(namely RS92-SGP/RS92-SGPD).

Further Information
http://brmlab.cz/project/weathersonde/start

See individual files for license, where no explicit license is specified
see LILCENSE.txt for details.

It is based on Gnuradio building blocks with some custom code.
Use Python and C++ as main languagues. Result is tested only on Linux,
but add tweaks for other platforms shoud be easy, feel free to send patches.


## Dependencies
- GNU Radio v3.7.X or the v3.8 development branch (*next*). <br> See the [GNU Radio Wiki](http://gnuradio.org/redmine/projects/gnuradio/wiki/InstallingGR) for installation instructions.

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
https://www.youtube.com/watch?v=hnv0efcShfo
