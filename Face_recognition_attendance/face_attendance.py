import cv2
import torch
import time
import os
import csv
import numpy as np
from torchvision import models, transforms
from PIL import Image
import torch.nn.functional as F

MODEL_PATH = "face_recognition_vgg16_best.pth"
CLASS_INFO = {
    "Labib": "21-45925-3",
    "Utsha": "21-45058-2",
    "Foysal": "21-45809-3",
    "Onnay": "21-45409-3",
    "Sresta": "21-45977-3"
}
CLASS_NAMES = list(CLASS_INFO.keys())
ATTENDANCE_CSV = "attendance.csv"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

model = models.vgg16(pretrained=False)
model.classifier[6] = torch.nn.Linear(4096, len(CLASS_NAMES))

model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model = model.to(DEVICE)
model.eval()

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

marked = set()

def mark_attendance(name, id_number):
    key = f"{name}_{id_number}"
    if key not in marked:
        with open(ATTENDANCE_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, id_number, time.strftime('%Y-%m-%d'), time.strftime('%H:%M:%S')])
        marked.add(key)
        print(f"✅ Marked: {name} ({id_number})")

# Initialize webcam
cap = cv2.VideoCapture(0)
print("🔍 Starting face recognition... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_img = frame[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (224, 224))
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        input_tensor = transform(Image.fromarray(face_img)).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            output = model(input_tensor)
            probs = F.softmax(output, dim=1)
            best_prob, pred = torch.max(probs, 1)
            confidence = best_prob.item()

            if confidence > 0.8:  # Confidence threshold
                name = CLASS_NAMES[pred.item()]
                id_number = CLASS_INFO[name]
                mark_attendance(name, id_number)

                label = f"{name} ({id_number})"
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 255, 0), 2)
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 0, 255), 2)

    cv2.imshow("Face Attendance System", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("📄 Attendance saved to:", ATTENDANCE_CSV)
