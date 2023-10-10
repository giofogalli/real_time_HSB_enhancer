# Real time USB Compliant Camera play with RGB and HSB enhanced frames

import os
import cv2
import numpy as np
from PIL import Image
import datetime

def HSB_enhance(img, shift_den=150):
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    neg = 255 - gray
    r, c = gray.shape
    shift = r// shift_den
    enhanced = (gray[shift:,:] + neg[:-shift,:]) #255 - 
    enhanced = cv2.blur(enhanced, ((shift//2)+1, (shift//2)+1))
    black_box = np.zeros_like(gray)
    black_box[int(np.floor(shift/2)):-int(np.ceil(shift/2))] = enhanced
    gray_blurred = cv2.blur(gray, ((shift//2)+1, (shift//2)+1))
    black_box = cv2.addWeighted(black_box, 0.9, gray_blurred, 0.1, 1)
    #p_final = Image.fromarray(black_box)
    #enhancer = ImageEnhance.Contrast(p_final)
    #p_enhanced = enhancer.enhance(2)# 1.5
    #final = np.asarray(p_enhanced)
    return(black_box)


CWD = os.getcwd()

def real_time_video(n, frame_size=(640,480), fps=60):
    
    cap = cv2.VideoCapture(n)
    #cap.open(n, apiPreference=cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_size[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_size[1])
    cap.set(cv2.CAP_PROP_FPS, fps)
    # loop over frames from the video stream
    
    mode = 'rgb'
    win_name = f'Camera {n}'
    output_path = os.path.join(CWD,'saved_frames')
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    
    print('''
    Real time USB Compliant Camera

    Press "c" to change mode between RGB and HSB enhanced.
    Press "s" to save current frame in ./saved_frames.
    Press "q" or "ESC" to exit.
    
    ''')
    
    print_frame_shape = True
    while True:
        ret, frame = cap.read()
        if not ret:
            print("VideoCaptureError: could not read any frame.")
            break
        if print_frame_shape:
            print(f"Current frame shape is {frame.shape[:2][::-1]}.")
            print_frame_shape = False

        if mode == 'hsb':
            frame = HSB_enhance(frame)

        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

        # Move it to (X,Y)
        #cv2.moveWindow(win_name, X, Y)
            
        # Show the Image in the Window
        cv2.imshow(win_name, frame)
        
        # Resize the Window
        rows, cols = frame.shape[:2]
        cv2.resizeWindow(win_name, 1000, 600)
        #cv2.imshow(f'Camera {n}', frame
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop

        if key == ord("c"):
            mode = 'rgb' if mode != 'rgb' else 'hsb'

        elif key == ord("s"):
            current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d_%H.%M.%S')
            time_name = current_time + '.jpg'
            cv2.imwrite(os.path.join(output_path, time_name), frame)

        elif key == ord("q") or key == 27: # ESC # or cv2.getWindowProperty(win_name, 1) < 0:
            #print(cv2.getWindowProperty(win_name, 1))
            break
        
    
    cv2.destroyAllWindows()
    cap.release()
    

if __name__ == '__main__':
    
    import argparse

    parser = argparse.ArgumentParser(description="""
    
    Select camera index and frame size to be used.
    
    camera_index [int]: 0, 1, 2 ...
    frame_size [int: width height]*: 640 480 (default), 1920 1080, 3840 2160 ... 
    *it will aprox. to closest camera resolution.
    
    Common resolutions (16:9):
    High Definition (HD)    1280 x 720
    Full HD, FHD            1920 x 1080
    2K, Quad HD, QHD        2560 x 1440
    4K, Ultra HD            3840 x 2160
    5K, Ultra HD            5120 x 2880
    8K, Ultra HD            7680 x 4320
    """)

    print(parser.description)

    parser.add_argument('-i','--camera_index', metavar='N', type=int, help='Must be a integer that represents camera source.', required=True)
    parser.add_argument('-f','--frame_size', type=int, nargs=2, help='Must be a tuple repesenting (height, width) of the target frame.', required=False)
    args = vars(parser.parse_args())

    cam_index = args['camera_index']
    frame_size = args['frame_size']
    if frame_size is None:
        frame_size = [480, 640]
    
    frame_size = frame_size[::-1]
    
    real_time_video(cam_index, frame_size)
