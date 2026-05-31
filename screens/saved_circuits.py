"""SavedCircuitsScreen - Seite mit gespeicherten Zirkeln"""
from kivy.uix.screenmanager import Screen


class SavedCircuitsScreen(Screen):
    """Seite mit gespeicherten Zirkeln"""
    
    def go_back(self):
        """Zurück zur Startseite"""
        self.manager.current = 'home'
