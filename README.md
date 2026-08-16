# Pneumonia Detection from Chest X-Ray Images

An educational deep learning project that detects pneumonia from chest X-ray images using Transfer Learning.

> ⚠️ **Medical Disclaimer:** This project is for learning and portfolio purposes only. It is **not** a real medical diagnosis tool and must not be used to make actual medical decisions.

## Goal

Classify chest X-ray images into two classes: `NORMAL` or `PNEUMONIA`, using a neural network built with Transfer Learning.

## Dataset

- **Source:** Kermany et al. (2018), Mendeley Data / the well-known Kaggle "Chest X-Ray Images (Pneumonia)" dataset.
- **Classes:** NORMAL, PNEUMONIA.
- **Size:** ~5,800 images (train + test), with an additional validation split (15%) taken from the training set.

## Model

- **Base model:** MobileNetV2 (Transfer Learning, pretrained on ImageNet).
- Custom layers added on top (GlobalAveragePooling + Dense + Dropout), followed by fine-tuning of the last 30 layers of MobileNetV2.
- Class weights were used to handle class imbalance.

## Technologies

- Python, TensorFlow / Keras
- Streamlit (user interface)
- NumPy, Pillow

## Running Locally

```bash
# 1. Clone the repository
git clone <repository-url>
cd pneumonia-detection

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

## Usage Example

1. Open the app.
2. Upload a chest X-ray image (jpg/png).
3. Click "Run analysis".
4. The result (NORMAL or PNEUMONIA) and the model's confidence score will appear.

## Results (Metrics on Test Data)

| Metric | NORMAL | PNEUMONIA |
|---|---|---|
| Precision | 0.93 | 0.86 |
| Recall | 0.74 | 0.97 |
| F1-score | 0.82 | 0.91 |

**Overall Accuracy:** 88%

Recall for the PNEUMONIA class was prioritized (97%) because missing a real pneumonia case (False Negative) is far more dangerous than a false alarm.

## Limitations

- The dataset originates from a single hospital in China and may not generalize well to other imaging devices or populations.
- The original class imbalance (more PNEUMONIA images than NORMAL) may still affect results despite mitigation.
- The model does not distinguish between pneumonia types (bacterial/viral).
- Performance on low-quality images or non-standard imaging angles is not guaranteed.

## Medical Disclaimer

This app is **not an approved medical diagnosis tool** and must not replace consultation with a doctor or radiologist. All results are for educational purposes only.
