from nicegui import ui

ui.query('body').classes('bg-gray-800')

with ui.card():
    ui.label('Hey')




ui.run()