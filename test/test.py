from nicegui import ui

with ui.row().classes('flex flex-row w-full min-h-screen p-4 gap-4 bg-slate-900'):

    with ui.card().classes('flex-1 h-64 bg-gray-800 text-white p-4'):
        ui.label('Left card')

    with ui.card().classes('flex-1 h-64 bg-gray-800 text-white p-4'):
        ui.label('Right card')

ui.run()
