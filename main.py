#from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.clock import Clock
from applayout import MDScreen
from applayout import AppLayout
from applayout import ButtonsLayout
from applayout import ButtonsLayoutInfo
from applayout import Content
from applayout import Settings
from applayout import Weather
#from applayout import Example
from android_permissions import AndroidPermissions
from kivymd.app import MDApp
from kivy.uix.button import Button
#from applayout import ClassifyObject
#import pandas as pd
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import csv
import json
import requests


from kivy.lang import Builder



#3Builder.load_file('setupkv.kv')
#Builder.load_file('setupkv_1.kv')

kv = Builder.load_file('setupkv.kv')
#kv = Builder.load_file('setupkv_1.kv')

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    from android import mActivity
    View = autoclass('android.view.View')

    @run_on_ui_thread
    def hide_landscape_status_bar(instance, width, height):
        # width,height gives false layout events, on pinch/spread 
        # so use Window.width and Window.height
        if Window.width > Window.height: 
            # Hide status bar
            option = View.SYSTEM_UI_FLAG_FULLSCREEN
        else:
            # Show status bar 
            option = View.SYSTEM_UI_FLAG_VISIBLE
        mActivity.getWindow().getDecorView().setSystemUiVisibility(option)
elif platform != 'ios':    
    # Dispose of that nasty red dot, required for gestures4kivy.
    from kivy.config import Config 
    Config.set('input', 'mouse', 'mouse, disable_multitouch')

 


