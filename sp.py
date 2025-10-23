import streamlit as st

# === 1. DATA DASAR SISTEM ===
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

# Prior (peluang awal sebelum melihat gejala)
prior = {
    'P1': 0.3,
    'P2': 0.4,
    'P3': 0.3
}

# Likelihood: P(gejala | penyakit)
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
        langkah = [f"P({p_kode}) = {prior[p_kode]}"]
        for g_kode in gejala_teramati:
            prob *= likelihood[p_kode][g_kode]
            langkah.append(f"× P({g_kode}|{p_kode}) = {likelihood[p_kode][g_kode]}")
        posterior_unnormalized[p_kode] = prob
        detail_hitung[p_kode] = langkah

    total_prob = sum(posterior_unnormalized.values())
    posterior_normalized = {}

    if total_prob > 0:
        for p_kode, prob in posterior_unnormalized.items():
            posterior_normalized[p_kode] = prob / total_prob
    else:
        posterior_normalized = prior

    return posterior_normalized, detail_hitung, total_prob


# === 3. ANTARMUKA STREAMLIT ===
st.set_page_config(page_title="🌿 Sistem Pakar Cengkeh", layout="centered")
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
        st.warning("❗ Harap pilih minimal **3 gejala** untuk mendapatkan hasil diagnosa yang akurat.")
    else:
        hasil_probabilitas, detail_hitung, total_prob = diagnosa(selected_gejala)
        most_likely = max(hasil_probabilitas, key=hasil_probabilitas.get)

        st.subheader("📋 Gejala yang Dipilih")
        for g in selected_gejala:
            st.write(f"• {gejala[g]}")

        st.subheader("📊 Hasil Probabilitas Penyakit")

        for p_kode, prob in hasil_probabilitas.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{penyakit[p_kode]}** → {prob:.2%}")
            with col2:
                with st.expander("Detail"):
                    st.markdown(f"**Langkah Perhitungan {penyakit[p_kode]}**")
                    for langkah in detail_hitung[p_kode]:
                        st.write(langkah)
                    st.write(f"= {posterior_unnormalized := prior[p_kode] * \
                        eval('*'.join(str(likelihood[p_kode][g]) for g in selected_gejala))}")
                    st.write(f"Total = {total_prob:.6f}")
                    st.write(f"P({p_kode}|Gejala) = {posterior_unnormalized:.6f} / {total_prob:.6f} = {prob:.6f}")
                    st.progress(prob)

        st.success(f"🌱 **Diagnosa Akhir: {penyakit[most_likely]}**")
        st.caption(f"(Probabilitas: {hasil_probabilitas[most_likely]:.2%})")

else:
    st.info("Pilih gejala, lalu tekan tombol *Jalankan Diagnosa* untuk melihat hasil.")

with open("sp.html", "r", encoding="utf-8") as f:
    html_content = f.read()

st.components.v1.html(html_content, height=1800, scrolling=True)
