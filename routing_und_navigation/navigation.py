import flet as ft
from home import homeView
from additional import additionalView


def routing(page):
    return {
        '/': ft.View(
            route='/',
            controls=[
                homeView(page)
            ]
        ),
        '/task': ft.View(
            route='/task',
            controls=[
                additionalView(page)
            ]
        )
    }
