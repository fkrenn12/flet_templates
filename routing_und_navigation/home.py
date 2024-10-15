import flet as ft
from project_colors import *


def homeView(page):
    menu = ft.Row(controls=[
        ft.Icon(ft.icons.MENU, color=prim_letter_color),
        ft.Icon(ft.icons.POWER_SETTINGS_NEW_OUTLINED, color=prim_letter_color)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    ueberschrift = ft.Container(
        content=(ft.Text("Welcome here...", size=30, color=prim_letter_color)),
        margin=ft.margin.only(top=20)
    )

    box = ft.Container(
        bgcolor=blue,
        height=80,
        width=140,
        border_radius=10,
        margin=ft.margin.only(top=20, bottom=20)
    )

    boxen = ft.Row(
        controls=[box, box, box]
    )

    aufgaben = ft.Container(
        height=450,
        # bgcolor=rot
    )

    aufgabenListe = ft.Stack(
        controls=[
            aufgaben,
            ft.FloatingActionButton(icon=ft.icons.ADD, bgcolor=yellow, right=20, bottom=20,
                                    on_click=lambda _: page.go('/task'))
        ]
    )

    home = ft.Row(
        controls=[
            ft.Container(
                bgcolor=green,
                height=780,
                width=480,
                border_radius=30,
                padding=ft.padding.only(top=40, left=20, right=40),
                content=ft.Column(
                    controls=[
                        menu, ueberschrift, boxen, aufgabenListe
                    ]
                )
            )
        ]
    )
    return home
