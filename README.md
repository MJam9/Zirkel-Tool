# Zirkel-Tool für Sportstunden

Eine mobile App zum Erstellen und Verwalten von Trainingszirkeln für deine  nächste Sportstunden. Zirkel können individuell konfiguriert, für die spätere Verwendung gespeichert und direkt gestartet werden.

<img width="216" height="444" alt="Zirkel-Startscreen" src="https://github.com/user-attachments/assets/0b3df26b-2a0d-444b-8ace-d59182ab8d60" />

## Funktionen

- **Flexibles Setup**: Konfiguriere Rundenanzahl, Übungszeit, Pausen und Vorbereitungszeit individuell.
- **Live-Timer**: Übersichtliche Anzeige der aktuellen Phase (Übung, Pause oder Vorbereitung) inklusive akustischer Signale.
- **Speicherverwaltung**: Benenne deine Zirkel und speichere sie dauerhaft ab.
- **Schnellstart**: Greife auf eine Liste gespeicherter Zirkel zu, um sofort mit dem Training zu beginnen.

## Installation 
Die Anwendung kann plattformübergreifend genutzt werden: auf dem PC (Windows/Linux/macOS) oder auf Android-Geräten (z. B. via PyDroid 3).

### Voraussetzungen
Stelle sicher, dass Python installiert ist, und installiere die benötigten Abhängigkeiten:

```bash
pip install kivy pygame numpy
```

## Verwendung

- **Startseite**: Nutze die Hauptnavigation, um entweder einen neuen Zirkel zu erstellen oder deine Bibliothek zu öffnen.
- **Zirkel einstellen**: Gib die gewünschten Zeiten ein. Die Gesamtdauer wird dir automatisch berechnet. Du kannst den Zirkel direkt starten oder für später speichern.
- **Zirkel starten**: Während der Zirkel läuft, führt dich die App durch die Phasen. Akustische Signale kündigen das Ende einer Phase oder die letzten Sekunden an.
  
<img width="216" height="444" alt="ZirkeLaufScreen" src="https://github.com/user-attachments/assets/f770c922-7fd5-4889-8ec8-dcd36b35e1c5" />


- **Gespeicherte Zirkel**: Verwalte deine Vorlagen. Hier kannst du gespeicherte Zirkel laden oder nicht mehr benötigte Einträge löschen.
  
<img width="216" height="444" alt="ZirkelAuswahlScreen" src="https://github.com/user-attachments/assets/36e93420-3a9f-4c39-952b-15379ec89d93" />


