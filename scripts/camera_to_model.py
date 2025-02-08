import os
import time
import cv2
from ultralytics import YOLO  # Carlos u prob need to do this: pip install ultralytics

model = YOLO('best.pt')  # replace the string with the path to the model

output_dir = "output_images" # directory to save the output images
os.makedirs(output_dir, exist_ok=True)

def capture_img_csi(output_path):
    os.system(f"libcamera-still -o {output_path}")

def capture_img_USB(output_path):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(output_path, frame)
    cap.release()

# capture images every 10 seconds and process them with YOLO
def main():
    frame_counter = 0
    while True:
        img_path = f"frame_{frame_counter}.jpg"
        capture_img_csi(img_path)  # Use capture_img_USB(img_path) if using a USB camera
        
        # Run YOLO inference on the captured image
        results = model.predict(source=img_path, save=True, save_dir=output_dir)

        print(f"Processed frame {frame_counter}. Output saved to {output_dir}")
        
        frame_counter += 1
        time.sleep(10)

if __name__ == "__main__":
    main()