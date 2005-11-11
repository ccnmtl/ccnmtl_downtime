#!/usr/bin/env python
import cherrypy
import os.path

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-p","--port",dest="port", help="specify the port", default="80", metavar="PORT")
parser.add_option("-s","--system",dest="system", help="system name", default="this system", metavar="SYSTEM")
parser.add_option("-t","--time",dest="time", help="what time the system is expected to be back up", default="", metavar="TIME")
(options,args) = parser.parse_args()

image_path = os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(__file__),"images")))
index_path = os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(__file__),"downtime_template.html")))

cherrypy.config.update({'global' : {'server.socketPort' : int(options.port)},
                        '/images' : {'staticFilter.on' : True,
                                     'staticFilter.dir' : image_path}})

class DownTimeApp:
    def index(self):
        output = open(index_path,"r").read()
        output = output.replace("[this system]",options.system)
        output = output.replace("[date or time here]",options.time)
        return output
    index.exposed = True

    def default(self,*args,**kwargs):
        raise cherrypy.HTTPRedirect("/")
    default.exposed = True

if __name__ == "__main__":
    cherrypy.root = DownTimeApp()
    cherrypy.server.start()
