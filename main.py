from nicegui import ui
import asyncio
import random
from datetime import datetime

# === HEAD + JS ===
ui.add_head_html('''
<style>
  body {
    background: linear-gradient(135deg, #0f111a, #0c0e14);
    color: white;
    font-family: Inter, sans-serif;
    margin: 0; padding: 0;
    scroll-behavior: smooth;
  }
  
  /* Animation keyframes */
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
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
  
  @keyframes twinkle {
    from { opacity: 0.8; }
    to { opacity: 0.2; }
  }
  
  /* Layout */
  .interview-section {
    width: 100%;
    padding: 20px 40px;
    margin-top: 0;
  }
  
  .card-container {
    display: flex;
    gap: 20px;
    width: 100%;
    margin-top: 10px;
  }
  
  .interview-card {
    flex: 1;
    min-width: 0;
    background: #1c1f2e;
    border-radius: 12px;
    padding: 20px;
    height: 550px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
  }
  
  /* Progress bars */
  .question-item {
    margin: 4px 0;
  }
  
  .progress-container {
    width: 100%;
    height: 4px;
    background: #131620;
    border-radius: 2px;
    margin-top: 4px;
    overflow: hidden;
  }
  
  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #3b82f6, #9333ea);
    width: 0%;
    transition: width 0.1s linear;
  }
  
  /* Typography */
  .question-text {
    font-size: 12px;
    line-height: 1.3;
    color: #e5e7eb;
  }
  
  .advice-text {
    font-size: 11px;
    color: #9ca3af;
    font-style: italic;
  }
  
  .timer-display {
    font-size: 18px;
    color: #00bfff;
    font-family: monospace;
    font-weight: bold;
  }
  
  .card-header {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 12px;
    text-align: left;
    color: #f3f4f6;
  }
  
  /* Video placeholder */
  .video-placeholder {
    border: 2px solid #3b82f6;
    border-radius: 8px;
    height: 280px;
    width: 100%;
    background-color: #131620;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #9ca3af;
    font-size: 14px;
    margin-bottom: 15px;
  }
  
  /* Buttons */
  .btn {
    border: none;
    border-radius: 9999px;
    padding: 10px 20px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    font-size: 13px;
  }
  
  .btn-primary {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
  }
  
  .btn-warning {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: white;
  }
  
  .btn-danger {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
  }
  
  .btn-secondary {
    background: linear-gradient(135deg, #4b5563, #374151);
    color: white;
  }
  
  .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  /* Transition overlay */
  .transition-overlay {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(28, 31, 46, 0.9);
    backdrop-filter: blur(5px);
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    animation: fadeIn 0.3s ease-out;
  }
  
  .countdown {
    font-size: 24px;
    font-weight: bold;
    color: #3b82f6;
    margin-top: 10px;
  }
  
  /* Loading states */
  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
  }
  
  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(59, 130, 246, 0.2);
    border-top-color: #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 16px;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .loading-text {
    color: #9ca3af;
    font-size: 14px;
  }
  
  /* Results */
  .results-container {
    animation: fadeIn 0.5s ease-out;
  }
  
  .metric {
    margin-bottom: 12px;
  }
  
  .metric-value {
    font-size: 18px;
    font-weight: bold;
    color: #3b82f6;
  }
  
  /* Landing page styles */
  .hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 24px;
  }
  
  .hero-content {
    max-width: 1200px;
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 40px;
  }
  
  .hero-text {
    flex: 1;
    min-width: 300px;
  }
  
  .hero-image {
    flex: 1;
    min-width: 300px;
    position: relative;
  }
  
  .image-container {
    position: relative;
    width: 100%;
    max-width: 100%;
    display: flex;
    justify-content: flex-end;
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
    box-shadow: 0 0 6px 2px rgba(59, 130, 246, 0.6);
  }
  
  .star.small { width: 2px; height: 2px; animation-delay: 0s; }
  .star.medium { width: 3px; height: 3px; animation-delay: 1s; }
  .star.large { width: 4px; height: 4px; animation-delay: 0.5s; }
  
  /* Footer */
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
    footer.classList.toggle('visible', heroBottom < 50);
  });
  
  window.addEventListener('load', function() {
    const footer = document.getElementById('footer');
    const hero = document.getElementById('hero');
    if (!footer || !hero) return;
    const heroBottom = hero.getBoundingClientRect().bottom;
    footer.classList.toggle('visible', heroBottom < 50);
  });
</script>
''')

