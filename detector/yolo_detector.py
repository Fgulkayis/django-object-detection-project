import cv2
from ultralytics import YOLO
import numpy as np
import os

class ObjectDetector:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')
        self.class_names = self.model.names
    
    def detect_objects(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Görsel Bulunmadı Veya Okunmadı: {image_path}")
       
        results= self.model(img ,verbose=False)
       
        annotated_img = img.copy()
      
        for r in results:
            boxes = r.boxes.xyxy.cpu().numpy().astype(int)
            confidences = r.boxes.conf.cpu().numpy()
            class_ids = r.boxes.cls.cpu().numpy().astype(int)

            for box, conf, class_id in zip(boxes, confidences, class_ids):
                x1, y1, x2, y2 = box
                if conf < 0.5:
                    continue
                label = f"{self.class_names[class_id]}: {conf:.2f}"
                color = (0,255,0)

                cv2.rectangle(annotated_img, (x1, y1), (x2, y2), color, 2)
                
                cv2.putText(annotated_img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        return annotated_img