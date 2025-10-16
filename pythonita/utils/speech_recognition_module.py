"""
Modulo Speech-to-Text per comandi vocali.
Supporta Google Speech Recognition, Sphinx, e altri engine.
"""

import speech_recognition as sr
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class SpeechRecognizer:
    """
    Gestore riconoscimento vocale.
    Registra audio e lo converte in testo.
    """
    
    def __init__(self, language='it-IT', engine='google'):
        """
        Inizializza riconoscitore vocale.
        
        Args:
            language: Codice lingua (it-IT, en-US, etc.)
            engine: Engine riconoscimento ('google', 'sphinx', 'wit', 'bing')
        """
        self.recognizer = sr.Recognizer()
        self.language = language
        self.engine = engine
        
        # Configurazione ottimale per italiano
        self.recognizer.energy_threshold = 4000  # Soglia rumore
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8  # Pausa tra parole (secondi)
        
        logger.info(f"Speech recognizer initialized: {engine}, language={language}")
    
    def listen_from_microphone(self, timeout=5, phrase_time_limit=10) -> Tuple[bool, str]:
        """
        Ascolta da microfono e converte in testo.
        
        Args:
            timeout: Secondi di attesa prima del timeout
            phrase_time_limit: Durata massima frase
            
        Returns:
            (success, text): True/False, testo riconosciuto o messaggio errore
        """
        try:
            with sr.Microphone() as source:
                logger.info("Listening from microphone...")
                
                # Calibrazione automatica rumore ambiente
                logger.info("Calibrating ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Ascolto
                logger.info("Listening for speech...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
                
                # Riconoscimento
                logger.info(f"Recognizing with {self.engine}...")
                text = self._recognize_audio(audio)
                
                if text:
                    logger.info(f"Recognized: {text}")
                    return True, text
                else:
                    return False, "Nessun testo riconosciuto"
                    
        except sr.WaitTimeoutError:
            logger.warning("Listening timeout")
            return False, "Timeout: nessun audio rilevato"
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return False, "Audio non comprensibile"
        except sr.RequestError as e:
            logger.error(f"Recognition service error: {e}")
            return False, f"Errore servizio riconoscimento: {e}"
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False, f"Errore imprevisto: {e}"
    
    def recognize_from_file(self, audio_file_path: str) -> Tuple[bool, str]:
        """
        Riconosce audio da file.
        
        Args:
            audio_file_path: Path file audio (WAV, FLAC, etc.)
            
        Returns:
            (success, text): True/False, testo riconosciuto o messaggio errore
        """
        try:
            with sr.AudioFile(audio_file_path) as source:
                logger.info(f"Loading audio from {audio_file_path}")
                audio = self.recognizer.record(source)
                
                logger.info(f"Recognizing with {self.engine}...")
                text = self._recognize_audio(audio)
                
                if text:
                    logger.info(f"Recognized: {text}")
                    return True, text
                else:
                    return False, "Nessun testo riconosciuto"
                    
        except Exception as e:
            logger.error(f"Error recognizing from file: {e}")
            return False, f"Errore: {e}"
    
    def _recognize_audio(self, audio) -> Optional[str]:
        """
        Riconosce audio con engine selezionato.
        
        Args:
            audio: AudioData
            
        Returns:
            Testo riconosciuto o None
        """
        try:
            if self.engine == 'google':
                return self.recognizer.recognize_google(audio, language=self.language)
            elif self.engine == 'sphinx':
                return self.recognizer.recognize_sphinx(audio, language=self.language)
            elif self.engine == 'wit':
                # Richiede WIT_AI_KEY
                return self.recognizer.recognize_wit(audio, key="WIT_AI_KEY")
            elif self.engine == 'bing':
                # Richiede BING_KEY
                return self.recognizer.recognize_bing(audio, key="BING_KEY", language=self.language)
            else:
                logger.error(f"Unknown engine: {self.engine}")
                return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            logger.error(f"Recognition request error: {e}")
            return None
    
    def test_microphone(self) -> Tuple[bool, str]:
        """
        Testa microfono e riconoscimento.
        
        Returns:
            (success, message): True/False, messaggio di test
        """
        try:
            # Verifica microfono disponibile
            mic_list = sr.Microphone.list_microphone_names()
            if not mic_list:
                return False, "Nessun microfono trovato"
            
            logger.info(f"Found {len(mic_list)} microphones: {mic_list}")
            
            # Test breve registrazione
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                return True, f"Microfono OK: {len(mic_list)} dispositivi trovati"
                
        except Exception as e:
            logger.error(f"Microphone test error: {e}")
            return False, f"Errore test microfono: {e}"
    
    def set_language(self, language: str):
        """
        Cambia lingua riconoscimento.
        
        Args:
            language: Codice lingua (it-IT, en-US, fr-FR, etc.)
        """
        self.language = language
        logger.info(f"Language changed to: {language}")
    
    def set_engine(self, engine: str):
        """
        Cambia engine riconoscimento.
        
        Args:
            engine: Nome engine ('google', 'sphinx', 'wit', 'bing')
        """
        self.engine = engine
        logger.info(f"Engine changed to: {engine}")


# Singleton instance
_speech_recognizer = None

def get_speech_recognizer(language='it-IT', engine='google') -> SpeechRecognizer:
    """
    Ottiene istanza singleton SpeechRecognizer.
    
    Args:
        language: Codice lingua
        engine: Engine riconoscimento
        
    Returns:
        SpeechRecognizer
    """
    global _speech_recognizer
    if _speech_recognizer is None:
        _speech_recognizer = SpeechRecognizer(language, engine)
    return _speech_recognizer


# Test standalone
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("TEST SPEECH RECOGNITION")
    print("=" * 60)
    
    recognizer = SpeechRecognizer(language='it-IT', engine='google')
    
    # Test microfono
    print("\n1. Test microfono...")
    success, message = recognizer.test_microphone()
    print(f"   Result: {message}")
    
    if success:
        # Test riconoscimento
        print("\n2. Test riconoscimento vocale...")
        print("   Parla ora! (hai 5 secondi)")
        success, text = recognizer.listen_from_microphone(timeout=5, phrase_time_limit=10)
        
        if success:
            print(f"\n✓ Testo riconosciuto: '{text}'")
        else:
            print(f"\n✗ Errore: {text}")
    
    print("\n" + "=" * 60)