# === LEARN MORE DIALOG ===
learn_more_dialog = ui.dialog()
with learn_more_dialog:
    with ui.card().classes('backdrop-blur-md bg-white/10 p-6 rounded-xl shadow-lg max-w-md'):
        ui.label('About Cloudy').classes('text-2xl font-bold text-white')
        ui.label(
            "Cloudy is the result of passion, struggle, and relentless pursuit of mastery. "
            "It's built to help you ace your next interview with confidence and AI-powered support."
        ).classes('text-gray-300 mt-2')
        ui.button('Close', on_click=learn_more_dialog.close).classes('mt-4 bg-white/20 text-white rounded-full px-4 py-1 border border-white/30')

# === HERO SECTION ===
with ui.row().classes('hero').props('id=hero'):
    with ui.column().classes('hero-text'):
        ui.label('With').classes('text-5xl font-bold text-white')
        ui.label('CLOUDY')\
            .classes('text-5xl font-bold')\
            .style('background: linear-gradient(90deg, #3b82f6, #9333ea); -webkit-background-clip: text; color: transparent;')
        ui.label('Never fail an interview again').classes('text-4xl font-bold text-white whitespace-nowrap')
        ui.label('With Cloudy AI, you can ace that next interview with flying colors.')\
            .classes('text-base text-gray-300 mt-2 max-w-md')
        with ui.row().classes('gap-4 mt-6 items-center'):
            ui.button('Get Started', on_click=lambda: ui.run_javascript("scrollToId('features')"))\
                .classes('btn btn-primary')
            ui.button('Learn More', on_click=learn_more_dialog.open)\
                .classes('btn btn-secondary')
            ui.html('''
            <div style="width: 24px; height: 40px; border: 2px solid #3b82f6; border-radius: 12px; display: flex; align-items: center; justify-content: center; animation: bounce 1.5s infinite; margin-left: 8px;">
                <div style="width: 6px; height: 6px; background: #3b82f6; border-radius: 50%;"></div>
            </div>
            ''')

    with ui.column().classes('hero-image'):
        with ui.element('div').classes('image-container'):
            ui.image('https://cdn-icons-png.flaticon.com/512/4712/4712019.png')\
                .classes('w-64 max-w-full rounded-xl shadow-xl')\
                .style('animation: float 6s ease-in-out infinite;')
            with ui.element('div').classes('stars'):
                for pos, size, delay in [
                    (5, 'small', 0), (12, 'medium', 1), (20, 'small', 0.3),
                    (27, 'large', 1.5), (33, 'medium', 0.7), (40, 'small', 1.2),
                    (48, 'large', 0.6), (55, 'small', 0.1), (62, 'medium', 0.9),
                    (68, 'small', 1.3), (75, 'large', 0.2), (82, 'medium', 1.1),
                    (90, 'small', 0.4), (95, 'large', 1.4)
                ]:
                    ui.element('div').classes(f'star {size}').style(f'top: 10px; left: {pos}%; animation-delay: {delay}s;')

# === FEATURES SECTION ===
with ui.column().classes('w-full min-h-screen bg-[#0c0e14] text-white gap-8 px-4 py-12 items-center').props('id=features'):
    ui.label('🧠 AI Interview Coach')\
        .classes('text-4xl font-bold tracking-tight text-center mb-4')\
        .style('background: linear-gradient(90deg, #3b82f6, #9333ea); -webkit-background-clip: text; color: transparent;')
    
    container = ui.row().classes('card-container')

# === App State ===
class AppState:
    current_state = "idle"
    questions = []
    current_question_index = 0
    advice_messages = [
        "Breath in, you've got this!",
        "Relax and speak clearly",
        "You're doing great!",
        "Take a moment to think",
        "Confidence is key!"
    ]

