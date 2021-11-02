import cherrypy
import datetime
import jinja2, os
import sqlite3 as sql


ROOTDIR = os.path.dirname(os.path.abspath(__file__)) 
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(ROOTDIR,'templates')),extensions=['jinja2.ext.autoescape'])

config = {
    'global' : {
        'server.socket_host' : '0.0.0.0',
        'server.socket_port' : 3000
    },
    '/': {
        'tools.staticdir.root': os.path.join(ROOTDIR,'static')
    },
    '/css': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'css'
    },
    '/img': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'images'
    }
}

DB = 'locations-with-tid.db'   

class Website:
    @cherrypy.expose
    def index(self):
        template = JINJA_ENVIRONMENT.get_template('reproduce-3.html')
        template_values = {
			'locations': self.get_locations(),'longitudes': self.get_longitudes(),'latitudes': self.get_latitudes()} #we need to pass longitudes and latitudes as separate dictionaries for OpenLayers to work, so this is added. 
        return template.render(template_values) #make and serve the webpage
            
    def get_locations(self):
        locations = []
        tids = self.get_tids()
        latitudes = self.get_latitudes()
        longitudes = self.get_longitudes()
        dates = self.get_dates()
        times = self.get_times()
        for i in range(len(latitudes)):
            locations.append([tids[i],latitudes[i],longitudes[i],dates[i],times[i]])  #make list of lists to enable jinja render as columns 
        print(locations)
        return locations
    
    def get_tids(self):
        tids = []
        with sql.connect(DB) as cur:
            results = cur.execute('''SELECT tid FROM Location;''')
            for tid, in results:
                tids.append(str(tid))
        return tids
   
    def get_latitudes(self):
        latitudes = []
        with sql.connect(DB) as cur:
            results = cur.execute('''SELECT latitude FROM Location;''')
            for latitude, in results:
                latitudes.append(str(latitude))
        return latitudes

    def get_longitudes(self):
        longitudes = []
        with sql.connect(DB) as cur:
            results = cur.execute('''SELECT longitude FROM Location;''')
            for longitude, in results:
                longitudes.append(str(longitude))
        return longitudes
    
    def get_dates(self):
        dates = []
        with sql.connect(DB) as cur:
            results = cur.execute('''SELECT date FROM Location;''')
            for date, in results:
                dates.append(str(date))
        return dates
    
    def get_times(self):
        times = []
        with sql.connect(DB) as cur:
            results = cur.execute('''SELECT time FROM Location;''')
            for time, in results:
                times.append(str(time))
        return times


    #return template.render(template_values)

if __name__ == '__main__':
    cherrypy.quickstart(Website(), '/', config)