"""CircuitRunningScreen - Seite zur Ausführung eines Zirkels"""
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
from sound_util import sound_player


class CircuitRunningScreen(Screen):
    """Seite zur Ausführung/Anzeige des laufenden Zirkels"""
    
    # Properties für die Anzeige
    rounds = NumericProperty(0)
    exercise_time = NumericProperty(0)
    pause_time = NumericProperty(0)
    prep_time = NumericProperty(0)
    
    current_round = NumericProperty(0)
    time_remaining = NumericProperty(0)
    current_phase = StringProperty('Übung')  # 'Übung' oder 'Pause'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer_event = None
        self.last_beep_time = None  # Track für letzte 5 Sekunden Warnton
    
    def setup_circuit(self, rounds, exercise_time, pause_time, prep_time=0):
        """Konfiguriere den Zirkel mit den Werten (inkl. Vorbereitungszeit)"""
        self.rounds = rounds
        self.exercise_time = exercise_time
        self.pause_time = pause_time
        self.prep_time = prep_time
        self.current_round = 1
        if prep_time and prep_time > 0:
            self.current_phase = 'Vorbereitung'
            self.time_remaining = prep_time
        else:
            self.current_phase = 'Übung'
            self.time_remaining = exercise_time
        self.last_beep_time = None
    
    def start_timer(self):
        """Starte den Timer"""
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
        # Wenn wir direkt in die Übung starten, spiele Start-Signal
        if self.current_phase == 'Übung':
            sound_player.play_session_start()
    
    def update_timer(self, dt):
        """Aktualisiere den Timer"""
        self.time_remaining -= 1
        
        # Warnton für letzte 5 Sekunden
        if self.time_remaining <= 5 and self.time_remaining > 0:
            if self.last_beep_time != self.time_remaining:
                sound_player.play_warning_beep()
                self.last_beep_time = self.time_remaining
        
        # Zeit vorbei
        if self.time_remaining <= 0:
            # Wenn Vorbereitung vorbei -> Starte Zirkel (Signal) und gehe zu Übung
            if self.current_phase == 'Vorbereitung':
                sound_player.play_session_start()
                self.current_phase = 'Übung'
                self.time_remaining = self.exercise_time
                self.last_beep_time = None
                return

            sound_player.play_finish_beep()
            self.next_phase()
    
    def next_phase(self):
        """Wechsle zur nächsten Phase"""
        if self.current_phase == 'Übung':
            # Wenn dies die letzte Runde ist, beende den Zirkel (keine abschließende Pause)
            if self.current_round >= self.rounds:
                self.finish_circuit()
                return
            # Wechsle zur Pause
            self.current_phase = 'Pause'
            self.time_remaining = self.pause_time
            self.last_beep_time = None
        else:
            # Wechsle zur nächsten Runde
            if self.current_round < self.rounds:
                self.current_round += 1
                self.current_phase = 'Übung'
                self.time_remaining = self.exercise_time
                self.last_beep_time = None
            else:
                # Zirkel fertig
                self.finish_circuit()
    
    def finish_circuit(self):
        """Beende den Zirkel"""
        if self.timer_event:
            self.timer_event.cancel()
        self.manager.current = 'home'
    
    def stop_circuit(self):
        """Stoppe den Zirkel"""
        if self.timer_event:
            self.timer_event.cancel()
        self.manager.current = 'home'
    
    def on_leave(self):
        """Wenn den Screen verlassen wird, stoppe den Timer"""
        if self.timer_event:
            self.timer_event.cancel()
