"""CircuitSetupScreen - Seite zum Einstellen eines Zirkels"""
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class CircuitSetupScreen(Screen):
    """Seite zum Einstellen/Erstellen eines Zirkels"""
    
    # Properties für die Input-Felder
    rounds = StringProperty('3')
    exercise_time = StringProperty('30')
    pause_time = StringProperty('10')
    prep_time = StringProperty('5')
    
    def start_circuit(self):
        """Starte den Zirkel mit den eingegebenen Werten"""
        try:
            rounds = int(self.ids.rounds_input.text)
            exercise_time = int(self.ids.exercise_time_input.text)
            pause_time = int(self.ids.pause_time_input.text)
            prep_time = int(self.ids.prep_time_input.text)
            
            # Validierung
            if rounds < 1 or exercise_time < 1 or pause_time < 1:
                return
            
            # Speichere die Werte in den Properties
            self.rounds = str(rounds)
            self.exercise_time = str(exercise_time)
            self.pause_time = str(pause_time)
            self.prep_time = str(prep_time)
            
            # Navigiere zum Running-Screen und übergebe die Werte
            running_screen = self.manager.get_screen('circuit_running')
            running_screen.setup_circuit(rounds, exercise_time, pause_time, prep_time)
            self.manager.current = 'circuit_running'
            
        except ValueError:
            pass  # Fehlerhafte Eingabe ignorieren
    
    def go_back(self):
        """Zurück zur Startseite"""
        self.manager.current = 'home'
