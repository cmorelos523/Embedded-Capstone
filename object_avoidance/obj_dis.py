import cv2
import numpy as np
import ArducamDepthCamera as ac

# Global variables 
threshold = 50  # 50 cm

def main():
    # Initialize camera 
    camera = ac.ArducamCamera()
    cfg_path = None
    # cfg_path = "file.cfg"

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

                # print(too_close)
                if np.any(too_close):
                    print("Warning: Object too close!")

                    # Find the closest point
                    valid_depths = depth_map[depth_map > 0]  # Ignore zero values
                    if valid_depths.size > 0:
                        min_dist = np.min(valid_depths)
                        min_loc = np.unravel_index(np.argmin(depth_map == min_dist), depth_map.shape)
                    else:
                        min_dist = None

                    min_loc = np.unravel_index(np.argmin(depth_map), depth_map.shape)
                    
                    print(f"Closest object at {min_loc} with distance {min_dist:.2f}m")
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
