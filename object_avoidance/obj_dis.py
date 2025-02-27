import cv2
import numpy as np
import ArducamDepthCamera as ac
import pyttsx3
import wave
import tempfile


# Global variables 
threshold = 50  # 50 cm
# Initialize TTS Engine
engine = pyttsx3.init()

# Set Speech Rate
engine.setProperty('rate', 100)


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


def main():

    # Initialize camera 
    camera = ac.ArducamCamera()
    cfg_path = None

    # Open camera 
    ret = 0
    if cfg_path is not None:
        ret = camera.openWithFile(cfg_path, 0)
    else:
        ret = camera.open(ac.Connection.CSI, 0)
    if ret != 0:
        print("Failed to open camera. Error code:", ret)
        return

    ret = camera.start(ac.FrameType.DEPTH)
    if ret != 0:
        print("Failed to start camera. Error code:", ret)
        camera.close()
        return

    try:
        while True:
            # Capture depth frame
            depth_frame = camera.requestFrame(200)  # Timeout of 200ms
            
            if depth_frame is not None:
                # Convert depth data to a NumPy array
                depth_map = np.array(depth_frame.depth_data, dtype=np.float32)

                # Find points that are too close
                too_close = (depth_map > 0) & (depth_map < threshold)
                # Establish left and right side of the camera
                height, width = depth_map.shape
                left_depth = depth_map[0:int(width/2)][:]
                right_depth = depth_map[int(width/2):width][:]

                #Determine if anything is too close 
                too_close_left = np.any((left_depth > 0) & (left_depth < threshold))
                too_close_right = np.any((right_depth > 0) & (right_depth < threshold))
                # print(too_close)
                if too_close_right:
                    save_text_to_wav("Careful, somthing is on your right", "object_right.wav")

                    # # Find the closest point
                    # valid_depths = depth_map[depth_map > 0]  # Ignore zero values
                    # if valid_depths.size > 0:
                    #     min_dist = np.min(valid_depths)
                    #     min_loc = np.unravel_index(np.argmin(depth_map == min_dist), depth_map.shape)
                    # else:
                    #     min_dist = None

                    # min_loc = np.unravel_index(np.argmin(depth_map), depth_map.shape)
                    
                    # print(f"Closest object at {min_loc} with distance {min_dist:.2f}m")
                elif too_close_left:
                    save_text_to_wav("Careful, something is on your left", "object_left.wav")
                
                #No close objects
                else:
                    print("No close objects")
                # Release frame
                camera.releaseFrame(depth_frame)
 

    except KeyboardInterrupt:
        print("Stopping camera...")
    finally:
        camera.stop()
        camera.close()



if __name__ == "__main__":
    main()