# === Video Card (Left Card) ===
class VideoCard:
    def __init__(self, container):
        self.container = container
        self.card = None
        self.start_btn = None
        self.pause_btn = None
        self.stop_btn = None
        self.setup()
    
    def setup(self):
        with self.container:
            with ui.card().classes('interview-card') as self.card:
                ui.label("🎥 See Yourself — Speak with Confidence").classes('card-header')
                
                with ui.element('div').classes('video-placeholder'):
                    ui.label('Video feed will appear here')
                
                self.start_btn = ui.button('Start Interview', on_click=lambda: app.start_interview()).classes('btn btn-primary')
                self.start_btn.disable()

                with ui.row().classes('gap-2 mt-2 justify-center'):
                    self.pause_btn = ui.button('Pause', on_click=lambda: app.pause_interview()).classes('btn btn-warning')
                    self.pause_btn.visible = False
                    self.stop_btn = ui.button('Stop', on_click=lambda: app.stop_interview()).classes('btn btn-danger')
                    self.stop_btn.visible = False

    def enable_start_button(self):
        self.start_btn.enable()
        self.start_btn.visible = True
        self.pause_btn.visible = False
        self.stop_btn.visible = False

# === Questions Card (Right Card) ===
class QuestionsCard:
    def __init__(self, container):
        self.container = container
        self.card = None
        self.timer_display = None
        self.progress_bars = []
        self.advice_labels = []
        self.time_remaining = 300
        self.timer_task = None
        self.transition_overlay = None
        self.generate_btn = None
        self.upload_btn = None
        self.setup()
        
    def setup(self):
        with self.container:
            with ui.card().classes('interview-card') as self.card:
                self.show_initial_state()
    
    async def show_loading(self, message="Generating questions..."):
        with self.card:
            self.card.clear()
            with ui.column().classes('loading-container'):
                ui.spinner(size='lg').classes('loading-spinner')
                ui.label(message).classes('loading-text')
        await asyncio.sleep(1.5)
        
    async def show_questions(self):
        with self.card:
            self.card.clear()
            with ui.column():
                with ui.row().classes('justify-between items-center w-full'):
                    ui.label('AI Interview Questions').classes('card-header')
                    self.timer_display = ui.label('05:00').classes('timer-display')
                
                AppState.questions = random.sample([
                    'Tell me about yourself in 1 minutes.',
                    'What are your key strengths for this role?',
                    'Describe a professional challenge you overcame.',
                    'Why are you interested in this position?',
                    'Where do you see your career in 3 years?'
                ], 5)
                
                self.progress_bars = []
                self.advice_labels = []
                for q in AppState.questions:
                    with ui.column().classes('question-item'):
                        ui.label(q).classes('question-text')
                        with ui.element('div').classes('progress-container'):
                            bar = ui.element('div').classes('progress-fill')
                            bar.style('width: 0%')
                        self.progress_bars.append(bar)
                        advice = ui.label("").classes('advice-text')
                        self.advice_labels.append(advice)
    
    async def show_transition(self, advice):
        self.transition_overlay = ui.element('div').classes('transition-overlay')
        with self.transition_overlay:
            ui.label(advice).classes('text-center text-lg')
            countdown = ui.label("").classes('countdown')
            
            for i in range(10, 0, -1):
                countdown.text = f"Next question in: {i}s"
                if i <= 3:
                    countdown.style('color: #ef4444; animation: pulse 0.5s infinite')
                await asyncio.sleep(1)
            
            countdown.text = "Starting next question..."
            await asyncio.sleep(0.5)
        
        self.transition_overlay.delete()
        self.transition_overlay = None
    
    async def start_interview(self):
        AppState.current_state = "interviewing" #Change the start of the right card to interviewing
        self.time_remaining = 300 #set an initial timer 5 minutes
        
        self.timer_task = asyncio.create_task(self.run_timer())
        
        for i, (bar, advice_label) in enumerate(zip(self.progress_bars, self.advice_labels)):
            if i > 0:
                advice = random.choice(AppState.advice_messages)
                await self.show_transition(advice)
            
            with self.card:
                advice_label.text = advice if i > 0 else random.choice(AppState.advice_messages)
            
            with self.card:
                bar.style('width: 0%')
                for t in range(60):
                    if AppState.current_state != "interviewing":
                        return
                    await asyncio.sleep(1)
                    progress = (t + 1) / 60 * 100
                    bar.style(f'width: {progress}%')
    
    async def run_timer(self):
        while self.time_remaining > 0 and AppState.current_state == "interviewing":
            await asyncio.sleep(1)
            self.time_remaining -= 1
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60
            if self.timer_display:
                self.timer_display.text = f'{minutes:02d}:{seconds:02d}'
        
        if self.time_remaining <= 0:
            await self.show_loading("Analyzing your responses...")
            await self.show_results()

    async def show_results(self):
        AppState.current_state = "results"
        with self.card:
            self.card.clear()
            with ui.column().classes('results-container'):
                ui.label('Interview Results').classes('card-header')
                
                with ui.column():
                    with ui.row().classes('metric items-center gap-4'):
                        ui.label('Filler Words:').classes('text-gray-400')
                        ui.label(str(random.randint(5, 15))).classes('metric-value')
                    
                    with ui.row().classes('metric items-center gap-4'):
                        ui.label('Clarity Score:').classes('text-gray-400')
                        ui.label(f"{random.randint(70, 95)}/100").classes('metric-value')
                    
                    with ui.row().classes('metric items-center gap-4'):
                        ui.label('Overall Score:').classes('text-gray-400')
                        ui.label(f"{random.randint(75, 97)}/100").classes('metric-value')
                    
                    ui.label("Great job! With practice, you'll ace the real interview.")\
                        .classes('text-center mt-6 text-gray-300')
                    
                    ui.button('Start New Interview', on_click=self.reset)\
                        .classes('btn btn-primary mt-6')

    def reset(self):
        AppState.current_state = "idle"
        self.show_initial_state()

    async def mock_upload_questions(self):
        AppState.current_state = "loading"
        await self.show_loading("Loading uploaded questions...")
        await self.show_questions()
        AppState.current_state = "ready"
        return True

    def show_initial_state(self):
        with self.card:
            self.card.clear()
            with ui.column():
                ui.label('Interview Preparation').classes('card-header')
                
                with ui.column().classes('gap-2 mb-6'):
                    ui.label('Get ready for your interview:').classes('font-medium text-gray-300')
                    ui.label('1. Click "Generate Questions" to get started').classes('text-sm text-gray-400')
                    ui.label('2. Prepare your webcam and microphone').classes('text-sm text-gray-400')
                    ui.label('3. Click "Start Interview" when ready').classes('text-sm text-gray-400')
                    ui.label('4. Answer each question within 1 minute').classes('text-sm text-gray-400')
                    ui.label('5. Review your performance at the end').classes('text-sm text-gray-400')
                
                with ui.row().classes('justify-center gap-4'):
                    self.generate_btn = ui.button('Generate Questions', on_click=self.generate_questions).classes('btn btn-primary')
                    self.upload_btn = ui.button('Upload Questions', on_click=self.mock_upload_questions).classes('btn btn-secondary')

    async def generate_questions(self):
        AppState.current_state = "loading"
        await self.show_loading()
        await self.show_questions()
        AppState.current_state = "ready"
        app.video_card.enable_start_button()

