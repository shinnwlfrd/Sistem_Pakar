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

        for g_kode in gejala_teramati:
            prob *= likelihood[p_kode][g_kode]
            langkah.append(f"→ dikalikan {likelihood[p_kode][g_kode]:.3f} menghasilkan {prob:.6f}")

        posterior_unnormalized[p_kode] = prob
        langkah.append(f"**Langkah 4: Nilai Tidak Ternormalisasi**  \nP({p_kode}|Gejala) ∝ {prob:.6f}")
        detail_hitung[p_kode] = langkah

    # Langkah 5A: Hitung total probabilitas
    langkah_total = []
    langkah_total.append("### ⚙️ Langkah 5A: Menghitung Total Probabilitas")
    langkah_total.append("Total = Jumlah semua nilai tidak ternormalisasi dari tiap penyakit:")

    total_prob = 0
    for p_kode, val in posterior_unnormalized.items():
        langkah_total.append(f"• {p_kode}: {val:.6f}")
        total_prob += val

    langkah_total.append(f"**Total = {total_prob:.6f}**")

    # Langkah 5B: Normalisasi ke 100%
    posterior_normalized = {}
    langkah_total.append("### 📊 Langkah 5B: Normalisasi ke Bentuk Persen (100%)")
    for p_kode, val in posterior_unnormalized.items():
        posterior_normalized[p_kode] = (val / total_prob if total_prob > 0 else 0)
        langkah_total.append(
            f"P({p_kode}|Gejala) = {val:.6f} / {total_prob:.6f} = **{posterior_normalized[p_kode]:.6f} ({posterior_normalized[p_kode]*100:.2f}%)**"
        )

    detail_hitung["Total"] = langkah_total

    return posterior_normalized, detail_hitung, posterior_unnormalized, total_prob


# === 3. ANTARMUKA STREAMLIT ===
st.set_page_config(page_title="🌿 Sistem Pakar Cengkeh", layout="wide")

# === CSS adaptif untuk dark/light mode ===
st.markdown("""
    <style>
    .block-container {max-width: 1000px;}
    .stExpander {border-radius: 8px; border: 1px solid var(--border-color, #ddd);}

    @media (prefers-color-scheme: light) {
        .stExpander {background-color: #f9f9f9;}
        .perhitungan {
            font-family: 'Courier New', monospace;
            background-color: #eef1f4;
            color: #000;
            padding: 10px 12px;
            border-radius: 6px;
            margin-bottom: 10px;
            line-height: 1.5;
        }
    }

    @media (prefers-color-scheme: dark) {
        .stExpander {background-color: #1e1e1e;}
        .perhitungan {
            font-family: 'Courier New', monospace;
            background-color: #2b2b2b;
            color: #e8e8e8;
            padding: 10px 12px;
            border-radius: 6px;
            margin-bottom: 10px;
            line-height: 1.5;
        }
    }
    </style>
""", unsafe_allow_html=True)

# === TAMPILAN UTAMA ===
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
        hasil_prob, detail, unnorm, total = diagnosa(selected_gejala)
        most_likely = max(hasil_prob, key=hasil_prob.get)

        st.subheader("📋 Gejala Terpilih")
        st.write(", ".join([gejala[g] for g in selected_gejala]))

        st.subheader("📊 Perhitungan Probabilitas")
        for p_kode, prob in hasil_prob.items():
            with st.expander(f"**{penyakit[p_kode]} — {prob:.2%}**"):
                for langkah in detail[p_kode]:
                    st.markdown(f"<div class='perhitungan'>{langkah}</div>", unsafe_allow_html=True)

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(f"""
                **Langkah 5: Normalisasi Awal (Tinjauan)**  
                P({p_kode}|Gejala) = {unnorm[p_kode]:.6f} / {total:.6f} = **{prob:.6f} ({prob*100:.2f}%)**
                """)
                st.progress(prob)

        st.subheader("🧮 Perhitungan Normalisasi (Langkah 5A & 5B)")
        for langkah in detail["Total"]:
            st.markdown(f"<div class='perhitungan'>{langkah}</div>", unsafe_allow_html=True)

        st.success(f"🌱 **Diagnosa Akhir:** {penyakit[most_likely]} ({hasil_prob[most_likely]*100:.2f}%)")

else:
    st.info("Pilih gejala, lalu tekan *Jalankan Diagnosa* untuk melihat hasil.")
