from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the model once when the app starts
model = load_model("pneumonia_model.keras")


def predict_pneumonia(uploaded_image):
    # Same preprocessing used during training in Colab
    img = image.load_img(uploaded_image, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Run the prediction
    prediction_prob = model.predict(img_array)[0][0]

    if prediction_prob > 0.5:
        result = "PNEUMONIA"
        confidence = prediction_prob * 100
    else:
        result = "NORMAL"
        confidence = (1 - prediction_prob) * 100

    return result, round(confidence, 2)
