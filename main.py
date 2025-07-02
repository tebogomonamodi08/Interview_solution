from nicegui import ui
import asyncio

# --- GLOBAL DARK THEME ---
ui.query('body').classes('bg-[#0d1117] text-white')

# --- TYPING EFFECT FUNCTION ---
async def type_title(label, text, delay=0.1):
    typed = ''
    cursor = '▌'
    for char in text:
        label.text = f'{cursor} {typed}'
        await asyncio.sleep(delay)
        typed += char
    label.text = typed  # Remove cursor once typing ends

# --- TITLE SECTION ---
with ui.column().classes('items-center pt-8 pb-2'):
    title_label = ui.label('').classes('text-4xl font-bold text-white font-mono')
    ui.timer(0.5, lambda: asyncio.create_task(
        type_title(title_label, '🧠 AI Interview Assistant')
    ), once=True)

# --- MAIN FLEX LAYOUT ---
with ui.row().classes('flex flex-row w-full min-h-screen p-6 gap-6 bg-[#0d1117]'):

    # --- LEFT CARD: Webcam + Action Buttons ---
    with ui.card().classes(
        'flex-1 min-w-0 h-[500px] bg-[#161b22] rounded-2xl shadow-xl flex flex-col justify-between p-5'
    ):
        ui.label('🎥 Webcam Stream').classes('text-2xl font-bold text-white')

        ui.image('http://localhost:8000/video').classes(
            'rounded-xl w-full h-[300px] object-cover bg-black')

        with ui.row().classes('justify-center gap-4 mt-4'):
            start_button = ui.button(icon='play_arrow', text='Start').props('outline color=primary').classes('text-white')
            cancel_button = ui.button(icon='close', text='Cancel').props('outline color=red').classes('text-white')

            async def on_button_click(btn):
                original_text = btn.text
                btn.text = '⏳ Working...'
                btn.props('loading')
                await asyncio.sleep(3)  # Simulate async operation
                btn.text = original_text
                btn.props(remove='loading')

            start_button.on('click', lambda e: on_button_click(start_button))
            cancel_button.on('click', lambda e: on_button_click(cancel_button))

    # --- RIGHT CARD: Instructions + Upload ---
    with ui.card().classes(
        'flex-1 min-w-0 h-[500px] bg-[#161b22] rounded-2xl shadow-xl flex flex-col justify-between p-5'
    ):
        ui.label('📄 Instructions').classes('text-2xl font-bold text-white mb-2')

        ui.markdown('''
        1. Click **Start** to begin your interview.  
        2. Speak clearly and stay within frame.  
        3. Your answers will be analyzed for clarity and confidence.
        ''').classes('text-white text-md')

        ui.button('Upload CV').props('color=primary outline').classes('mt-auto')

# --- RUN SERVER ---
ui.run()