# === Main App ===
class InterviewApp:
    def __init__(self):
        self.container = container
        self.video_card = VideoCard(self.container)
        self.questions_card = QuestionsCard(self.container)
    
    async def start_interview(self):
        self.video_card.start_btn.visible = False
        self.video_card.pause_btn.visible = True
        self.video_card.stop_btn.visible = True
        ui.notify('Interview started 🎤', color='positive')
        await self.questions_card.start_interview()
    
    async def pause_interview(self):
        paused = self.video_card.pause_btn.text == "Pause"
        self.video_card.pause_btn.text = "Resume" if paused else "Pause"
        ui.notify(f'Interview {"⏸️ Paused" if paused else "▶️ Resumed"}', color='warning')
        
        if paused:
            AppState.current_state = "paused"
        else:
            AppState.current_state = "interviewing"
            await self.questions_card.start_interview()
    
    def stop_interview(self):
        self.video_card.start_btn.visible = True
        self.video_card.pause_btn.visible = False
        self.video_card.stop_btn.visible = False
        self.video_card.pause_btn.text = "Pause"
        ui.notify('Interview cancelled ⛔', color='negative')
        AppState.current_state = "idle"
        self.questions_card.reset()
        self.video_card.start_btn.disable()

# Create and setup the app
app = InterviewApp()

# === FOOTER ===
with ui.element('footer').props('id=footer'):
    ui.label('Cloudy AI — Helping you ace interviews © 2025').classes('text-sm')
    with ui.row().classes('gap-4'):
        ui.icon('fa-brands fa-linkedin').classes('text-xl text-blue-400 hover:text-blue-300 cursor-pointer')
        ui.icon('fa-solid fa-envelope').classes('text-xl text-blue-400 hover:text-blue-300 cursor-pointer')
        ui.icon('fa-brands fa-github').classes('text-xl text-blue-400 hover:text-blue-300 cursor-pointer')

ui.run(title='Cloudy AI')