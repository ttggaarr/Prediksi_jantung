import pickle
import numpy as np
import streamlit as st

# load save model
model = pickle.load(open('/path/ke/direktori/gb_model.sav', 'rb'))

# Tambahkan CSS untuk mempercantik tampilan
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f5f5f5;
        margin: 0;
        padding: 0;
    }
    .stApp {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        max-width: 800px;
        margin: 2rem auto;
    }
    h1 {
        color: #004b8d;
        text-align: center;
    }
    label {
        font-weight: bold;
        color: #333333;
    }
    .stButton>button {
        background-color: #004b8d;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #003366;
    }
    </style>
""", unsafe_allow_html=True)

# Inisialisasi session state untuk melacak halaman
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Navigasi antara halaman
if st.session_state.page == "Home":
    st.title("Selamat Datang di Aplikasi Prediksi Penyakit Jantung!")
    st.write("""
        Aplikasi ini dirancang untuk membantu Anda dalam memprediksi risiko penyakit jantung berdasarkan berbagai faktor kesehatan.
        
        **Fitur Utama:**
        - Input data kesehatan seperti umur, tekanan darah, dan kadar kolesterol.
        - Prediksi risiko penyakit jantung menggunakan model machine learning yang andal.
        
        Silakan klik tombol di bawah ini untuk memulai prediksi Anda!
    """)

    # Tombol untuk navigasi ke halaman prediksi
    if st.button("Mulai Prediksi"):
        st.session_state.page = "Prediksi"

elif st.session_state.page == "Prediksi":
    st.title('Prediksi Penyakit Jantung')

    # Tata letak dua kolom besar
    col_left, col_right = st.columns(2)

    with col_left:
        age = st.number_input('Umur', step=2, min_value=0)
        resting_blood_pressure = st.number_input('Tekanan Darah Saat Istirahat (mmHg)', step=2, min_value=0)
        cholestoral = st.number_input('Kadar Kolesterol (mg/dL)', step=2, min_value=0)
        Max_heart_rate = st.number_input('Detak Jantung Maksimum', step=2, min_value=0)
        oldpeak = st.number_input('Depresi ST (Oldpeak)', step=2, min_value=0)
        slope = st.selectbox('Kemiringan (Slope) Segmen ST (0-2)', [0, 1, 2])

    with col_right:
        sex = st.selectbox('Jenis Kelamin (0: Perempuan, 1: Laki-laki)', [0, 1])
        chest_pain_type = st.selectbox('Jenis Nyeri Dada (0-3)', [0, 1, 2, 3])
        fasting_blood_sugar = st.selectbox('Gula Darah Puasa (>120 mg/dL: 1, Lainnya: 0)', [0, 1])
        rest_ecg = st.selectbox('Hasil Elektrokardiografi (0-2)', [0, 1, 2])
        exercise_induced_angina = st.selectbox('Angina Induksi Olahraga (0: Tidak, 1: Ya)', [0, 1])
        vessels_colored_by_flourosopy = st.selectbox('Pembuluh Darah Berwarna oleh Fluoroskopi (0-3)', [0, 1, 2, 3])
        thalassemia = st.selectbox('Talasemia (0: Tidak Diketahui, 1: Normal, 2: Cacat Tetap, 3: Cacat Reversibel)', [0, 1, 2, 3])

    # Code untuk prediksi
    heart_diagnosis = ''

    # Membuat tombol prediksi
    if st.button('Prediksi Penyakit Jantung'):
        heart_prediction = model.predict([[age, sex, chest_pain_type, resting_blood_pressure, cholestoral, 
                                            fasting_blood_sugar, rest_ecg, Max_heart_rate, exercise_induced_angina, 
                                            oldpeak, slope, vessels_colored_by_flourosopy, thalassemia]])
        
        if heart_prediction[0] == 1:
            heart_diagnosis = 'Pasien Terkena Penyakit Jantung'
        else:
            heart_diagnosis = 'Pasien Tidak Terkena Penyakit Jantung'

    st.success(heart_diagnosis)

    # Tombol kembali ke halaman Home
    if st.button("Kembali ke Home"):
        st.session_state.page = "Home"
