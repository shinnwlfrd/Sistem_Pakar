import streamlit as st
from fractions import Fraction

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

prior = {'P1': 0.3, 'P2': 0.4, 'P3': 0.3}

likelihood = {
    'P1': {'G1': 0.7, 'G2': 0.9, 'G3': 0.6, 'G4': 0.1, 'G5': 0.4, 'G6': 0.5, 'G7': 0.6, 'G8': 0.1, 'G9': 0.2},
    'P2': {'G1': 0.4, 'G2': 0.05, 'G3': 0.1, 'G4': 0.9, 'G5': 0.2, 'G6': 0.1, 'G7': 0.3, 'G8': 0.8, 'G9': 0.1},
    'P3': {'G1': 0.5, 'G2': 0.1, 'G3': 0.5, 'G4': 0.2, 'G5': 0.9, 'G6': 0.7, 'G7': 0.7, 'G8': 0.1, 'G9': 0.6}
}


# === 2. LOGIKA PERHITUNGAN BAYES ===
def diagnosa(gejala_teramati):
    posterior_unnormalized = {}
    detail_hitung = {}

    for p_kode, p_nama in penyakit.items():
        prob = prior[p_kode]
        langkah = []
        langkah.append(f"**Langkah 1: Prior**  \nP({p_kode}) = {prior[p_kode]:.3f}")
        langkah.append(f"**Langkah 2: Likelihood**")

        for g_kode in gejala_teramati:
            prob *= likelihood[p_kode][g_kode]
            langkah.append(
                f"   × P({g_kode}|{p_kode}) = {likelihood[p_kode][g_kode]:.3f} → Nilai sementara = {prob:.6f}"
            )

        posterior_unnormalized[p_kode] = prob
        langkah.append(f"**Langkah 3: Nilai tidak ternormalisasi**  \n"
                       f"P({p_kode}|Gejala) ∝ {prob:.6f}")
        detail_hitung[p_kode] = langkah

    total_prob = sum(posterior_unnormalized.values())
    posterior_normalized = {}

    for p_kode, prob in posterior_unnormalized.items():
        posterior_normalized[p_kode] = prob / total_prob if total_prob > 0 else 0

    return posterior_normalized, detail_hitung, posterior_unnormalized, total_prob


# === 3. ANTARMUKA STREAMLIT ===
st.set_page_config(page_title="🌿 Sistem Pakar Cengkeh", layout="wide")

# CSS agar tampil rapi di desktop
st.markdown("""
    <style>
    .block-container {
        max-width: 1000px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stExpander {
        background-color: #f8f9fa !important;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    .stProgress > div > div {
        background-color: #2e8b57 !important;
    }
    .perhitungan {
        font-family: 'Courier New', monospace;
        background-color: #f0f2f6;
        padding: 8px 12px;
        border-radius: 6px;
        margin-bottom: 6px;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌿 Sistem Pakar Diagnosa Penyakit Tanaman Cengkeh")
st.markdown("Gunakan aplikasi ini untuk **mendiagnosa penyakit tanaman cengkeh** berdasarkan gejala yang teramati.")

st.divider()
st.header("🩺 Pilih Gejala yang Teramati (Minimal 3)")

selected_gejala = []
cols = st.columns(3)
for i, (kode, deskripsi) in enumerate(gejala.items()):
    with cols[i % 3]:
        if st.checkbox(deskripsi, key=kode):
            selected_gejala.append(kode)

st.divider()

if st.button("🔍 Jalankan Diagnosa"):
    if len(selected_gejala) < 3:
        st.warning("❗ Harap pilih minimal **3 gejala** untuk hasil yang akurat.")
    else:
        hasil_probabilitas, detail_hitung, posterior_unnormalized, total_prob = diagnosa(selected_gejala)
        most_likely = max(hasil_probabilitas, key=hasil_probabilitas.get)

        st.subheader("📋 Gejala yang Dipilih")
        st.write(", ".join([gejala[g] for g in selected_gejala]))

        st.subheader("📊 Hasil Probabilitas Penyakit")

        for p_kode, prob in hasil_probabilitas.items():
            with st.expander(f"**{penyakit[p_kode]} → {prob:.2%}**"):
                for langkah in detail_hitung[p_kode]:
                    st.markdown(f"<div class='perhitungan'>{langkah}</div>", unsafe_allow_html=True)
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(f"""
                **Langkah 4: Normalisasi**  
                P({p_kode}|Gejala) = {posterior_unnormalized[p_kode]:.6f} / {total_prob:.6f}  
                = **{prob:.6f}**
                """)
                st.progress(prob)

        st.success(f"🌱 **Diagnosa Akhir:** {penyakit[most_likely]} ({hasil_probabilitas[most_likely]:.2%})")

else:
    st.info("Pilih gejala, lalu tekan *Jalankan Diagnosa* untuk melihat hasil.")
