"""SavedCircuitsScreen - Seite mit gespeicherten Zirkeln"""
import json
import os

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

SAVED_CIRCUITS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'saved_circuits.json')


class SavedCircuitsScreen(Screen):
    """Seite mit gespeicherten Zirkeln"""

    def on_pre_enter(self):
        self.load_saved_circuits()

    def load_saved_circuits(self):
        saved = {}
        if os.path.exists(SAVED_CIRCUITS_FILE):
            try:
                with open(SAVED_CIRCUITS_FILE, 'r', encoding='utf-8') as file:
                    saved = json.load(file)
            except (ValueError, OSError, json.JSONDecodeError):
                saved = {}

        container = self.ids.saved_circuits_list
        container.clear_widgets()

        if not saved:
            self.ids.empty_label.opacity = 1
            return

        self.ids.empty_label.opacity = 0
        self.saved_circuits = saved

        for name in sorted(saved.keys()):
            button = Button(
                text=name,
                size_hint_y=None,
                height='50dp',
                background_color=(0.2, 0.6, 0.9, 1)
            )
            button.bind(on_release=lambda btn, selected=name: self.open_saved_circuit_popup(selected))
            container.add_widget(button)

    def open_saved_circuit_popup(self, name):
        circuit = self.saved_circuits.get(name)
        if not circuit:
            return

        content = BoxLayout(orientation='vertical', spacing='10dp', padding='10dp')
        content.add_widget(Label(text=f'Zirkel: {name}', size_hint_y=None, height='30dp'))
        content.add_widget(Label(text=f'Runden: {circuit.get("rounds")}', size_hint_y=None, height='30dp'))
        content.add_widget(Label(text=f'Übungszeit: {circuit.get("exercise_time")} sec', size_hint_y=None, height='30dp'))
        content.add_widget(Label(text=f'Pausenzeit: {circuit.get("pause_time")} sec', size_hint_y=None, height='30dp'))
        content.add_widget(Label(text=f'Vorbereitung: {circuit.get("prep_time")} sec', size_hint_y=None, height='30dp'))
        
        # Zeige die Gesamtdauer
        total_duration = circuit.get('total_duration', '0:00')
        duration_label = Label(
            text=f'Gesamtdauer: {total_duration}',
            size_hint_y=None,
            height='40dp',
            font_size='16sp',
            bold=True,
            color=(0.2, 0.8, 0.2, 1)
        )
        content.add_widget(duration_label)

        button_bar = BoxLayout(size_hint_y=None, height='50dp', spacing='10dp')
        back_button = Button(text='Zurück', background_color=(0.8, 0.2, 0.2, 1))
        select_button = Button(text='Wählen', background_color=(0.2, 0.8, 0.2, 1))
        delete_button = Button(text='Löschen', background_color=(0.9, 0.5, 0.1, 1))

        popup = Popup(
            title='Zirkel auswählen',
            content=content,
            size_hint=(0.95, 0.6),
            auto_dismiss=False
        )

        back_button.bind(on_release=popup.dismiss)
        select_button.bind(on_release=lambda *_: self.select_saved_circuit(name, popup))
        delete_button.bind(on_release=lambda *_: self.delete_saved_circuit(name, popup))

        button_bar.add_widget(back_button)
        button_bar.add_widget(select_button)
        button_bar.add_widget(delete_button)
        content.add_widget(button_bar)

        popup.open()

    def select_saved_circuit(self, name, popup):
        circuit = self.saved_circuits.get(name)
        if not circuit:
            return

        running_screen = self.manager.get_screen('circuit_running')
        running_screen.setup_circuit(
            int(circuit.get('rounds', 0)),
            int(circuit.get('exercise_time', 0)),
            int(circuit.get('pause_time', 0)),
            int(circuit.get('prep_time', 0))
        )
        popup.dismiss()
        self.manager.current = 'circuit_running'

    def delete_saved_circuit(self, name, popup):
        """Löscht einen gespeicherten Zirkel"""
        if name in self.saved_circuits:
            del self.saved_circuits[name]
            
            # Speichern in JSON-Datei
            try:
                with open(SAVED_CIRCUITS_FILE, 'w', encoding='utf-8') as file:
                    json.dump(self.saved_circuits, file, ensure_ascii=False, indent=2)
            except OSError:
                pass
            
            popup.dismiss()
            self.load_saved_circuits()

    def go_back(self):
        """Zurück zur Startseite"""
        self.manager.current = 'home'
