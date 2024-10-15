import flet as ft
from project_colors import *
from home import homeView
from navigation import routing


def main(page: ft.Page):
    page.window.height = 800
    page.window.width = 500
    page.title = "📝 App Title"
    page.bgcolor = "black"

    homeContainer = ft.Container(
        bgcolor=blue,
        height=780,
        width=500,
        border_radius=30,
        content=ft.Stack(
            controls=[
                homeView(page)
            ]
        )
    )

    def route_change(route):
        page.views.clear()
        page.views.append(
            routing(page)[page.route]
        )
        page.update()

    page.theme_mode = ft.ThemeMode.DARK
    page.add(homeContainer)

    page.on_route_change = route_change


# page.go('/')

ft.app(target=main)