class MyApp(MDApp):

    dialog = None
    
    
    
    def build(self):
        #Initialize continue detection
        self.continue_detection_value = 0  
        #Initialize info button
        self.info_button_value = 0         
        
        self.started = False
        if platform == 'android':
            Window.bind(on_resize=hide_landscape_status_bar)

        
        
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.layout = MDScreen()
        self.cameradetect = AppLayout()       
        
        self.layout.add_widget(self.cameradetect)     
        
        self.addinfobutton = ButtonsLayoutInfo()       
        
     

        
        #To remove widget - nb clock still runs camera in background
        #self.layout.remove_widget(self.cameradetect)         
        
           
        #self.addcamerabutton = ButtonsLayout()
        #self.layout.add_widget(self.addcamerabutton) 
       
        
        #self.layout.add_widget(self.addinfobutton)
  
        
      
         
        return self.layout
       
        
        
        
        #return kv
        
    def navigation_draw(self):
        print("Navigation")    

    def on_start(self, *args):
        self.dont_gc = AndroidPermissions(self.start_app)

    def start_app(self):
        self.dont_gc = None
       
        # Can't connect camera till after on_start()
        Clock.schedule_once(self.connect_camera)
        #Clock.schedule_once(self.on_stop, 10)
        #Clock.schedule_once(self.on_start, 20)

    def connect_camera(self,dt):    
        #self.layout.detect.connect_camera(enable_analyze_pixels = True)
        #MDApp.root.applayout.detect.connect_camera(enable_analyze_pixels = True)
        #self.root.layout.detect.connect_camera(enable_analyze_pixels = True)
        self.cameradetect.detect.connect_camera(enable_analyze_pixels = True)
        
      
        #pass
        
        
    def screenshot(self):
        self.cameradetect.detect.capture_screenshot()
        #self.parent.addcamerabuttondetect.detect.capture_screenshot()
        #self.cameradetect.detect.connect_camera(enable_analyze_pixels = True)
        #self.detect.capture_screenshot()
        #self.addcamerabutton.detect.capture_screenshot()
        #self.parent.addcamerabutton.detect.capture_screenshot()
        #self.addcamerabutton.detect.capture_screenshot()
        #self.applayout.detect.capture_screenshot()       
        print("Did screenshot") 
       

    def on_stop(self, *args):
        
        #self.layout.detect.disconnect_camera()
        #self.layout.detect.disconnect_camera()
        self.cameradetect.detect.disconnect_camera()
        print("camera stopped")
        
        
    def remove_camera_layout(self, *args):
    
        
        
        #self.layout.detect.disconnect_camera()
        #self.layout.detect.disconnect_camera()
        #self.cameradetect.detect.disconnect_camera()
        self.layout.remove_widget(self.cameradetect)
        self.layout.remove_widget(self.addcamerabutton)
        print("remove_camera_layout")
        #self.layout.add_widget(self.cameradetect) 
        #print(MyApp.get_running_app())
        
  
    def add_camera_layout(self, *args):
        
        #self.layout.detect.disconnect_camera()
        #self.layout.detect.disconnect_camera()
        #self.cameradetect.detect.disconnect_camera()
        #self.layout.remove_widget(self.cameradetect)        
        self.layout.add_widget(self.cameradetect)       
        self.layout.add_widget(self.addcamerabutton) 
    
        print("added_camera_layout")      
        
        
        
        
              

    def add_object_info_layout(self, *args):
        
        #self.layout.detect.disconnect_camera()
        #self.layout.detect.disconnect_camera()
        #self.cameradetect.detect.disconnect_camera()
        #self.layout.remove_widget(self.cameradetect)        
        #self.layout.add_widget(self.cameradetect)  
        
        lst = []
            
        #self.layout.remove_widget(self.addinfobutton) 
        print("added_object_info_layout")  
        print("image name") 
        #for arg in args:
            #self.detected_object_name = arg
            #print(self.detected_object_name)
            #self.new_text = self.detected_object_name
            
            
        for arg in args:
            #self.new_text = arg
            lst.append(arg)
            #print("args")    

        self.detected_object_name = lst[0]
        self.probability_highest_value = lst[1]    
            
            
            
            
        


        file = open("csv/object_info.csv", "r")
        data = list(csv.reader(file, delimiter=","))
        file.close() 
        print("file data")   
        print(data)  
        
        index_of_list_value = next(i for i,v in enumerate(data) if self.detected_object_name in v)
        print('index_of_list_value')
        print(index_of_list_value)
        
        #list_row = data[[3][0]]
        list_row = data[[index_of_list_value][0]]
        
        #self.detected_object_name_1 = list_row[1]
        #print('sef.detected_object_name_1')
        #print(self.detected_object_name_1)
        
        
        
        
       
        self.detected_object_name = list_row[0]
        self.object_general_info = list_row[1]
        self.object_info_1 = list_row[2]
        self.object_info_2 = list_row[3]
        
        
        
        #self.object_all_info = self.detected_object_name +"\n" + self.object_general_info + "\n" + self.object_info_1
        self.object_all_info = self.object_general_info
            
        #self.addinfobutton = ButtonsLayoutInfo() 
        
        #Only add info button once. Thereafter move it out of sight and back in sight again
        print("self.info_button_value")
        print(self.info_button_value)
        if(self.info_button_value == 0):   
            self.layout.add_widget(self.addinfobutton) 
            self.info_button_value = 1
            
        
        #self.layout.remove_widget(self.addinfobutton) 
        #self.addinfobutton.remove_btn(self.addinfobutton)
       
        #self.addinfobutton.add_btn(self.detected_object_name, self.object_general_info, self.object_info_1)
        self.addinfobutton.add_btn(self.detected_object_name, self.object_all_info, self.probability_highest_value)
        
        #Set a timer that removes the info button after x amount of seconds if the user does
        #not open the dialog box in time 
        self.remove_button_time_expired(self)
        
        
        #self.continue_detection_value set value to 1 to stop detecting
        self.continue_detection_value = 1
        
    def remove_button_time_expired(self, *args):  
        print("we are going to remove the button as the timer will expire")     
        self.time_expired = Clock.schedule_once(self.remove_button_time_expired_confirmed,5)
   


    def cancel_remove_button_time_expired(self, *args):  
        #We need to cancel the clock schedule to remove the info button as the user
        #clicked on the Dialog box in time
        print("The dialog box was opened so stop the remove button cloack schedule")     
        self.time_expired.cancel()

       


    def remove_button_time_expired_confirmed(self, *args):  
        print("we have removed the button as the timer has expired")     
        Clock.schedule_once(self.addinfobutton.remove_btn,1)
        self.continue_detection_value = 0

        
    '''    
    def show_alert_dialog(self):
            #Stop the clock schedule from removing the info button as dialog was opened
            self.cancel_remove_button_time_expired(self)
            
            if not self.dialog:
                self.dialog = MDDialog(
                    #size_hint= [0.9, None],
                    size_hint= [0.8, 0.5],
                    #Dont allow the user to close the dialog by click outside the box
                    auto_dismiss = False,
                    #title=self.detected_object_name,
                    #text=self.object_all_info,                   
                    type="custom",
                    #content_cls=Content(self),
                    content_cls=Content(),
                    buttons=[
                      
                        MDFlatButton(
                            text="Close",
                            on_release=self.closeDialog,
                            theme_text_color="Custom",
                            text_color=self.theme_cls.primary_color,
                        ),
                    ],
                )
            #Prevent the user from closing the dialog box by clicking outside the area    
            #self.dialog.bind(on_dismiss=self.dont_close_dialog)    
            self.dialog.open() 
            self.dialog.content_cls.add_img_name(self.detected_object_name, self.object_all_info, self.object_info_1, self.object_info_2)  
             
            #self.remove_info_button_layout(self)
               

    #def dont_close_dialog(self,instance):
        #print('Popup', instance, 'is being dismissed but is prevented!')
        #return True   
    
    
    def closeDialog(self, inst):
        self.dialog.dismiss()
        print("closeDialog pressed")
        
        #Continue to detect images in classifyobject.py        
        #self.continue_detection_value set value to 0 to continue detecting
        self.continue_detection_value = 0
       
            
        #self.layout.remove_widget(self.addinfobutton) 
        #self.addinfobutton.remove_btn(self.addinfobutton)
        
    '''    
        

    def continue_detection(self, *args):   
            continue_to_detect = self.continue_detection_value
      
            return continue_to_detect
       
 
 

    def show_alert_dialog(self):   
        print("we at show_alert_dialog")
        #Stop the clock schedule from removing the info button as dialog was opened
        self.cancel_remove_button_time_expired(self)
       
        self.adddialog = Content()  
      
        self.layout.add_widget(self.adddialog)   
        self.adddialog.add_img_name(self.detected_object_name, self.object_all_info, self.object_info_1, self.object_info_2)   


    def remove_show_alert_dialog(self, *args):   
        print("we removed show_alert_dialog")
        #self.addsettings = Settings()  
        #self.layout.add_widget(self.addsettings) 
        self.layout.remove_widget(self.adddialog)  
        #Continue to detect images in classifyobject.py        
        #self.continue_detection_value set value to 0 to continue detecting
        self.continue_detection_value = 0



    def settings(self, *args):   
        print("we at settings")
       
        self.addsettings = Settings()  
        self.layout.add_widget(self.addsettings)    


    def remove_settings(self, *args):   
        print("we removed settings")
        #self.addsettings = Settings()  
        #self.layout.add_widget(self.addsettings) 
        self.layout.remove_widget(self.addsettings)   
        


    def weather(self, *args):   
        print("we at weather")
       
        self.addweather = Weather()  
        self.layout.add_widget(self.addweather)    


    def remove_weather(self, *args):   
        print("we removed weather")
        #self.addsettings = Settings()  
        #self.layout.add_widget(self.addsettings) 
        self.layout.remove_widget(self.addweather)  
        
        
        
    def get_weather(self, city_name):   
        print("we at get weather")
        try:
        
       
            #url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}$appid={self.api_key}"
            #response = requests.get(url)
            
                     
            json_data_weather = '{"location": "East London", "temp": 282.21,"humidity": 65,"cod": "200","id": 2.55,"wind_speed": 20,"weather": "Clear sky"}'
            json_data_tides = '{"Day": "Wed 01", "High1": "5:32 AM SAST 0.94 m","Low1": "11:44 AM SAST 1.26 m","High2": "6:27 PM SAST 0.83 m","Low2":"7:22 PM SAST 0.74 m"}'          
                        
                
   
                 
            #x = response.json()     
            #x = json.dumps(json_data)
            x = json.loads(json_data_weather)
            y = json.loads(json_data_tides)
                
            
            print(x)
            print(type(x))
            
            #if x["cod"][0] != "404":
            a = 0
            if(a == 0):
                temperature = round(x["temp"]-273.15)
                humidity = x["humidity"]
                wind_speed = round(x["wind_speed"]*18/5)
                weather = x["weather"]
                location = x["location"]
                
                self.addweather.ids.temperature.text = f"[b]{temperature}[/b]°"
                self.addweather.ids.weather.text = str(weather)
                self.addweather.ids.humidity.text = f"{humidity}%"
                self.addweather.ids.wind_speed.text = f"{wind_speed} km/h"
                self.addweather.ids.location.text = str(location)


                high1 = y["High1"]
                low1 = y["Low1"]
                high2 = y["High2"]
                low2 = y["Low2"]                
      
                
               
                self.addweather.ids.high1.text = str(high1)
                self.addweather.ids.low1.text = str(low1)
                self.addweather.ids.high2.text = str(high2)
                self.addweather.ids.low2.text = str(low2)


                
                
            else:
                print("City not found")   
              
                 
        except requests.ConnectionError:
            print("No internet conection")
        
        
    def search_weather(self):   
        print("we at search weather")
        self.get_weather("Delhi")
                       


MyApp().run()

