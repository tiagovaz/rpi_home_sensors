#!/bin/bash

rrdtool graph temp_graph.png -w 1024 -h 400 -a PNG --slope-mode --start -3d --end now --vertical-label "temperature (°C)" DEF:in=templog.rrd:temp:AVERAGE DEF:out=templog.rrd:humid:AVERAGE LINE2:in#00ff00:"temp" LINE2:out#0000ff:"humid"
