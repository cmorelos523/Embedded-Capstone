import os
import time
import cv2
from ultralytics import YOLO
import RPi.GPIO as GPIO

model = YOLO('/home/cse475/Embedded-Capstone/runs/detect/train/weights/best.pt')
GPIO.setmode(GPIO.BCM)
pin_number = 17
GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

output_dir = "output_images"
os.makedirs(output_dir, exist_ok=True)

def capture_img_csi(output_path):
    os.system(f"libcamera-still -o {output_path}")

def capture_img_USB(output_path):
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    ret, frame = cap.read()
    print(ret)
    if ret:
        print("sup")
        cv2.imwrite(output_path, frame)
    cap.release()

def main():
    frame_counter = 0
    while True:
        input_value = GPIO.input(pin_number)
        print(input_value)
        if input_value == GPIO.HIGH:
            
            img_path = f"frame_{frame_counter}.jpg"
            capture_img_USB(img_path)
            
            results = model.predict(source=img_path, save=True, save_dir=output_dir)

            print(f"Processed frame {frame_counter}. Output saved to {output_dir}")
            
            frame_counter += 1

if __name__ == "__main__":
    main()