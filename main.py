"""
Zirkel-Tool für Sportstunden
Hauptdatei für die App-Verwaltung
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder
import os

from screens import HomeScreen, CircuitSetupScreen, CircuitRunningScreen, SavedCircuitsScreen

# .kv-Dateien laden
Builder.load_file(os.path.join(os.path.dirname(__file__), 'screens', 'homescreen.kv'))
Builder.load_file(os.path.join(os.path.dirname(__file__), 'screens', 'circuitsetupscreen.kv'))
Builder.load_file(os.path.join(os.path.dirname(__file__), 'screens', 'circuitrunningscreen.kv'))
Builder.load_file(os.path.join(os.path.dirname(__file__), 'screens', 'savedcircuitsscreen.kv'))

# Kivy Config für automatische Skalierung
Config.set('graphics', 'multisampling', True)
Config.set('graphics', 'fullscreen', 'auto')

# Fensstergröße nur für Desktop-Tests setzen (nicht auf echtem Handy)
if os.name == 'nt':  # Windows/Desktop
    Window.size = (360, 640)


class ZirkelApp(App):
    """Hauptanwendung für das Zirkel-Tool"""
    
    def build(self):
        """Baue die App mit ScreenManager"""
        # ScreenManager für die Navigation zwischen Seiten
        sm = ScreenManager()
        
        # Alle Screens registrieren
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CircuitSetupScreen(name='circuit_setup'))
        sm.add_widget(CircuitRunningScreen(name='circuit_running'))
        sm.add_widget(SavedCircuitsScreen(name='saved_circuits'))
        
        return sm


if __name__ == '__main__':
    ZirkelApp().run()
