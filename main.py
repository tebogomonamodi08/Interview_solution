from nicegui import ui

ui.add_head_html('''
<style>
  body {
    background: linear-gradient(135deg, #0f111a, #0c0e14);
    color: white;
    font-family: Inter, sans-serif;
    margin: 0; padding: 0;
    scroll-behavior: smooth;
  }
  @keyframes bounce {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(8px); }
  }
  @keyframes float {
      0% { transform: translateY(0px); }
      50% { transform: translateY(-15px); }
      100% { transform: translateY(0px); }
  }

  #footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    background: #0c0e14;
    color: #9ca3af;
    padding: 0.75rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.5);
    transition: opacity 0.3s ease;
    opacity: 0;
    pointer-events: none;
    z-index: 1000;
    font-size: 14px;
  }
  #footer.visible {
    opacity: 1 !important;
    pointer-events: auto !important;
  }

  .image-container {
    position: relative;
    width: 256px;
    max-width: 100%;
  }
  .stars {
    position: absolute;
    top: -20px;
    left: 0;
    width: 100%;
    height: 40px;
    pointer-events: none;
    overflow: visible;
  }
  .star {
    position: absolute;
    background: white;
    border-radius: 50%;
    opacity: 0.8;
    animation: twinkle 2s infinite ease-in-out alternate;
    box-shadow: 0 0 6px 2px rgba(59, 130, 246, 0.6); /* subtle blue glow */
  }
  .star.small { width: 2px; height: 2px; animation-delay: 0s; }
  .star.medium { width: 3px; height: 3px; animation-delay: 1s; }
  .star.large { width: 4px; height: 4px; animation-delay: 0.5s; }

  @keyframes twinkle {
    from { opacity: 0.8; }
    to { opacity: 0.2; }
  }
</style>

<script>
  function scrollToId(id) {
      document.getElementById(id).scrollIntoView({behavior: 'smooth'});
  }

  window.addEventListener('scroll', function() {
    const footer = document.getElementById('footer');
    const hero = document.getElementById('hero');
    if (!footer || !hero) return;
    const heroBottom = hero.getBoundingClientRect().bottom;
    if(heroBottom < 50){
      footer.classList.add('visible');
    } else {
      footer.classList.remove('visible');
    }
  });

  window.addEventListener('load', function() {
    const footer = document.getElementById('footer');
    const hero = document.getElementById('hero');
    if (!footer || !hero) return;
    const heroBottom = hero.getBoundingClientRect().bottom;
    if(heroBottom < 50){
      footer.classList.add('visible');
    } else {
      footer.classList.remove('visible');
    }
  });
</script>
''')

learn_more_dialog = ui.dialog()
with learn_more_dialog:
    with ui.card().classes('backdrop-blur-md bg-white/10 p-6 rounded-xl shadow-lg max-w-md'):
        ui.label('About Cloudy').classes('text-2xl font-bold text-white')
        ui.label(
            "Cloudy is the result of passion, struggle, and relentless pursuit of mastery. "
            "It's built to help you ace your next interview with confidence and AI-powered support."
        ).classes('text-gray-300 mt-2')
        ui.button('Close', on_click=learn_more_dialog.close).classes('mt-4 bg-white/20 text-white rounded-full px-4 py-1 border border-white/30')

with ui.row().classes('flex flex-col md:flex-row items-center justify-between max-w-full mx-0 min-h-screen gap-10').props('id=hero'):

    with ui.column().classes('w-full md:w-5/12 items-start gap-3 text-left').style('padding-left: 24px; max-width: 600px;'):
        ui.label('With').classes('text-5xl font-bold text-white')
        ui.label('CLOUDY') \
            .classes('text-5xl font-bold') \
            .style('background: linear-gradient(90deg, #3b82f6, #9333ea); -webkit-background-clip: text; color: transparent;')
        ui.label('Never fail an interview again') \
            .classes('text-4xl font-bold text-white whitespace-nowrap')

        ui.label('With Cloudy AI, you can ace that next interview with flying colors.') \
            .classes('text-base text-gray-300 mt-2 max-w-md')

        with ui.row().classes('gap-4 mt-6 items-center'):

            ui.button('Get Started', on_click=lambda: ui.run_javascript("scrollToId('features')")) \
                .classes('backdrop-blur bg-white/10 text-white px-6 py-2 rounded-full border border-white/30 shadow-md hover:bg-white/20 transition-all duration-300')

            ui.button('Learn More', on_click=learn_more_dialog.open) \
                .classes('backdrop-blur bg-white/10 text-white px-6 py-2 rounded-full border border-white/30 shadow-md hover:bg-white/20 transition-all duration-300')

            ui.html('''
            <div style="width: 24px; height: 40px; border: 2px solid #3b82f6; border-radius: 12px; display: flex; align-items: center; justify-content: center; animation: bounce 1.5s infinite; margin-left: 8px;">
                <div style="width: 6px; height: 6px; background: #3b82f6; border-radius: 50%;"></div>
            </div>
            ''')

    with ui.column().classes('w-full md:w-5/12 flex justify-end items-center').style('padding-right: 32px; max-width: 600px;'):
        with ui.element('div').classes('image-container'):
            ui.image('https://cdn-icons-png.flaticon.com/512/4712/4712019.png') \
                .classes('w-64 max-w-full rounded-xl shadow-xl') \
                .style('animation: float 6s ease-in-out infinite;')

            with ui.element('div').classes('stars'):
                ui.element('div').classes('star small').style('top: 10px; left: 5%; animation-delay: 0s;')
                ui.element('div').classes('star medium').style('top: 12px; left: 12%; animation-delay: 1s;')
                ui.element('div').classes('star small').style('top: 5px; left: 20%; animation-delay: 0.3s;')
                ui.element('div').classes('star large').style('top: 8px; left: 27%; animation-delay: 1.5s;')
                ui.element('div').classes('star medium').style('top: 12px; left: 33%; animation-delay: 0.7s;')
                ui.element('div').classes('star small').style('top: 15px; left: 40%; animation-delay: 1.2s;')
                ui.element('div').classes('star large').style('top: 6px; left: 48%; animation-delay: 0.6s;')
                ui.element('div').classes('star small').style('top: 10px; left: 55%; animation-delay: 0.1s;')
                ui.element('div').classes('star medium').style('top: 14px; left: 62%; animation-delay: 0.9s;')
                ui.element('div').classes('star small').style('top: 8px; left: 68%; animation-delay: 1.3s;')
                ui.element('div').classes('star large').style('top: 11px; left: 75%; animation-delay: 0.2s;')
                ui.element('div').classes('star medium').style('top: 9px; left: 82%; animation-delay: 1.1s;')
                ui.element('div').classes('star small').style('top: 13px; left: 90%; animation-delay: 0.4s;')
                ui.element('div').classes('star large').style('top: 7px; left: 95%; animation-delay: 1.4s;')
