import numpy as np
import cv2
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import Model
from sklearn.metrics.pairwise import cosine_similarity

# Load the pre-trained VGG16 model without the top layers
base_model = VGG16(weights="imagenet", include_top=False)
model = Model(inputs=base_model.input, outputs=base_model.output)

def extract_features(image_path):
    """Extract deep features from an image using VGG16."""
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))  # Resize to match VGG16 input size
    img = np.expand_dims(img, axis=0)  # Expand dimensions to match input shape
    img = preprocess_input(img)  # Preprocess for VGG16
    features = model.predict(img)  # Get deep features
    return features.flatten()  # Flatten the feature map

def compare_images(image1_path, image2_path):
    """Compute similarity between two images using cosine similarity."""
    features1 = extract_features(image1_path)
    features2 = extract_features(image2_path)
    similarity = cosine_similarity([features1], [features2])[0][0]  # Cosine similarity score
    return similarity