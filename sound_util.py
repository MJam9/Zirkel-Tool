"""Sound Utility für Zirkel-Tool - Piep-Töne für Timer"""
import numpy as np
import io
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

import wave


class SoundPlayer:
    """Klasse zum Erzeugen und Abspielen von Tönen"""
    
    def __init__(self):
        self.initialized = False
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
                self.initialized = True
            except:
                pass
    
    @staticmethod
    def generate_tone(frequency, duration, sample_rate=22050):
        """
        Generiere einen Sinuswellen-Ton
        
        Args:
            frequency: Frequenz in Hz
            duration: Dauer in Sekunden
            sample_rate: Sample-Rate in Hz
        
        Returns:
            numpy array mit dem Audio-Signal
        """
        samples = int(duration * sample_rate)
        t = np.linspace(0, duration, samples)
        # Sinuswelle generieren
        wave_data = np.sin(2 * np.pi * frequency * t)
        # Normalisieren auf 16-bit
        wave_data = np.int16(wave_data * 32767 * 0.8)
        return wave_data, sample_rate

    @staticmethod
    def generate_sweep_tone(start_freq, end_freq, duration, sample_rate=22050):
        """
        Generiere einen linear ansteigenden oder abfallenden Frequenz-Sweep

        Args:
            start_freq: Startfrequenz in Hz
            end_freq: Endfrequenz in Hz
            duration: Dauer in Sekunden
            sample_rate: Sample-Rate in Hz

        Returns:
            numpy array mit dem Audio-Signal
        """
        samples = int(duration * sample_rate)
        t = np.linspace(0, duration, samples)
        freqs = np.linspace(start_freq, end_freq, samples)
        wave_data = np.sin(2 * np.pi * freqs * t)
        wave_data = np.int16(wave_data * 32767 * 0.85)
        return wave_data, sample_rate
    
    @staticmethod
    def create_wav_from_array(wave_data, sample_rate):
        """Konvertiere Numpy Array zu WAV Bytes"""
        # Stereo: dupiziere die Daten für beide Kanäle
        stereo_data = np.zeros((len(wave_data), 2), dtype=np.int16)
        stereo_data[:, 0] = wave_data
        stereo_data[:, 1] = wave_data
        
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(2)  # Stereo
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(stereo_data.tobytes())
        
        wav_buffer.seek(0)
        return wav_buffer
    
    def play_tone(self, frequency, duration):
        """Spiele einen Ton ab"""
        if not PYGAME_AVAILABLE or not self.initialized:
            return
        
        try:
            wave_data, sample_rate = self.generate_tone(frequency, duration)
            wav_buffer = self.create_wav_from_array(wave_data, sample_rate)
            
            sound = pygame.mixer.Sound(wav_buffer)
            sound.play()
        except Exception as e:
            print(f"Fehler beim Abspielen des Tons: {e}")
    
    def play_warning_beep(self):
        """Spiele einen Warnton ab (für letzte 5 Sekunden)"""
        # Hoher Ton (1000 Hz) kurz
        self.play_tone(frequency=1000, duration=0.15)
    
    def play_finish_beep(self):
        """Spiele einen Abschluss-Ton ab (Zeit vorbei)"""
        # Doppel-Piep als Abschluss-Signal, deutlich anders als die 5s-Warntöne (1000 Hz)
        try:
            sample_rate = 22050
            # erster kurzer Pie (höher)
            tone1, _ = self.generate_tone(frequency=1600, duration=0.12, sample_rate=sample_rate)
            # kleiner Abstand (Stille)
            silence = np.zeros(int(0.06 * sample_rate), dtype=np.int16)
            # zweiter Pie (noch höher)
            tone2, _ = self.generate_tone(frequency=2200, duration=0.16, sample_rate=sample_rate)

            combined = np.concatenate([tone1, silence, tone2])
            wav_buffer = self.create_wav_from_array(combined, sample_rate)
            sound = pygame.mixer.Sound(wav_buffer)
            sound.play()
        except Exception as e:
            print(f"Fehler beim Abspielen des Abschluss-Tons: {e}")

    def play_session_start(self):
        """Spiele das Start-Signal für einen ganzen Zirkel (gleiches Signal wie Ende)"""
        # Doppel-Piep, weniger hell/hoch als das Abschluss-Signal
        try:
            sample_rate = 22050
            # erster milder Pie
            tone1, _ = self.generate_tone(frequency=1200, duration=0.12, sample_rate=sample_rate)
            silence = np.zeros(int(0.06 * sample_rate), dtype=np.int16)
            # zweiter etwas höherer Pie
            tone2, _ = self.generate_tone(frequency=1800, duration=0.14, sample_rate=sample_rate)

            combined = np.concatenate([tone1, silence, tone2])
            # etwas leiser/angenehmer machen
            combined = (combined.astype(np.int32) * 0.7).astype(np.int16)

            wav_buffer = self.create_wav_from_array(combined, sample_rate)
            sound = pygame.mixer.Sound(wav_buffer)
            sound.play()
        except Exception as e:
            print(f"Fehler beim Abspielen des Start-Tons: {e}")

    def play_session_end(self):
        """Spiele das End-Signal für einen ganzen Zirkel (gleiches Signal wie Start)"""
        # Verwende exakt das gleiche Signal wie beim Start
        self.play_session_start()


# Globale Instanz
sound_player = SoundPlayer()
