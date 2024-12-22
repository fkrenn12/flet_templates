import flet as ft
import serial_comm
import json

SEND_TOPIC = '121213'
SUPPORTED = ["Screen", "Button", "Text", "Switch", "Slider", "Dropdown", "TextField"]


class Controls(list):
    def __init__(self, page: ft.Page, mqtt=None):
        super().__init__()
        self.page = page
        self.mqtt = mqtt
        mqtt.register_callback(self.mqtt_incoming)
        serial_comm.register_callback(self.mqtt_incoming)

    def mqtt_incoming(self, payload):
        payload = json.loads(payload)
        self.processing(payload)
        self.page.update()

    def mqtt_publish(self, payload: dict):
        payload = json.dumps(payload)
        self.mqtt.mqtt_client.publish(SEND_TOPIC, payload)
        try:
            payload = payload + '\n'
            serial_comm.ser.write(payload.encode())
            print(f'Sent seial: {payload}')
        except:
            pass

    def exist(self, name: str = str()) -> bool:
        for control in self:
            if control.name == name:
                return True
        else:
            return False

    def control(self, name: str = str()):
        for control in self:
            if control.name == name:
                return control
        else:
            return None

    def processing(self, control: dict):
        if control.get("type") not in SUPPORTED:
            return

        if control.get("type") == 'Screen':
            self.page.bgcolor = control.get("bgcolor", self.page.bgcolor)
            return
        else:
            if not self.exist(control.get("name")):
                print(f'Do not exist')
                if control.get("type") == "Text":
                    self.append(Text(name=control.get("name")))
                elif control.get("type") == "Button":
                    self.append(Button(name=control.get("name"), _on_click=self.mqtt_publish))
                elif control.get("type") == "Switch":
                    self.append(Switch(name=control.get("name"), _on_change=self.mqtt_publish))
                elif control.get("type") == "Slider":
                    self.append(Slider(name=control.get("name"), _on_change=self.mqtt_publish))
                elif control.get("type") == "Dropdown":
                    self.append(Dropdown(name=control.get("name"), _on_change=self.mqtt_publish))
                elif control.get("type") == "TextField":
                    self.append(TextField(name=control.get("name"), _on_submit=self.mqtt_publish))
            else:
                print('exist')

        ctl = self.control(name=control.get("name"))
        ctl.set_properties(control)
        self.page.controls = self


class Text(ft.Text):
    def __init__(self, name: str = str(), visible=True):
        super().__init__()
        self.name = name
        self.visible = visible

    def did_mount(self):
        self.update()

    def set_properties(self, properties: dict):
        self.visible = properties.get('visible', self.visible)
        self.value = properties.get('text', self.value)
        self.size = properties.get('size', self.size)
        self.color = properties.get('color', self.color)
        self.bgcolor = properties.get('bgcolor', self.bgcolor)


class TextField(ft.TextField):
    def __init__(self, name: str = str(), _on_submit=None, visible=True):
        super().__init__()
        self.name = name
        self.visible = visible
        self.__size = 10
        self.on_blur = self.__on_submit
        self.on_submit = self.__on_submit
        self._on_submit = _on_submit

    def did_mount(self):
        self.update()

    def set_properties(self, properties: dict):
        self.__size = properties.get('size', self.__size)
        self.visible = properties.get('visible', self.visible)
        self.label = properties.get('text', self.label)
        self.text_style = ft.TextStyle(size=self.__size)
        self.color = properties.get('color', self.color)
        self.bgcolor = properties.get('bgcolor', self.bgcolor)

    def __on_submit(self, e=None):
        self._on_submit({"name": self.name, "event": "submit", "value": self.value})

