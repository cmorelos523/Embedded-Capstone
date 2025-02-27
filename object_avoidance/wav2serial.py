import os
import spidev
import wave
import time

# SPI Setup (adjust to your STM32 setup)
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI bus 0, device 0
spi.max_speed_hz = 1000000  # Adjust SPI speed as needed

# Folder containing WAV files
wav_folder = "/path/to/wav/folder"

# List of priority files (can be full filenames or partial)
priority_files = ["object_right.wav", "object_left.wav"]

def send_wav_over_spi(wav_file):
    """ Read WAV file, convert to PCM, and send over SPI """
    with wave.open(wav_file, 'rb') as wav:
        # Extract parameters
        channels = wav.getnchannels()
        sample_width = wav.getsampwidth()
        sample_rate = wav.getframerate()
        num_frames = wav.getnframes()
        
        print(f"Sending {wav_file} (Channels: {channels}, Rate: {sample_rate}Hz, Frames: {num_frames})")

        # Read raw PCM data
        pcm_data = wav.readframes(num_frames)

        # Send PCM data in chunks
        chunk_size = 1024  # Size of each chunk to send over SPI
        for i in range(0, len(pcm_data), chunk_size):
            spi.xfer2(list(pcm_data[i:i + chunk_size]))  # Send PCM chunk
            time.sleep(0.005)  # Small delay to prevent overflow

def process_folder(wav_folder):
    """ Process all WAV files in the folder, prioritizing certain files """
    files = os.listdir(wav_folder)
    files_with_time = [] # Organize off time 
    # First process priority files
    for priority in priority_files:
        if priority in files:
            file_path = os.path.join(wav_folder, priority)
            creation_time = os.path.getctime(file_path)
            send_wav_over_spi(file_path)
            files_with_time.append((file_path, creation_time))
            files.remove(priority)  # Remove from remaining files list to avoid duplication

    # Then process all other files
    for filename in files:
        if filename.endswith(".wav"):  # Only process WAV files
            file_path = os.path.join(wav_folder, filename)
            send_wav_over_spi(file_path)

try:
    process_folder(wav_folder)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    spi.close()
