from nicegui import ui
import asyncio
import random

# --- GLOBAL STYLING ---
ui.query('body').classes('bg-[#0d1117] text-white')
ui.add_head_html('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>')

# --- QUESTIONS ---
questions = [
    "What inspired you to pursue your career?",
    "Describe a challenging project you overcame.",
    "Where do you see yourself in 5 years?",
    "How do you handle feedback?",
    "Why are you the ideal candidate?"
]

# --- MOTIVATION MESSAGES ---
motivation_messages = [
    "🌟 You got this!",
    "💨 Breathe in, breathe out.",
    "⭐ You are a star!"
]

# --- UI ELEMENT HOLDERS ---
progress_bars = []
transition_label = None
beep_indicator = None
start_btn = None
cancel_btn = None
instruction_column = None
question_column = None

def build_question_column():
    global question_column, transition_label, progress_bars
    question_column.clear()
    progress_bars.clear()

    with question_column:
        ui.label('📝 Questions').classes('text-xl font-bold text-white pb-2')

        for q in questions:
            with ui.column().classes('w-full max-w-[500px] gap-1 items-start'):
                ui.label(q).classes('text-sm font-bold text-white text-left')
                with ui.element('div').classes(
                    'w-full h-[32px] bg-gray-700 rounded overflow-hidden relative'
                ).style('position: relative') as bar_container:
                    bar_fill = ui.element('div').classes(
                        'h-full transition-all ease-linear'
                    ).style('width: 0%; position: absolute; top: 0; left: 0; background-color: #30a14e; visibility: hidden')
                    progress_bars.append(bar_fill)

        transition_label = ui.label('').classes('text-sm font-bold text-gray-300 pt-4 opacity-0 text-center')

def reset_flow():
    global transition_label
    for bar in progress_bars:
        bar.style('width: 0%')
        bar.style('visibility: hidden')

    question_column.set_visibility(False)
    instruction_column.set_visibility(True)
    transition_label.text = ''
    transition_label.classes('opacity-0')
    beep_indicator.set_visibility(False)

    # Reset start button styling
    start_btn.text = 'Start'
    start_btn.classes('text-white')
    start_btn.props('outline color=primary')

    build_question_column()  # Fully rebuild question UI

# --- HEADER ---
with ui.column().classes('items-center pt-6 pb-2 mb-3'):
    ui.label('🧠 AI Interview Assistant').classes('text-4xl font-bold text-white tracking-wide')

# --- MAIN LAYOUT ---
with ui.row().classes('flex flex-row w-full min-h-screen px-4 pb-4 gap-4 bg-[#0d1117]'):

    # --- LEFT PANEL ---
    with ui.card().classes('flex-1 h-[480px] bg-[#161b22] rounded-2xl shadow-xl flex flex-col justify-between p-4 m-0'):
        ui.label('🎥 Webcam Stream').classes('text-xl font-bold text-white')
        ui.image('http://localhost:8000/video').classes('rounded-xl w-full h-[280px] object-cover bg-black')

        beep_indicator = ui.label('🔴 Interview Starting...').classes(
            'text-sm font-bold text-red-400 animate__animated animate__flash animate__infinite'
        ).style('text-align: center')
        beep_indicator.set_visibility(False)

        with ui.row().classes('justify-center gap-4 mt-4'):
            start_btn = ui.button(icon='play_arrow', text='Start').props('outline color=primary').classes('text-white')
            cancel_btn = ui.button(icon='close', text='Cancel').props('outline color=red').classes('text-white')

            async def on_click(btn):
                start_btn.text = 'Interview Running'
                start_btn.classes('bg-green-600 text-white font-bold')
                start_btn.props(remove='outline color=primary')

                beep_indicator.set_visibility(True)
                await asyncio.sleep(3)
                beep_indicator.set_visibility(False)

                instruction_column.classes('animate__fadeOut')
                await asyncio.sleep(0.8)
                instruction_column.set_visibility(False)
                question_column.set_visibility(True)

                for i in range(len(progress_bars)):
                    msg = random.choice(motivation_messages)
                    transition_label.text = msg
                    transition_label.classes(remove='opacity-0')
                    await asyncio.sleep(6)

                    for count in ["3...", "2...", "1...", "Ready...Go!"]:
                        transition_label.text = count
                        await asyncio.sleep(1)

                    transition_label.classes('opacity-0')

                    bar_fill = progress_bars[i]
                    bar_fill.style('visibility: visible')
                    for j in range(51):
                        percent = min(2 * j, 100)
                        bar_fill.style(f'width: {percent}%')
                        await asyncio.sleep(0.1)

                # Reset button at end
                start_btn.text = 'Start'
                start_btn.classes('text-white')
                start_btn.props('outline color=primary')

            start_btn.on('click', lambda e: on_click(start_btn))
            cancel_btn.on('click', lambda e: reset_flow())

    # --- RIGHT PANEL ---
    with ui.card().classes('flex-1 h-[480px] bg-[#161b22] rounded-2xl shadow-xl p-4 overflow-y-auto m-0'):

        instruction_column = ui.column().classes('animate__animated animate__fadeIn')
        instruction_column.set_visibility(True)

        with instruction_column:
            ui.label('📄 Instructions').classes('text-xl font-bold text-white mb-2')
            ui.markdown('''
            1. Click **Start** to begin your interview  
            2. Speak clearly and stay within frame  
            3. Your answers will be analyzed for clarity and confidence
            ''').classes('text-white text-sm')
            ui.button('Upload CV').props('color=primary outline').classes('mt-2')

        question_column = ui.column().classes('hidden gap-4 w-full justify-start items-center pt-2')
        question_column.set_visibility(False)

        build_question_column()  # Initial build

# --- START APP ---
ui.run()












