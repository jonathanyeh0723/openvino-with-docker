import cv2
from ultralytics import YOLO
import time
import collections
import numpy as np

# Load a pretrained YOLOv8n model
model = YOLO('yolov8n.pt')

# Define path to input file
# video_file =
cap = cv2.VideoCapture(0)
# Run inference on the source
while cap.isOpened():
    success, frame = cap.read()
    _, f_width = frame.shape[:2]
    processing_times = collections.deque()

    if success:
        start_time = time.time()
        results = model(frame)
        
        stop_time = time.time()
        processing_times.append(stop_time - start_time)

        annotated_frame = results[0].plot()
        # Use processing times from last 200 frames.
        if len(processing_times) > 200:
            processing_times.popleft()

        #_, f_width = frame.shape[:2]
        # Mean processing time [ms].
        processing_time = np.mean(processing_times) * 1000
        fps = 1000 / processing_time
        cv2.putText(
            img=annotated_frame,
            text=f"Inference time: {processing_time:.1f}ms ({fps:.1f} FPS)",
            org=(20, 40),
            fontFace=cv2.FONT_HERSHEY_COMPLEX,
            fontScale=f_width / 1000,
            color=(0, 0, 255),
            thickness=1,
            lineType=cv2.LINE_AA,
        )

        #annotated_frame = results[0].plot()
        #for #result in results:
            #boxes = result.boxes.cpu().numpy()
            #for i, box in enumerate(boxes):
                #r = box.xyxy[0].astype(int)
                #print(r)
                #classes = result.names[int(box.cls[0])]
                #print(classes, box.conf[0])
                #if classes == 'person':
                #cv2.rectangle(frame, r[:2], r[2:], (0, 255, 0), 3)

        cv2.imshow("YOLOv8 Inference", annotated_frame)
        #cv2.imshow("YOLOv8 Inference", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    else:
        break

# Release
cap.release()
cv2.destroyAllWindows()
