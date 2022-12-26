#!/usr/bin/python

import os
import rrdtool
import tempfile
import web

# web.py app URL routing setup
URLS = ('/graph.png', 'Graph',
        '/view', 'Page')

RRD_FILE = '/home/pi/rpi_home_sensors/templog.rrd'
SCALES = ('day', 'week', 'month', 'quarter', 'half', 'year')
RESOLUTIONS = {'day': '-26hours', 'week':'-8d', 'month':'-35d', 'quarter':'-90d',
  'half':'-6months', 'year':'-1y'}

class Page:
    def GET(self):
        scale = web.input(scale='day').scale.lower()
        if scale not in SCALES:
            scale = SCALES[0]
        result = '<html><head><title>Temp Logger</title></head><h4>'
        for tag in SCALES:
            if tag == scale:
                result += '| %s |' % (tag,)
            else:
                result += '| <a href="./view?scale=%s">%s</a> |' % (tag, tag)
        result += '</h4>'
        result += '<img src="./graph.png?scale=%s">' % (scale, )
        result += '</html>'
        web.header('Content-Type', 'text/html')
        return result
 
class Graph:
  def GET(self):
      scale = web.input(scale='day').scale.lower()
      if scale not in SCALES:
          scale = SCALES[0]
      fd,path = tempfile.mkstemp('.png')
      rrdtool.graph(path,
                    '-w 900',  '-h',  '400', '-a', 'PNG',
                    '--slope-mode',
                    '--start',  ',%s' % (RESOLUTIONS[scale], ),
                    '--end', 'now',
                    '--vertical-label',  'temperature (C)',
                    'DEF:in=%s:temp:AVERAGE' % (RRD_FILE, ),
                    'DEF:out=%s:humid:AVERAGE' % (RRD_FILE, ),
                    'LINE2:in#00ff00:temp ',
                    'GPRINT:in:LAST:Cur\:%8.2lf',
                    'GPRINT:in:AVERAGE:Avg\: %8.2lf',
                    'GPRINT:in:MAX:Max\:%8.2lf',
                    r'GPRINT:in:MIN:Min\:%8.2lf\j',
                    'LINE2:out#0000ff:humid',
                    'GPRINT:out:LAST:Cur\:%8.2lf',
                    'GPRINT:out:AVERAGE:Avg\:%8.2lf',
                    'GPRINT:out:MAX:Max\:%8.2lf',
                    r'GPRINT:out:MIN:Min\:%8.2lf\j')
      with open(path, 'rb') as f: # open the file in read binary mode
          data = f.read() # read the bytes from the file to a variable
      os.unlink(path)
      web.header('Content-Type', 'image/png')
      return data
      

if __name__ == "__main__":
    web.application(URLS, globals()).run()
