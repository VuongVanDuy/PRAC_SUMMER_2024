import sys
import os
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QApplication
from PyQt5.QtCore import QUrl
from .frame_tabs import frame_tabs
from .frame_hide import frame_hide
from .frame_view import frame_view
from .detail import DetailRoute
from ..data_app import *

class body_frame(QFrame):
    def __init__(self):
        super().__init__()
        self.all_routes = get_info_general_routes()
        self.html_file = './map/map_spb.html'
        
        self.body_layout = QHBoxLayout(self)
        self.frame_tabs = frame_tabs(self.all_routes)
        self.body_layout.addWidget(self.frame_tabs)
        
        self.frame_hide = frame_hide()
        self.body_layout.addWidget(self.frame_hide)
        
        self.frame_view = frame_view(self.html_file)
        self.body_layout.addWidget(self.frame_view)
        
        self.detail_widget = DetailRoute()
        self.body_layout.insertWidget(0, self.detail_widget)
        self.detail_widget.setVisible(False)
        
        self.frame_tabs.clickedRoute.connect(self.showDetailRoute)
        self.frame_hide.hide_button.clicked.connect(self.toggle_visibility_tabs) 
    
    def showDetailRoute(self, route):
        try:
            self.cur_data_route = init_data_route(route, direction=0)
        except Exception as e:
            print(e)
            return
        
        self.frame_tabs.setVisible(False) 
        self.detail_widget.update_frame_detail(new_cur_route=self.cur_data_route)  
        self.detail_widget.setVisible(True)
        self.showRoute(f"./map/direction_{self.cur_data_route.direction}/{route}" + ".html")  
        self.frame_hide.hide_button.clicked.disconnect(self.toggle_visibility_tabs)
        self.frame_hide.hide_button.clicked.connect(self.toggle_visibility_details)
        self.detail_widget.changedAddr.connect(self.update_location)
        self.detail_widget.changedDirection.connect(self.change_direction) 
        self.detail_widget.back_button.clicked.connect(self.backMainTabs)
    
    def showRoute(self, html_file):
        url = QUrl.fromLocalFile(os.path.realpath(html_file))
        self.frame_view.map.setUrl(url)
    
    def change_direction(self, direction):
        self.direction = direction
        self.cur_data_route = init_data_route(self.cur_data_route.routeId, self.direction)
        self.showRoute(f"./map/direction_{self.direction}/{self.cur_data_route.routeId}.html")
        self.detail_widget.update_direction(self.cur_data_route)
    
    def update_location(self, newAddr):
        stops_of_route = self.cur_data_route.get_stops_of_route()
        lat = stops_of_route[newAddr][0]
        lon = stops_of_route[newAddr][1]
        # Call JavaScript function to update marker location
        self.frame_view.map.page().runJavaScript(f"updateMarker({lat}, {lon});")
    
    def backMainTabs(self):
        self.showRoute('./map/map_spb.html')
        self.detail_widget.setVisible(False)
        self.frame_tabs.setVisible(True)
        self.frame_hide.hide_button.clicked.disconnect(self.toggle_visibility_details)
        self.frame_hide.hide_button.clicked.connect(self.toggle_visibility_tabs)
        
    def toggle_visibility_tabs(self):
        if self.frame_tabs.isVisible():
            self.frame_tabs.setVisible(False)
            self.frame_hide.hide_button.setText('▶')
        else:
            self.frame_tabs.setVisible(True)
            self.frame_hide.hide_button.setText('◀')
    
    def toggle_visibility_details(self):
        if self.detail_widget.isVisible():
            self.detail_widget.setVisible(False)
            self.frame_hide.hide_button.setText('▶')
        else:
            self.detail_widget.setVisible(True)
            self.frame_hide.hide_button.setText('◀')
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    h_lay = body_frame(html_file='./map/direction_0/1062.html')
    h_lay.show()
    sys.exit(app.exec_())