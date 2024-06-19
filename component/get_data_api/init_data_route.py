from .route.request import *
from .map.request import *

# Function to read a JSON file and return its content
class init_data_route():
    def __init__(self, routeId, direction):
        self.routeId = routeId
        self.direction = direction
        self.get_data_route()
        self.get_info_general_route()
        self.get_coords_route()
        self.get_data_stops()
        self.get_stops_of_route()
        
    
    def get_data_route(self):
        res, code = get_data_route_by_id(self.direction, self.routeId)
        if code:
            self.data_route = res['result']
        else:
            print('error:', res)
            
    def get_info_general_route(self):
        info, code = get_info_route(self.routeId)
        if code:
            self.name_route = info['result']['long_name']
            self.ticket_price = info['result']['ticket']
            self.time = info['result']['time']
        else:
            print("error:", info)

    def get_coords_route(self):
        path_route = self.data_route[0]['path']
        self.coords = []
        for addr in path_route:
            self.coords.append([addr['lat'], addr['lon']])
    
    def get_data_stops(self):
        res, code = get_data_stops()
        if code:
            stopsInfo = res['result']
        else:
            print('error:', res)
            return
        
        self.data_stops = {}
        for i in range(len(stopsInfo)):
            info_stop = [stopsInfo[i]['name'], stopsInfo[i]['lat'], stopsInfo[i]['lon']]
            self.data_stops[stopsInfo[i]['id']] = info_stop

    def get_stops_of_route(self):
        stopID_of_route = self.data_route[0]['stopIDs']

        self.stops_route = {}
        for i in range(len(stopID_of_route)):
            stop_id = stopID_of_route[i]
            if stop_id in self.data_stops:
                info = self.data_stops[stop_id]
                self.stops_route[info[0]] = [info[1], info[2]]
    
        
def get_all_routesId():
    res, code = get_all_ids()
    if code:
        return res['result']
    else:
        return None

def get_info_general_routes():
    res, code = get_info_all_routes()
    if code:
        return res['result'] 
    else:
        return None 

if __name__ == '__main__':
    data_route = init_data_route(1062, 0)
    print(data_route.stops_route)
    
    #print(data_route.data_stops)