with ui.column().classes('min-h-screen bg-[#0c0e14] text-white items-center justify-center gap-6 px-6 py-24').props('id=features'):

    # === Properly Separated Heading ===
    ui.label('🧠 AI Interview Coach').classes('text-4xl font-bold tracking-tight text-center').style('background: linear-gradient(90deg, #3b82f6, #9333ea); -webkit-background-clip: text; color: transparent;')
    with ui.row().classes('w-full flex-col md:flex-row gap-6 items-center justify-center'):
    
    # === Left Card: Introduction
        with ui.card().classes('bg-white/5 backdrop-blur-md shadow-xl border border-white/10 rounded-2xl p-6 w-full md:w-[48%]'):
            ui.label("🎙️ Record your responses, analyze your tone, and boost your confidence before the big day.").classes('text-base text-gray-300 mb-4 text-center')
            ui.label("Coming soon: real-time transcription and AI coaching powered by FastAPI and Whisper.").classes('text-sm text-gray-500 italic text-center')
            # === Webcam Feed ===
    ui.label("🎥 Webcam Preview").classes('text-xl font-bold text-white mb-4 text-center')
    
    ui.image('http://localhost:8000/video')\
        .classes('rounded-xl w-full h-[280px] object-cover bg-black shadow-lg')\
        .style('border: 2px solid #3b82f6;')

    # === Advice Overlay (Initial hidden) ===
    advice_label = ui.label('🔍 Advice: Try speaking slower for clarity.')\
        .classes('absolute top-4 left-1/2 transform -translate-x-1/2 bg-black/60 text-white text-sm rounded-xl px-4 py-2 shadow-md backdrop-blur-md z-10')\
        .style('visibility: hidden;')

    # === Button to Simulate Advice Display ===
    def show_advice():
        advice_label.set_visibility(True)
        ui.timer(5.0, lambda: advice_label.set_visibility(False), once=True)

    ui.button('Show Advice Overlay', on_click=show_advice)\
        .classes('mt-4 bg-blue-600 text-white px-4 py-2 rounded-xl')

    # === Right Card: Placeholder for Future Features
        with ui.card().classes('bg-white/5 backdrop-blur-md shadow-xl border border-white/10 rounded-2xl p-6 w-full md:w-[48%]'):
            ui.label("👀 Preview your webcam feed, track progress, and stay calm during practice.").classes('text-base text-gray-300 mb-4 text-center')
            ui.label("We'll guide you question by question and give instant, AI-powered feedback.").classes('text-sm text-gray-500 italic text-center')
            ui.label('Your voice, your words, your confidence. Let’s rehearse it right.').classes('text-base text-gray-400 max-w-lg text-center')

with ui.element('footer').props('id=footer').style(
    'display: flex; justify-content: space-between; align-items: center; '
    'padding: 12px 24px; background: #0c0e14; color: #9ca3af; '
    'box-shadow: 0 -2px 10px rgba(0,0,0,0.5); position: fixed; bottom: 0; width: 100%; '
    'opacity: 0; pointer-events: none; transition: opacity 0.3s ease; z-index: 1000; font-size: 14px;'
):
    ui.label('Cloudy AI — Helping you ace interviews © 2025').style('user-select:none;')

    with ui.row().classes('gap-6'):
        ui.icon('fa-brands fa-linkedin').classes('text-2xl').style('color: #3b82f6;')
        ui.icon('fa-solid fa-envelope').classes('text-2xl').style('color: #3b82f6;')
        ui.icon('fa-brands fa-github').classes('text-2xl').style('color: #3b82f6;')

ui.run(title='Cloudy AI')










