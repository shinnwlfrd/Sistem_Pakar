import tkinter as tk
from tkinter import font, ttk

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
    # Probabilitas gejala JIKA terkena P1 (Busuk Akar)
    'P1': {
        'G1': 0.7, 'G2': 0.9, 'G3': 0.6, 'G4': 0.1, 'G5': 0.4,
        'G6': 0.5, 'G7': 0.6, 'G8': 0.1, 'G9': 0.2  # Baru
    },
    
    # Probabilitas gejala JIKA terkena P2 (Bercak Daun)
    'P2': {
        'G1': 0.4, 'G2': 0.05, 'G3': 0.1, 'G4': 0.9, 'G5': 0.2,
        'G6': 0.1, 'G7': 0.3, 'G8': 0.8, 'G9': 0.1  # Baru
    },
    
    # Probabilitas gejala JIKA terkena P3 (Layu Bakteri)
    'P3': {
        'G1': 0.5, 'G2': 0.1, 'G3': 0.5, 'G4': 0.2, 'G5': 0.9,
        'G6': 0.7, 'G7': 0.7, 'G8': 0.1, 'G9': 0.6  # Baru
    }
}

# === 2. LOGIKA DIAGNOSA ===
def diagnosa(gejala_teramati: list) -> dict:
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
        return prior
    return posterior_normalized

# === 3. GUI FUNGSIONALITAS ===
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def jalankan_diagnosa():
    clear_frame(output_gejala_frame)
    clear_frame(output_prob_frame)
    clear_frame(output_result_frame)

    gejala_teramati = [kode for kode, var in gejala_vars.items() if var.get()]

    if not gejala_teramati:
        ttk.Label(output_result_frame, text="❗ Silakan pilih minimal satu gejala.", foreground="red").pack(anchor='w', pady=5)
        return

    hasil_probabilitas = diagnosa(gejala_teramati)
    most_likely_kode = max(hasil_probabilitas, key=hasil_probabilitas.get)

    # Tampilan hasil
    ttk.Label(output_gejala_frame, text="🩺 Gejala yang Dipilih:", style="Bold.TLabel").pack(anchor='w', pady=(0,5))
    for g_kode in gejala_teramati:
        ttk.Label(output_gejala_frame, text=f"• {gejala[g_kode]}").pack(anchor='w')

    ttk.Label(output_prob_frame, text="\n📊 Probabilitas Tiap Penyakit:", style="Bold.TLabel").pack(anchor='w')
    for p_kode, prob in hasil_probabilitas.items():
        ttk.Label(output_prob_frame, text=f"• {penyakit[p_kode]} → {prob:.2%}").pack(anchor='w')

    ttk.Label(output_result_frame, text="\n🌱 Diagnosa Akhir:", style="Bold.TLabel").pack(anchor='w')
    ttk.Label(output_result_frame, text=f"{penyakit[most_likely_kode]}", style="Result.TLabel").pack(anchor='w')
    ttk.Label(output_result_frame, text=f"(Probabilitas: {hasil_probabilitas[most_likely_kode]:.2%})", foreground="#555").pack(anchor='w')

  
# === 4. TAMPILAN GUI ===
root = tk.Tk()
root.title("🌿 Sistem Pakar Penyakit Cengkeh")
root.geometry("700x600")
root.configure(bg="#f5f7f9")

# Gaya umum
style = ttk.Style()
style.theme_use("clam")

# Warna & font tema
PRIMARY = "#2E8B57"  # hijau elegan
SECONDARY = "#E9F3EF"
ACCENT = "#4CAF50"

style.configure("TLabel", background="#f5f7f9", font=("Segoe UI", 10))
style.configure("Bold.TLabel", background="#f5f7f9", font=("Segoe UI", 10, "bold"))
style.configure("Title.TLabel", background="#f5f7f9", font=("Segoe UI", 14, "bold"), foreground=PRIMARY)
style.configure("Result.TLabel", background="#f5f7f9", font=("Segoe UI", 12, "bold"), foreground=PRIMARY)
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
style.map("TButton", background=[("active", PRIMARY)], foreground=[("active", "white")])

# Frame utama
container = ttk.Frame(root, padding=20)
container.pack(fill="both", expand=True)

title_label = ttk.Label(container, text="🌿 Sistem Pakar Diagnosa Penyakit Tanaman Cengkeh", style="Title.TLabel")
title_label.pack(pady=(0,15))

# Input card
input_card = ttk.Frame(container, padding=15, style="Card.TFrame")
input_card.pack(fill="x", pady=10)
style.configure("Card.TFrame", background=SECONDARY, relief="ridge")

ttk.Label(input_card, text="Pilih Gejala yang Teramati:", style="Bold.TLabel").pack(anchor='w', pady=(0,5))

gejala_vars = {}
for kode, deskripsi in gejala.items():
    var = tk.BooleanVar()
    cb = ttk.Checkbutton(input_card, text=f"{deskripsi}", variable=var)
    cb.pack(anchor='w', padx=10)
    gejala_vars[kode] = var

# Tombol Diagnosa
btn_diagnosa = ttk.Button(container, text="🔍 Jalankan Diagnosa", command=jalankan_diagnosa)
btn_diagnosa.pack(fill="x", pady=15)

# Output card
output_card = ttk.Frame(container, padding=15, style="Card.TFrame")
output_card.pack(fill="both", expand=True, pady=10)

ttk.Label(output_card, text="Hasil Diagnosa", style="Title.TLabel").pack(pady=(0,10))

output_gejala_frame = ttk.Frame(output_card)
output_gejala_frame.pack(fill='x', anchor='w')

output_prob_frame = ttk.Frame(output_card)
output_prob_frame.pack(fill='x', anchor='w')

output_result_frame = ttk.Frame(output_card)
output_result_frame.pack(fill='x', anchor='w')

root.mainloop()
