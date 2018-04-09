import pyowm

class weatherModule():

    def __init__(self):
        self.weather = pyowm.OWM('3e50224f2d8e6458dcc6a9b57fe7f313')
        self.forcast = []

    def query_temp(self):
        self.forcast.clear()
        self.forcast = [self.weather.weather_at_place("Toronto,CA").get_weather()]

    def query_week(self):
        self.forcast.clear()
        self.forcast = self.weather.three_hours_forecast("Toronto,CA").get_forecast().get_weathers()[:6]

    def get_current_icon(self, day=0):
        return self.forcast[day].get_weather_icon_name()

    def get_current_temp(self, day=0):
        return self.forcast[day].get_temperature('celsius')['temp']

    def get_min_temp(self, day=0):
        return self.forcast[day].get_temperature('celsius')['temp_min']

    def get_max_temp(self, day=0):
        return self.forcast[day].get_temperature('celsius')['temp_max']

    def get_status(self, day=0):
        return self.forcast[day].get_detailed_status().title()


if(__name__ == "__main__"):
    m = weatherModule()
    m.query_week()
    print(m.get_current_icon())
    print(m.get_current_temp())
    print(m.get_min_temp())
    print(m.get_max_temp())
    print(m.get_status())
    print(m.get_current_icon())