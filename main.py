from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle

from agents_module import MasterConsensusEngine
from broker_connector import BrokerConnector

Window.clearcolor = (0.04, 0.04, 0.05, 1)  # Deep Obsidian Black

class StyledCard(BoxLayout):
    def __init__(self, bg_color=(0.08, 0.1, 0.12, 1), **kwargs):
        super().__init__(**kwargs)
        self.padding = 15
        self.spacing = 10
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class TacticalNeuralMatrixApp(App):
    def build(self):
        self.title = "Tactical Neural Matrix v1.0"
        self.engine = MasterConsensusEngine()
        self.broker = BrokerConnector(paper_mode=True)

        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=15)

        # 1. Header Bar
        header = StyledCard(bg_color=(0.06, 0.08, 0.1, 1), size_hint=(1, 0.12))
        title_label = Label(
            text="[b]TACTICAL NEURAL MATRIX[/b]\n[color=00E5FF]11-AGENT CONSENSUS SYSTEM[/color]",
            markup=True,
            font_size='18sp',
            halign='center'
        )
        header.add_widget(title_label)
        main_layout.add_widget(header)

        # 2. Consensus & Agent Dashboard Card
        self.dashboard = StyledCard(bg_color=(0.08, 0.11, 0.14, 1), size_hint=(1, 0.45), orientation='vertical')
        
        self.status_title = Label(
            text="[b]SYSTEM READY[/b]",
            markup=True,
            font_size='20sp',
            color=(0, 1, 0.4, 1)
        )
        self.status_desc = Label(
            text="Press 'SCAN MARKET' to run 11-Agent evaluation...",
            font_size='14sp',
            color=(0.7, 0.8, 0.9, 1),
            halign='center'
        )
        self.dashboard.add_widget(self.status_title)
        self.dashboard.add_widget(self.status_desc)
        main_layout.add_widget(self.dashboard)

        # 3. Interactive Buttons Area
        btn_layout = GridLayout(cols=2, spacing=12, size_hint=(1, 0.25))

        scan_btn = Button(
            text="SCAN MARKET",
            font_size='16sp',
            bold=True,
            background_color=(0, 0.8, 0.9, 1)
        )
        scan_btn.bind(on_press=self.run_market_scan)

        voice_btn = Button(
            text="🎙 VOICE AI",
            font_size='16sp',
            bold=True,
            background_color=(0, 1, 0.5, 1)
        )
        voice_btn.bind(on_press=self.trigger_voice_ai)

        btn_layout.add_widget(scan_btn)
        btn_layout.add_widget(voice_btn)
        main_layout.add_widget(btn_layout)

        return main_layout

    def run_market_scan(self, instance):
        # Simulated live data feed (Liquidity + CHOCH + 1:2 RR)
        data = {
            "structure": "CHOCH_BULLISH",
            "liquidity_swept": True,
            "choch_confirmed": True,
            "rr_ratio": 2.5,
            "stop_loss": 21480.0,
            "target": 21700.0
        }

        res = self.engine.evaluate_market(data)

        if res["decision"] == "BUY":
            order = self.broker.execute_order("NIFTY50", "BUY", 25, res["stop_loss"], res["target"])
            self.status_title.text = f"[b][color=00FF66]BUY SIGNAL ({res['votes']})[/color][/b]"
            self.status_desc.text = f"{res['reason']}\n\n{order['message']}\n{order['details']}"
        elif res["decision"] == "LOCKOUT":
            self.status_title.text = "[b][color=FF3366]SYSTEM LOCKED OUT[/color][/b]"
            self.status_desc.text = res['reason']
        else:
            self.status_title.text = f"[b][color=FFCC00]HOLD ({res['votes']})[/color][/b]"
            self.status_desc.text = res['reason']

    def trigger_voice_ai(self, instance):
        self.status_title.text = "[b][color=00E5FF]VOICE AI LISTENING...[/color][/b]"
        self.status_desc.text = "Voice command active. System ready for trade voice commands."

if __name__ == '__main__':
    TacticalNeuralMatrixApp().run()
