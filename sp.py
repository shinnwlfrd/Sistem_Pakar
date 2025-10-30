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

# === NILAI PRIOR DAN LIKELIHOOD ===
prior = {'P1': 0.3, 'P2': 0.4, 'P3': 0.3}

likelihood = {
    'P1': {'G1': 0.7, 'G2': 0.9, 'G3': 0.6, 'G4': 0.1, 'G5': 0.4, 'G6': 0.5, 'G7': 0.6, 'G8': 0.1, 'G9': 0.2},
    'P2': {'G1': 0.4, 'G2': 0.05, 'G3': 0.1, 'G4': 0.9, 'G5': 0.2, 'G6': 0.1, 'G7': 0.3, 'G8': 0.8, 'G9': 0.1},
    'P3': {'G1': 0.5, 'G2': 0.1, 'G3': 0.5, 'G4': 0.2, 'G5': 0.9, 'G6': 0.7, 'G7': 0.7, 'G8': 0.1, 'G9': 0.6}
}


# === 2. FUNGSI PERHITUNGAN BAYES ===
def diagnosa(gejala_teramati):
    posterior_unnormalized = {}
    detail_hitung = {}

    for p_kode, p_nama in penyakit.items():
        prob = prior[p_kode]
        langkah = []

        langkah.append(f"### 🧩 {p_nama}")
        langkah.append(f"**Langkah 1: Nilai Prior**  \nP({p_kode}) = {prior[p_kode]:.3f}")

        langkah.append("**Langkah 2: Nilai Likelihood untuk Gejala Terpilih**")
        for g_kode in gejala_teramati:
            langkah.append(f"• P({g_kode}|{p_kode}) = {likelihood[p_kode][g_kode]:.3f} → ({gejala[g_kode]})")

        langkah.append("**Langkah 3: Perkalian Prior × Semua Likelihood**")
        langkah.append(f"Rumus: P({p_kode}) × ∏ P(Gejala|{p_kode})")

        hasil_temp = prior[p_kode]
        for g_kode in gejala_teramati:
            before = hasil_temp
            hasil_temp *= likelihood[p_kode][g_kode]
            langkah.append(f"{before:.6f} × {likelihood[p_kode][g_kode]:.3f} = {hasil_temp:.6f}")

        posterior_unnormalized[p_kode] = hasil_temp
        langkah.append(f"**Langkah 4: Nilai Tidak Ternormalisasi**  \nP({p_kode}|Gejala) ∝ {hasil_temp:.6f}")
        detail_hitung[p_kode] = langkah

    total_prob = sum(posterior_unnormalized.values())
    posterior_normalized = {}
    norm_steps = {}

    for p_kode, val in posterior_unnormalized.items():
        if total_prob > 0:
            posterior_normalized[p_kode] = val / total_prob
        else:
            posterior_normalized[p_kode] = 0

        # Buat langkah rinci normalisasi
        norm_steps[p_kode] = [
            f"**Langkah 5: Normalisasi**",
            f"Total = {total_prob:.6f}",
            f"P({p_kode}|Gejala) = {val:.6f} / {total_prob:.6f}",
            f"= **{posterior_normalized[p_kode]:.6f}** → ({posterior_normalized[p_kode]*100:.2f}%)"
        ]

    return posterior_normalized, detail_hitung, posterior_unnormalized, total_prob, norm_steps


# === 3. ANTARMUKA STREAMLIT ===
st.set_page_config(page_title="🌿 Sistem Pakar Cengkeh", layout="wide")

st.markdown("""
    <style>
    .block-container {max-width: 1000px;}
    .stExpander {background-color: #f9f9f9 !important; border-radius: 8px; border: 1px solid #ddd;}
    .perhitungan {
        font-family: 'Courier New', monospace;
        background-color: #eef1f4;
        padding: 10px 12px;
        border-radius: 6px;
        margin-bottom: 10px;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌿 Sistem Pakar Diagnosa Penyakit Tanaman Cengkeh")
st.markdown("Gunakan aplikasi ini untuk **mendiagnosa penyakit tanaman cengkeh** berdasarkan gejala yang kamu amati.")

st.divider()
st.header("🩺 Pilih Gejala (Minimal 3)")

selected_gejala = []
cols = st.columns(3)
for i, (kode, deskripsi) in enumerate(gejala.items()):
    with cols[i % 3]:
        if st.checkbox(deskripsi, key=kode):
            selected_gejala.append(kode)

st.divider()

if st.button("🔍 Jalankan Diagnosa"):
    if len(selected_gejala) < 3:
        st.warning("❗ Pilih minimal 3 gejala untuk hasil yang akurat.")
    else:
        hasil_prob, detail, unnorm, total, norm_steps = diagnosa(selected_gejala)
        most_likely = max(hasil_prob, key=hasil_prob.get)

        st.subheader("📋 Gejala Terpilih")
        st.write(", ".join([gejala[g] for g in selected_gejala]))

        st.subheader("📊 Perhitungan Probabilitas Lengkap")
        for p_kode, prob in hasil_prob.items():
            with st.expander(f"**{penyakit[p_kode]} — {prob*100:.2f}%**"):
                for langkah in detail[p_kode]:
                    st.markdown(f"<div class='perhitungan'>{langkah}</div>", unsafe_allow_html=True)

                for step in norm_steps[p_kode]:
                    st.markdown(f"<div class='perhitungan'>{step}</div>", unsafe_allow_html=True)

                st.progress(prob)

        st.success(f"🌱 **Diagnosa Akhir:** {penyakit[most_likely]} ({hasil_prob[most_likely]*100:.2f}%)")

else:
    st.info("Pilih gejala, lalu tekan *Jalankan Diagnosa* untuk melihat hasil.")
