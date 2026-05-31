"""CircuitSetupScreen - Seite zum Einstellen eines Zirkels"""
import json
import os

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty

SAVED_CIRCUITS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'saved_circuits.json')


class CircuitSetupScreen(Screen):
    """Seite zum Einstellen/Erstellen eines Zirkels"""
    
    # Properties für die Input-Felder
    rounds = StringProperty('3')
    exercise_time = StringProperty('30')
    pause_time = StringProperty('10')
    prep_time = StringProperty('5')

    def get_settings_data(self):
        rounds = int(self.ids.rounds_input.text)
        exercise_time = int(self.ids.exercise_time_input.text)
        pause_time = int(self.ids.pause_time_input.text)
        prep_time = int(self.ids.prep_time_input.text)

        if rounds < 1 or exercise_time < 1 or pause_time < 1:
            raise ValueError('Ungültige Werte')

        return {
            'rounds': rounds,
            'exercise_time': exercise_time,
            'pause_time': pause_time,
            'prep_time': prep_time,
        }

    def open_save_popup(self):
        """Öffne ein Popup zur Namenseingabe für das Speichern."""
        content = BoxLayout(orientation='vertical', spacing='10dp', padding='10dp')
        name_input = TextInput(
            hint_text='Name für den Zirkel',
            multiline=False,
            size_hint_y=None,
            height='40dp'
        )
        button_bar = BoxLayout(size_hint_y=None, height='40dp', spacing='10dp')

        cancel_button = Button(text='Abbrechen', background_color=(0.8, 0.2, 0.2, 1))
        save_button = Button(text='Speichern', background_color=(0.2, 0.5, 0.9, 1))

        popup = Popup(
            title='Zirkel speichern',
            content=content,
            size_hint=(0.9, 0.4),
            auto_dismiss=False
        )

        cancel_button.bind(on_release=popup.dismiss)
        save_button.bind(on_release=lambda *_: self._save_named_circuit(name_input.text, popup))

        content.add_widget(Label(text='Gib einen Namen für diesen Zirkel ein:'))
        content.add_widget(name_input)
        button_bar.add_widget(cancel_button)
        button_bar.add_widget(save_button)
        content.add_widget(button_bar)

        popup.open()

    def _save_named_circuit(self, name, popup):
        """Speichere den Zirkel unter dem angegebenen Namen."""
        if not name or not name.strip():
            return

        try:
            settings = self.get_settings_data()
            self.save_circuit_by_name(name.strip(), settings)
            popup.dismiss()
        except ValueError:
            pass

    def save_circuit_by_name(self, name, settings):
        """Schreibe den benannten Zirkel in die JSON-Datei."""
        saved = {}
        if os.path.exists(SAVED_CIRCUITS_FILE):
            try:
                with open(SAVED_CIRCUITS_FILE, 'r', encoding='utf-8') as file:
                    saved = json.load(file)
            except (ValueError, OSError, json.JSONDecodeError):
                saved = {}

        saved[name] = settings

        with open(SAVED_CIRCUITS_FILE, 'w', encoding='utf-8') as file:
            json.dump(saved, file, indent=2, ensure_ascii=False)

        self.rounds = str(settings['rounds'])
        self.exercise_time = str(settings['exercise_time'])
        self.pause_time = str(settings['pause_time'])
        self.prep_time = str(settings['prep_time'])

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
