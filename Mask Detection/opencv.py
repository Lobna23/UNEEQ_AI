import cv2
import numpy as np
import tensorflow as tf

# Load the trained model
model = tf.keras.models.load_model("MobileNetV2.h5")  


# Define class labels (must match your model training)
class_labels = ["Mask Worn Incorrectly", "With Mask", "Without Mask"]

# Initialize webcam
cap = cv2.VideoCapture(0)  # 0 for the default camera

# Face detection using OpenCV's built-in Haarcascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

while True:
    # Capture frame from webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    for (x, y, w, h) in faces:
        # Extract face ROI
        face = frame[y:y + h, x:x + w]

        # Preprocess the face image
        face_resized = cv2.resize(face, (224, 224))  # Resize to match model input
        face_normalized = face_resized / 255.0  # Normalize pixel values
        face_reshaped = np.reshape(face_normalized, (1, 224, 224, 3))  # Add batch dimension

        # Make prediction
        predictions = model.predict(face_reshaped)
        predicted_class = np.argmax(predictions)  # Get class index

        # Get class label
        label = class_labels[predicted_class]

        # Define color for bounding box (Green = With Mask, Red = Without Mask, Yellow = Incorrect)
        color = (0, 255, 0) if predicted_class == 1 else (0, 0, 255) if predicted_class == 2 else (0, 255, 255)

        # Draw bounding box and label
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # Show the frame
    cv2.imshow("Mask Detection", frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
