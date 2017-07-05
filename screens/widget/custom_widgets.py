from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.uix.label import Label


def build_button(disp_text='', xPos=0, yPos=0, rect_size=[10,10], pos=[0,0], resource=''):
    button = Button(text = disp_text)
    button.x = xPos
    button.y = yPos
    button = texture(button, rect_size, pos, resource)
    button.size = rect_size
    button.background_color = [0,0,0,0]
    return button


def build_data_button(disp_text='', xPos=0, yPos=0, rect_size=[10,10], pos=[0,0], resource='', custom_data={}):
    button = build_button(disp_text, xPos, yPos, rect_size, pos, resource)
    button.CUSTOM_DATA = custom_data
    return button


def build_click_button(disp_text='', xPos=0, yPos=0, rect_size=[10,10], pos=[0,0], resource='', button_bind=None):
    button = build_button(disp_text, xPos, yPos, rect_size, pos, resource)
    button.bind(on_press=button_bind)
    return button


def build_label(disp_text='', xPos=0, yPos=0, rect_size=[10,10], pos=[0,0], resource=''):
    label = Label(text= disp_text)
    label.x = xPos
    label.y = yPos
    label = texture(label, rect_size, pos, resource)
    return label


def texture(button, rect_size, pos, resource):
    with button.canvas.before:
        button.rect = Rectangle(source=resource, size=rect_size, pos=[button.get_center_x() + pos[0], button.y + pos[1]])
    return button