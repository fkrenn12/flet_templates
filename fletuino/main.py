import flet as ft
import mqtt
import serial_comm
from controls import Controls


def main(page: ft.Page):
    controls = Controls(page, mqtt)
    page.title = "Fletuino - Easy Visualisation for any Microcontroller"
    page.theme_mode = ft.ThemeMode.DARK
    page.controls = controls
    page.scroll = "adaptive"
    page.update()
    mqtt.mqtt_client.loop_start()
    serial_comm.loop.start()


ft.app(target=main)
