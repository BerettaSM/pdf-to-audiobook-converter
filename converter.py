import pyttsx3 as tts


class AudioConverter:

    @staticmethod
    def convert_and_save(string: str, save_location: str):
        engine = tts.init()
        engine.setProperty("rate", 150)
        engine.save_to_file(string, save_location)
        engine.runAndWait()
