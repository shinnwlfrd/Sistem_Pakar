import streamlit as st

# === 1. BASIS PENGETAHUAN ===

gejala = {
    'G1': 'Daun menguning',
    'G2': 'Akar membusuk',
    'G3': 'Batang lembek',
    'G4': 'Daun bercak hitam',
    'G5': 'Layu tiba-tiba',
    'G6': 'Ranting mengering',
    'G7': 'Daun rontok',
    'G8': 'Bintik putih pada daun',
    'G9': 'Pembengkakan pada batang'
}

penyakit = {
    'P1': 'Penyakit Busuk Akar',
    'P2': 'Penyakit Bercak Daun',
    'P3': 'Penyakit Layu Bakteri'
}

prior = {
    'P1': 0.3,
    'P2': 0.4,
    'P3': 0.3
}

likelihood = {
    'P1': {'G1': 0.7, 'G2': 0.9, 'G3': 0.6, 'G4': 0.1, 'G5': 0.4, 'G6': 0.5, 'G7': 0.6, 'G8': 0.1, 'G9': 0.2},
    'P2': {'G1': 0.4, 'G2': 0.05, 'G3': 0.1, 'G4': 0.9, 'G5': 0.2, 'G6': 0.1, 'G7': 0.3, 'G8': 0.8, 'G9': 0.1},
    'P3': {'G1': 0.5, 'G2': 0.1, 'G3': 0.5, 'G4': 0.2, 'G5': 0.9, 'G6': 0.7, 'G7': 0.7, 'G8': 0.1, 'G9': 0.6}
}

# === 2. LOGIKA DIAGNOSA ===

def diagnosa(gejala_teramati):
    """
    Menghitung probabilitas posterior untuk setiap penyakit berdasarkan gejala yang teramati.
    Menggunakan Teorema Bayes dengan asumsi independensi gejala.
    """
    posterior_unnormalized = {}
    
    for p_kode, p_nama in penyakit.items():
        prob = prior[p_kode]
        for g_kode in gejala_teramati:
            prob *= likelihood[p_kode][g_kode]
        posterior_unnormalized[p_kode] = prob
    
    total_prob = sum(posterior_unnormalized.values())
    posterior_normalized = {}
    
    if total_prob > 0:
        for p_kode, prob in posterior_unnormalized.items():
            posterior_normalized[p_kode] = prob / total_prob
    else:
        posterior_normalized = prior
    
    return posterior_normalized

# === 3. ANTARMUKA STREAMLIT ===

st.set_page_config(
    page_title="Sistem Pakar Cengkeh",
    page_icon="🌿",
    layout="centered"
)

st.title("🌿 Sistem Pakar Diagnosa Penyakit Tanaman Cengkeh")
st.markdown("Gunakan aplikasi ini untuk **mendiagnosa penyakit tanaman cengkeh** berdasarkan gejala yang teramati.")

st.divider()

st.header("🩺 Pilih Gejala yang Teramati (minimal 3)")

selected_gejala = []
cols = st.columns(3)

for i, (kode, deskripsi) in enumerate(gejala.items()):
    with cols[i % 3]:
        if st.checkbox(deskripsi, key=kode):
            selected_gejala.append(kode)

st.divider()

if st.button("🔍 Jalankan Diagnosa"):
    if len(selected_gejala) < 3:
        st.warning("❗ Silakan pilih **minimal 3 gejala** untuk hasil diagnosa yang akurat.")
    else:
        hasil_probabilitas = diagnosa(selected_gejala)
        most_likely_kode = max(hasil_probabilitas, key=hasil_probabilitas.get)
        
        st.subheader("📋 Gejala yang Dipilih")
        for g_kode in selected_gejala:
            st.write(f"• {gejala[g_kode]}")
        
        st.subheader("📊 Probabilitas Tiap Penyakit")
        for p_kode, prob in hasil_probabilitas.items(
            st.write(f"• **{penyakit[p_kode]}** → {prob:.2%}")
        
        st.success(f"🌱 **Diagnosa Akhir: {penyakit[most_likely_kode]}**")
        st.caption(f"(Probabilitas: {hasil_probabilitas[most_likely_kode]:.2%})")
else:
    st.info("Pilih minimal 3 gejala, lalu tekan tombol *Jalankan Diagnosa* untuk melihat hasil.")        
