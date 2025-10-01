import cv2
import numpy as np
from mtcnn.mtcnn import MTCNN

from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.sequence import pad_sequences


def extract_frames_from_video(video_path, frame_interval=15):
    """
    Extract frames from a single video and return them as a list for later processing.

    Args:
    - video_path (str): Path to the input video file.
    - frame_interval (int): Interval for frame extraction (e.g., extract every 30th frame).

    Returns:
    - frames (list): A list of frames extracted from the video.
    """
    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Get the total frame count and frame rate
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)

    print(f"Processing {video_path} - Total frames: {total_frames}, FPS: {fps}")

    frames = []
    count = 0

    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Extract the frame every `frame_interval` frames
        if count % frame_interval == 0:
            frames.append(frame)

        count += 1

    # Release the video capture object
    video.release()

    print(f"Extracted {len(frames)} frames from {video_path}")

    return frames

def extract_highest_confidence_face_from_frames(frames):
    """
    Extract the face with the highest confidence score from a list of frames using MTCNN.
    :param frames: List of frames (images) extracted from the video.
    :return: List of the highest confidence face images from each frame.
    """
    mtcnn = MTCNN()

    face_images = []

    for idx, frame in enumerate(frames):
        faces = mtcnn.detect_faces(frame)

        if faces:
            highest_confidence_face = None
            max_confidence = 0  # Variable to store the highest confidence

            for face in faces:
                confidence = face['confidence']
                if confidence > max_confidence:
                    max_confidence = confidence
                    highest_confidence_face = face

            if highest_confidence_face:
                x, y, w, h = highest_confidence_face['box']
                face_crop = frame[y:y+h, x:x+w]
                face_images.append(face_crop)

    print(f"Extracted {len(face_images)} faces with the highest confidence.")
    return face_images


def preprocess_image(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (224, 224))
    image_preprocessed = preprocess_input(image_resized)
    image_batch = np.expand_dims(image_preprocessed, axis=0)

    return image_batch

def feature_extraction(faces):
    features = []

    model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
    feature_extractor = Model(inputs=model.input, outputs=model.output)

    for face in faces:
        face_n = preprocess_image(face)
        face_feature = feature_extractor.predict(face_n)
        features.append(face_feature)

    features = np.concatenate(features, axis=0)

    features = np.expand_dims(features, axis=0)

    return features

def prediction(video_path):
    # Load the saved model
    model = load_model('my_model.keras')

    video_capture = cv2.VideoCapture(video_path)

    frames_list = extract_frames_from_video(video_path)
    faces = extract_highest_confidence_face_from_frames(frames_list)
    ResNet_features = feature_extraction(faces)
    max_length = 108
    features_padded = pad_sequences(ResNet_features, maxlen=max_length, dtype='float32', padding='post', truncating='post')
    predictions = model.predict(np.array(features_padded))
    pred = (predictions > 0.5).astype(int)

    if pred == 1:
        print("This video is FAKE")
    elif pred == 0:
        print("This video is REAL")

    return predictions






