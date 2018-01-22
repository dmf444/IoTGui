from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from backend.wemo import wemo as Wemo

from globals import SCREEN_WIDTH, SCREEN_HEIGHT
from screens.widget import custom_widgets as CustomWidgets


class WemoLayout(GridLayout):
    screen = ObjectProperty()
    _current_selected_wemo = None

    def __init__(self, **kwargs):

        super(WemoLayout, self).__init__(**kwargs)
        with self.canvas.before:
            self.rect = Rectangle(source='resources/background.png', size=[SCREEN_WIDTH, SCREEN_HEIGHT], pos=self.pos)

        device_number = 0
        inital_y = 340
        for device in Wemo.WEMO_NAME_MAP:
            self.add_widget(CustomWidgets.build_click_button(device, 10, inital_y - (55 * device_number), [177, 50], [-50,0], "resources/longbuttonNonSelect.png", self.select_wemo))
            device_number += 1

        self.bottom_bar = Image(source='resources/barDesignBackwards.png', size=[694, 48], pos=[17, 395])
        self.add_widget(self.bottom_bar)

        self.text_frame = Image(source='resources/selectionBackground.png', size=[445, 341], pos=[213, 74])
        self.add_widget(self.text_frame)

        self.toggle_button = CustomWidgets.build_button('', 552, 142, [208, 208], [-50,0], resource="resources/nullbutton.png")
        self.toggle_button.bind(on_press=self.toggle_light)
        self.add_widget(self.toggle_button)

        self.title_name = Label(text="NAME:", font_size=25, bold=True, pos=[242, 381], size=[220, 25])

        self.add_widget(self.title_name)

        self.wemo_name = Label(text="None Selected", text_size=[300, 25], font_size=25, pos=[222, 331], size=[300, 25], halign="left")
        self.add_widget(self.wemo_name)

        self.home_button = CustomWidgets.build_button('', 735, 420, [45, 45], [-50,0], resource="resources/home.png")
        self.home_button.bind(on_press=self.go_home)
        self.add_widget(self.home_button)

        self.bottom_bar = Image(source='resources/bottombar.png', size=[768, 33], pos=[17, 10])
        self.add_widget(self.bottom_bar)

    def toggle_light(self, *args):
        if(self._current_selected_wemo is not None):
            Wemo.WEMO_NAME_MAP[self._current_selected_wemo].toggle()
            self.update_button()

    def go_home(self, *args):
        self.screen.manager.current = "main"

    def select_wemo(self, *args):
        self.set_current_wemo(args[0].text)
        self.update_button()
        self.update_labels()

    def update_labels(self):
        self.wemo_name.text = self._current_selected_wemo

    def update_button(self):
        state = Wemo.WEMO_NAME_MAP[self._current_selected_wemo].get_state()
        if(state == 1):
            print("SCREW YOU")
            print("Button is {}".format(self.toggle_button.disabled))
            d = "resources/onbutton.png"
            self.canvas.ask_update()
        else:
            print("MISERERE MEI DEUS " + self.toggle_button.background_normal)
            d = "resources/offbutton.png"
            self.canvas.ask_update()

        self.remove_widget(self.toggle_button)
        togg = CustomWidgets.build_button('', 552, 142, [208, 208], [-50,0], resource=d)
        togg.bind(on_press=self.toggle_light)
        self.add_widget(togg)
        self.toggle_button = togg

    def set_current_wemo(self, wemo_name):
        self._current_selected_wemo = wemo_name


class WemoScreen(Screen):
    def __init__(self, **kw):
        super(WemoScreen, self).__init__(**kw)

        self.add_widget(WemoLayout(screen=self))