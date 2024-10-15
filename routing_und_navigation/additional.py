import flet as ft
from project_colors import *


def additionalView(page):
    menu = ft.Row(controls=[
        ft.IconButton(icon=ft.icons.CANCEL, icon_color=blue,
                      on_click=lambda _: page.go('/')),
    ], alignment=ft.MainAxisAlignment.END)

    ueberschrift = ft.Container(
        content=(ft.Text("Adding Task", size=30, color=prim_letter_color)),
        margin=ft.margin.only(top=20)
    )

    additional = ft.Row(
        controls=[
            ft.Container(
                bgcolor=orange,
                height=780,
                width=480,
                border_radius=30,
                padding=ft.padding.only(top=40, left=20, right=40),
                content=ft.Column(
                    controls=[
                        menu, ueberschrift
                    ]
                )
            )
        ]
    )
    return additional