class Dropdown(ft.Dropdown):
    def __init__(self, name: str = str(), _on_change=None, visible=True):
        super().__init__()
        self.name = name
        self.visible = visible
        self.on_change = self.__on_change
        self._on_change = _on_change
        self.__options = list()

    def did_mount(self):
        self.update()

    def set_properties(self, properties: dict):
        self.__options = properties.get('options', self.__options)
        options = list()
        for opt in self.__options:
            options.append(ft.dropdown.Option(str(opt)))
        self.options = options # [ft.dropdown.Option("Red")]
        self.visible = properties.get('visible', self.visible)
        self.label = properties.get('text', self.label)
        self.color = properties.get('color', self.color)
        self.bgcolor = properties.get('bgcolor', self.bgcolor)

    def __on_change(self, e=None):
        self._on_change({"name": self.name, "event": "changed", "selection": self.value})



class Button(ft.ElevatedButton):
    def __init__(self, name: str = str(), _on_click=None, visible=True):
        super().__init__()
        self.name = name
        self.visible = visible
        self.on_click = self.__on_click
        self._on_click = _on_click
        self.__size = 10
        self.__click_count = 0

    def did_mount(self):
        self.update()

    def set_properties(self, properties: dict):
        self.visible = properties.get('visible', self.visible)
        self.text = properties.get('text', self.text)
        self.__size = properties.get('size', self.__size)
        self.style = ft.ButtonStyle(text_style=ft.TextStyle(size=self.__size))
        self.color = properties.get('color', self.color)
        self.bgcolor = properties.get('bgcolor', self.bgcolor)

    def __on_click(self, e=None):
        self.__click_count += 1
        self._on_click({"name": self.name, "event": "click", "count": self.__click_count})


class Switch(ft.Switch):
    def __init__(self, name: str = str(), _on_change=None, visible=True):
        super().__init__()
        self.name = name
        self.value = False
        self.on_change = self.__on_change
        self._on_change = _on_change
        self.visible = visible
        self.__size = 10
        self.__color = None
        self.__bgcolor = None

    def did_mount(self):
        self.update()

    def set_properties(self, properties: dict):
        self.visible = properties.get('visible', self.visible)
        self.label = properties.get('text', self.label)
        self.__color = properties.get('color', self.__color)
        self.__bgcolor = properties.get('bgcolor', self.__bgcolor)
        self.__size = properties.get('size', self.__size)
        self.label_style = ft.TextStyle(size=self.__size, color=self.__color, bgcolor=self.__bgcolor)

    def __on_change(self, e=None):
        self._on_change({"name": self.name, "event": "changed", "checked": self.value})


class Slider(ft.Column):
    def __init__(self, name: str = str(), _on_change=None, visible=True):
        super().__init__()
        self.__label = ft.Text()
        self.__slider = ft.Slider()
        self.visible = visible
        self.name = name
        self.__slider.min = 0
        self.__slider.max = 100
        self.__slider.divisions = self.__slider.max - self.__slider.min
        self.__slider.value = 0
        self.__slider.on_change = self.__on_change
        self._on_change = _on_change
        self.__size = 10
        self.__color = None
        self.__bgcolor = None

    def did_mount(self):
        self.update()

    def set_properties(self, properties: dict):
        self.__label.value = properties.get('text', str())
        self.__color = properties.get('color', self.__color)
        self.__slider.thumb_color = self.__color
        self.__bgcolor = properties.get('bgcolor', self.__bgcolor)
        self.__slider.bgcolor = self.__bgcolor
        self.__slider.active_color = self.__bgcolor
        self.__slider.inactive_color = self.__bgcolor
        self.__slider.min = properties.get('min', self.__slider.min)
        self.__slider.max = properties.get('max', self.__slider.max)
        self.__slider.divisions = self.__slider.max - self.__slider.min
        self.visible = properties.get('visible', self.visible)
        print(f'set properties self.__label.value {self.__label.value}')
        self.controls = [self.__slider]
        if self.__label.value:
            self.controls.insert(0, self.__label)

        self.__size = properties.get('size', self.__size)
        self.__label.style = ft.TextStyle(size=self.__size, color=self.__color, bgcolor=self.__bgcolor)

    def __on_change(self, e=None):
        self.__slider.label = "{value}"
        self._on_change({"name": self.name, "event": "changed", "position": self.__slider.value})
        self.update()
