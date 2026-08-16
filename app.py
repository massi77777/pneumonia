import streamlit as st
from utils.prediction import predict_pneumonia

st.set_page_config(page_title="Pneumonia Detection", page_icon="🫁")

st.title("🫁 Pneumonia Detection from Chest X-Ray")
st.write("Upload a chest X-ray image and the model will analyze it.")

# Important disclaimer: this is not a medical diagnosis tool
st.warning(
    "⚠️ This app is for educational purposes only and is NOT a medical "
    "diagnosis tool. Do not rely on it for real medical decisions. "
    "Always consult a qualified doctor."
)

uploaded_file = st.file_uploader("Choose an X-ray image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(uploaded_file, caption="Uploaded image", use_container_width=True)

    if st.button("Run analysis"):
        with st.spinner("Analyzing image..."):
            result, confidence = predict_pneumonia(uploaded_file)

        st.subheader("Result:")

        if result == "PNEUMONIA":
            st.error(f"Predicted result: **{result}**")
        else:
            st.success(f"Predicted result: **{result}**")

        st.metric(label="Model confidence", value=f"{confidence:.1f}%")

        st.caption(
            "This confidence score is an internal number from the model "
            "based on training data, not a real medical probability."
        )
