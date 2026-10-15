import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi Halaman Dashboard
st.set_page_config(
    page_title="Dashboard Analisis Fiskal",
    page_icon="📊",
    layout="wide"
)

# Judul Utama Dashboard
st.title("📊 Dashboard Analisis Dataset Fiskal")
st.markdown("Dashboard interaktif ini dibangun menggunakan **Streamlit**, **Pandas**, **NumPy**, dan **Matplotlib** untuk menganalisis data fiskal.")

# URL Dataset dari GitHub
URL = "https://raw.githubusercontent.com/Alam-A99/DATAAKSI/refs/heads/main/dataset_fiskal_97_hipoFull.csv"

# Fungsi untuk memuat data dengan caching agar performa lebih cepat
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

# Memuat data
with st.spinner("Sedang memuat data dari GitHub..."):
    try:
        df = load_data(URL)
        st.success("Data berhasil dimuat!")
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        st.stop()

# --- SIDEBAR: KONTROL & FILTER ---
st.sidebar.header("⚙️ Pengaturan Dashboard")

# Opsi untuk melihat tabel data mentah
if st.sidebar.checkbox("🔍 Tampilkan Raw Data", value=False):
    st.subheader("Pratinjau Data Mentah")
    st.dataframe(df.head(50), use_container_width=True)

# Informasi Umum Dataset
st.sidebar.markdown("---")
st.sidebar.subheader("📌 Informasi Dataset")
st.sidebar.write(f"**Total Baris:** {df.shape[0]}")
st.sidebar.write(f"**Total Kolom:** {df.shape[1]}")

# --- RINGKASAN STATISTIK ---
st.subheader("📈 Ringkasan Statistik Deskriptif")
st.markdown("Statistik utama menggunakan fungsi agregasi Pandas & NumPy:")
st.dataframe(df.describe(), use_container_width=True)

# --- VISUALISASI DATA MENGGUNAKAN MATPLOTLIB ---
st.subheader("📊 Visualisasi Grafik Interaktif")

# Menyaring kolom yang bernilai numerik
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

if len(numeric_cols) > 0:
    # Pilihan kolom oleh pengguna
    selected_col = st.selectbox("Pilih Kolom Numerik untuk Dianalisis:", numeric_cols)
    
    # Layout 2 kolom untuk grafik
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Histogram Distribusi: {selected_col}**")
        fig, ax = plt.subplots(figsize=(7, 4))
        df[selected_col].dropna().hist(ax=ax, bins=25, color='#4f46e5', edgecolor='white', alpha=0.8)
        ax.set_title(f"Distribusi {selected_col}", fontsize=12)
        ax.set_xlabel(selected_col)
        ax.set_ylabel("Frekuensi")
        st.pyplot(fig)
        
    with col2:
        st.markdown(f"**Boxplot (Deteksi Outlier): {selected_col}**")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.boxplot(df[selected_col].dropna(), patch_artist=True, boxprops=dict(facecolor='#10b981', color='#047857'))
        ax.set_title(f"Boxplot {selected_col}", fontsize=12)
        ax.set_ylabel(selected_col)
        st.pyplot(fig)
        
    # Analisis Metrik Tambahan menggunakan NumPy
    st.markdown("---")
    st.subheader("💡 Metrik Kalkulasi NumPy")
    col_a, col_b, col_c, col_d = st.columns(4)
    
    col_a.metric("Nilai Rata-rata (Mean)", f"{np.mean(df[selected_col]):,.2f}")
    col_b.metric("Nilai Tengah (Median)", f"{np.median(df[selected_col].dropna()):,.2f}")
    col_c.metric("Standar Deviasi", f"{np.std(df[selected_col].dropna()):,.2f}")
    col_d.metric("Nilai Maksimum", f"{np.max(df[selected_col]):,.2f}")

else:
    st.warning("Tidak ditemukan kolom numerik yang valid untuk divisualisasikan dalam dataset ini.")