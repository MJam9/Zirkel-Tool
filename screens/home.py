"""HomeScreen - Startseite der Zirkel-Tool"""
from kivy.uix.screenmanager import Screen


class HomeScreen(Screen):
    """Startseite mit Navigation zu den anderen Screens"""
    
    def go_to_setup(self):
        """Wechsle zur Seite 'Zirkel einstellen'"""
        self.manager.current = 'circuit_setup'
    
    def go_to_saved(self):
        """Wechsle zur Seite 'Gespeicherte Zirkel'"""
        self.manager.current = 'saved_circuits'
