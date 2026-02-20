import os
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from image_model import extract_features

FEATURES = {}

def build_index():
    global FEATURES
    FEATURES = {}

    if not os.path.exists("covers"):
        os.makedirs("covers")

    for file in os.listdir("covers"):
        path = os.path.join("covers", file)
        image = Image.open(path).convert("RGB")
        FEATURES[file] = extract_features(image)

def search(query_image):
    global FEATURES

    if not FEATURES:
        return None, 0

    query_feature = extract_features(query_image)

    best_match = None
    best_score = -1

    for file, feature in FEATURES.items():
        score = cosine_similarity([query_feature], [feature])[0][0]

        if score > best_score:
            best_score = score
            best_match = file

    return best_match, best_score
