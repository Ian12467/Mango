# yolo_model.py

from ultralytics import YOLO
import cv2
import numpy as np

class MangoClassifier:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
    
    def classify_mango(self, image_path):
        img = cv2.imread(image_path)
        results = self.model(img)
        
        # Process results
        detections = results[0].boxes.data
        class_ids = detections[:, 5].int().tolist()
        confidences = detections[:, 4].tolist()
        boxes = detections[:, :4].tolist()
        
        # Map class IDs to labels (adjust based on your model's classes)
        labels = ['FirstGrade', 'SecondGrade', 'NoGrade']
        classifications = [labels[id] for id in class_ids]
        
        return classifications, confidences, boxes

# In app.py, add:
from yolo_model import MangoClassifier

mango_classifier = MangoClassifier('path_to_your_yolov8_model.pt')

@app.route('/classify', methods=['POST'])
def classify_mango():
    if 'image' not in request.files:
        return jsonify({"error": "No image file"}), 400
    
    image = request.files['image']
    image_path = f"uploads/{image.filename}"
    image.save(image_path)
    
    classifications, confidences, boxes = mango_classifier.classify_mango(image_path)
    
    return jsonify({
        "classifications": classifications,
        "confidences": confidences,
        "boxes": boxes
    })