from ultralytics import YOLO
import cv2
import numpy as np


# Load a model
model = YOLO('yolov8n.pt') # pretrained YOLOv8n model

# Run single inference for a image
frame = cv2.imread('neymar.jpeg')
results = model(frame)

# Process results list
for result in results:
    boxes = result.boxes.cpu().numpy()
    for i, box in enumerate(boxes):
        r = box.xyxy[0].astype(int)
        classes = result.names[int(box.cls[0])]
        if classes == 'cat':
            cv2.rectangle(frame, r[:2], r[2:], (0, 255, 0), 3)
            xmin, ymin, xmax, ymax = r[:4]

            text = '{} {:.1%}'.format(classes, round(box.conf[0], 2))
            (text_width, text_height) = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, fontScale=1, thickness=1)[0]
            padding = 5
            rect_height = text_height + padding * 7
            rect_width = text_width + padding * 26
            cv2.rectangle(frame, (xmin, ymin), (xmin + rect_width, ymin - rect_height), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, text, (xmin + padding, ymin - text_height + padding), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), lineType=cv2.LINE_AA, thickness=2)

    cv2.imshow("YOLOv8 Inference", frame)
    cv2.imwrite('neymar_output.png', frame)
    cv2.waitKey(0)


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

