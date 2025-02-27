import pyttsx3
import wave
import tempfile

# Initialize TTS Engine
engine = pyttsx3.init()

# Adjust Speech Rate
engine.setProperty('rate', 100)  # Reduce speed (0.5x slower)

def save_text_to_wav(text, filename="output.wav"):
    """ Convert text to speech and save it as a WAV file """
    print(f"Saving '{text}' as {filename}")

    # Generate speech and save it to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        temp_filename = temp_wav.name
        engine.save_to_file(text, temp_filename)
        engine.runAndWait()

    # Convert to a properly formatted WAV file
    with wave.open(temp_filename, 'rb') as original_wav, wave.open(filename, 'wb') as new_wav:
        new_wav.setnchannels(original_wav.getnchannels())
        new_wav.setsampwidth(original_wav.getsampwidth())
        new_wav.setframerate(original_wav.getframerate())
        new_wav.writeframes(original_wav.readframes(original_wav.getnframes()))

    print(f"Audio saved as {filename}")

# Example usage
text = "Hello, this is your Raspberry Pi speaking!"
save_text_to_wav(text, "speech_output_slow.wav")
