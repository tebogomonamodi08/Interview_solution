from nicegui import ui

with ui.card().tight():
    ui.label('Testing')
    ui.button('Click Me', on_click= lambda : ui.label('I am clicked.'))

with ui.list():
    with ui.slide_item('slide me') as slider_1:
        slider_1.right('Hey', color='red')


ui.run()  