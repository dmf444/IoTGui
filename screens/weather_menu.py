from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from backend.weather.weatherwrapper import weatherModule

from globals import SCREEN_WIDTH, SCREEN_HEIGHT
from screens.widget import custom_widgets as CustomWidgets


class WeatherLayout(GridLayout):
    screen = ObjectProperty()
    image_reference = {"01n": "sunny", "01d" : "sunny", "02n": "sunny_clouds", "02d" : "sunny_clouds", "03n": "cloudy", "03d" : "cloudy",
                       "04n": "cloudy", "04d" : "cloudy", "09n": "shower_rain", "09d": "shower_rain", "10n": "rain", "10d" : "rain",
                       "11n": "thunderstorm", "11d" : "thunderstorm", "13n": "snow_heavy", "13d" : "snow_heavy", "50n": "mist", "50d": "mist"}

    def __init__(self, **kwargs):

        super(WeatherLayout, self).__init__(**kwargs)
        with self.canvas.before:
            self.rect = Rectangle(source='resources/background.png', size=[SCREEN_WIDTH, SCREEN_HEIGHT], pos=self.pos)



        for i in range(5):
            self.add_widget(CustomWidgets.build_label("", 12 + (144*i + 14*i), 97, [144, 275], [-50, 0], 'resources/weatherbox.png'))
            status = self.screen.get_weather().get_status(i)
            icon = self.image_reference[self.screen.get_weather().get_current_icon(i)]
            temp = "Current Temp: " + str(self.screen.get_weather().get_current_temp(i)) + "\n\n" + "Max Temp: " + str(self.screen.get_weather().get_max_temp(i)) + "\nMin Temp: " + str(self.screen.get_weather().get_min_temp(i))
            if(len(status) > 18):
                status = status[:18] + "\n" + status[18:]
            self.add_widget(ULabel(text=status, font_size=14, halign="center", bold=True, pos=[14 + (144*i + 14*i), 209], size=[136, 34]))
            self.add_widget(ULabel(text=temp, font_size=12, halign="center", bold=False, pos=[14 + (144 * i + 14 * i), 117], size=[136, 89]))
            self.add_widget(CustomWidgets.build_label("", 34 + (144 * i + 14 * i), 250, [100, 100], [-50, 0], 'resources/weather_icon/' + icon + '.png'))

        self.bottom_bar = Image(source='resources/barDesignBackwards.png', size=[694, 48], pos=[17, 395])
        self.add_widget(self.bottom_bar)



        #self.title_name = Label(text="NAME:", font_size=25, bold=True, pos=[242, 381], size=[220, 25])
        #self.add_widget(self.title_name)

        #self.wemo_name = Label(text="None Selected", text_size=[300, 25], font_size=25, pos=[222, 331], size=[300, 25], halign="left")
        #self.add_widget(self.wemo_name)

        self.home_button = CustomWidgets.build_button('', 735, 420, [45, 45], [-50,0], resource="resources/home.png")
        self.home_button.bind(on_press=self.go_home)
        self.add_widget(self.home_button)

        self.bottom_bar = Image(source='resources/bottombar.png', size=[768, 33], pos=[17, 10])
        self.add_widget(self.bottom_bar)

    def go_home(self, *args):
        self.screen.manager.current = "main"



class WeatherScreen(Screen):
    _weather = None

    def __init__(self, **kw):
        super(WeatherScreen, self).__init__(**kw)
        self._weather = weatherModule()
        self._weather.query_week()

        self.add_widget(WeatherLayout(screen=self))

    def update_weather(self):
        self._weather.query_week()

    def get_weather(self):
        return self._weather


class ULabel(Label):
    def __init__(self, **kwargs):
        super(ULabel, self).__init__(**kwargs)
        #self.text= str(time.asctime())
        Clock.schedule_interval(self.update, 3600)

    def update(self, *args):
        #self.text = str(time.asctime())
        print("YO")