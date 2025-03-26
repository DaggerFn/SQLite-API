import cv2
from ultralytics import YOLO
from time import time, sleep
from threading import Lock, Thread
from numpy import zeros, uint8, ceil, hstack, vstack
from flask import Flask, Response
import numpy as np
 
 
# Define a lista de URLs das câmeras
camera_urls = [
    "http://10.1.60.185:5000/video_raw2",
    "http://10.1.60.185:5000/video_raw3",
    "http://10.1.60.185:5000/video_raw4",
    "http://10.1.60.185:5000/video_raw2",
    "http://10.1.60.185:5000/video_raw3",
    "http://10.1.60.185:5000/video_raw4",
]
 
#model = YOLO('yolov8s-pose.pt').to('cpu')
app = Flask(__name__)
 
# Inicializa os frames e frames anotados globais
global_frames = [None] * len(camera_urls)
annotated_frames = [None] * len(camera_urls)
frame_lock = Lock()
 
def imageUpdater(id, video_path, interval):
    global global_frames
    cap = cv2.VideoCapture(video_path)
    last_time = 0
    while True:
        current_time = time()
        if current_time - last_time >= interval:
            last_time = current_time
            success, frame = cap.read()
            if success:
                frame = cv2.resize(frame, (480, 320))  # Redimensiona o frame
                with frame_lock:
                    global_frames[id] = frame
        else:
            cap.grab()
 
def generate():
    global global_frames
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    out = cv2.VideoWriter('appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=ultrafast ! rtph264pay ! udpsink host=127.0.0.1 port=5000', fourcc, 10, (880, 440))
 
    while True:
        sleep(0.05)
        with frame_lock:
            if global_frames:
                # Montar o grid
                grid_size = int(ceil(len(global_frames) ** 0.5))
                grid_frames = []
                for i in range(0, len(global_frames), grid_size):
                    row_frames = global_frames[i:i + grid_size]
                    while len(row_frames) < grid_size:
                        row_frames.append(zeros((480, 640, 3), dtype=uint8))
                    grid_frames.append(hstack(row_frames))
               
                grid_image = vstack(grid_frames)
               
                resized_frame = cv2.resize(grid_image, (880, 440))  # Reduzir a resolução
                out.write(resized_frame)
                _, jpeg = cv2.imencode('.jpg', resized_frame, encode_param)
                frame_bytes = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            else:
                yield (b'--frame\r\n'
                       b'Content-Type: text/plain\r\n\r\n' + b'Waiting for the frame...\r\n')
 
    out.release()
 
 
@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
 
if __name__ == '__main__':
    # Inicializa threads de atualização de frames para cada câmera
    threads = []
    for idx, url in enumerate(camera_urls):
        thread = Thread(target=imageUpdater, kwargs={'id': idx, 'video_path': url, 'interval': 0.01})
        thread.start()
        threads.append(thread)

    # Inicializa o servidor Flask
    app.run(host='0.0.0.0', port=5000)
 
