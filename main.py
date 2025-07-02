from nicegui import ui
import asyncio

ui.query('body').classes('bg-[#0d1117] text-white')  # Set dark background color

# Shared loading state
is_loading = ui.spinner('hourglass').classes('text-primary').props('size="md"')
is_loading.visible = False

with ui.row().classes('w-full h-screen p-6 gap-4'):

    # Left Card: Webcam Stream + Buttons
    with ui.card().classes('w-1/2 h-[500px] bg-[#1e1e1e] rounded-2xl shadow-lg flex flex-col justify-between p-4'):
        ui.label('🎥 Webcam Stream').classes('text-xl text-white')
        ui.image('http://localhost:8000/video').classes('rounded-xl w-full h-[300px] bg-black')

        with ui.row().classes('justify-center gap-4 mt-4'):
            async def start_clicked():
                is_loading.visible = True
                await asyncio.sleep(5)  # Simulate delay
                is_loading.visible = False

            ui.button('Start', on_click=start_clicked).props('outline color="primary"').classes('text-white')
            ui.button('Cancel').props('outline color="primary"').classes('text-white')
            is_loading

    # Right Card: Instructions
    with ui.card().classes('w-1/2 h-[500px] bg-[#1e1e1e] rounded-2xl shadow-lg p-4'):
        ui.label('📄 Instructions').classes('text-xl text-white mb-2')
        ui.markdown('''
        1. Click **Start** to begin your interview.
        2. Speak clearly and stay within frame.
        3. Your answers will be analyzed for clarity and confidence.
        ''')
        ui.button('Upload CV').props('color="primary" outline').classes('mt-auto')

ui.run()





