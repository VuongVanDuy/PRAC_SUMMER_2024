import json
import os
import requests

# Function to read a JSON file and return its content
class init_data_route():
    def __init__(self, routeId, direction):
        self.routeId = routeId
        self.direction = direction
        self.name_route = self.get_name_route()
        self.ticket_price = '60 рублей (к. Виза) - 45 рублей (к. Мир)'
        self.time = '6:00 - 24:00'
        self.file_stops = './data/stops.json'
        self.file_route = f'./data/direction_{direction}/{routeId}.json'
        self.data_route = self.read_data(self.file_route)
        self.create_data_stops()
        
    def read_data(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data['result']
        except Exception as e:
            print("Error:", e)
            return None 

    def get_coords_route(self):
        path_route = self.data_route[0]['path']
        coords = []
        for addr in path_route:
            coords.append([addr['lat'], addr['lon']])
        return coords
    
    def create_data_stops(self):
        stopsInfo = self.read_data(self.file_stops)
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
        # with open('./data/1065_stops.json', 'w', encoding='utf-8') as file:
        #     json.dump(stops_1062, file, ensure_ascii=False, indent=4)
        return self.stops_route
    
    def get_name_route(self):
        info_name_routes = self.read_data('./data/routes.json')
        for name_route in info_name_routes:
            if name_route['id'] == self.routeId:
                return name_route['long_name']
        
def get_all_routesId():
    path = './data/direction_0'
    files = os.listdir(path)
    routesId = []
    for file in files:
        if file.endswith('.json'):
            route = file.split('.')[0]
            routesId.append(route)
    return routesId

def get_info_general_routes():
    with open('./data/routes.json', 'r', encoding='utf-8') as file:
            data = json.load(file)['result']
            
    data_all_routes = []
    Ids = get_all_routesId()
    for route in data:
        if route['id'] in Ids:
            data_all_routes.append([int(route['id']), route['long_name'], route['ticket'], route['time']])
    
    return data_all_routes  

def get_info_general_route_by_id(id_route):
    with open('./data/routes.json', 'r', encoding='utf-8') as file:
            data = json.load(file)['result']
            
    for route in data:
        if route['id'] == str(id_route):
            data_route = [int(route['id']), route['long_name'], route['ticket'], route['time']]
            return data_route 
    return None

BASE_URl = 'http://127.0.0.1:5000'

def get_info_update():
    url = f"{BASE_URl}/info-update"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

if __name__ == '__main__':
    data_route = init_data_route('1062', 0)
    #print(data_route.get_stops_of_route())
    res = data_route.get_coords_route()
    #print(data_route.data_stops)
    print(get_info_general_route_by_id(1062))


