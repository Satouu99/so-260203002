# scheduler.py — mini-scheduler FCFS, SJF, RR, Priority
# Python 3.x | collections.deque untuk RR
from collections import deque

# Dataset campuran — sesuai instruksi slide
# Format: (nama, arrival_time, burst_time, priority)
PROSES = [
    ("P1", 0, 5, 3),
    ("P2", 1, 3, 1),
    ("P3", 2, 8, 4),
    ("P4", 3, 6, 2),
    ("P5", 4, 4, 5),
]

def tampil_tabel(hasil, judul):
    print(f"\n{'='*60}")
    print(f"  {judul}")
    print(f"{'='*60}")
    print(f"{'Proses':<8} {'AT':>4} {'BT':>4} {'CT':>5} {'TAT':>5} {'WT':>5} {'RT':>5}")
    print("-"*60)
    total_tat = total_wt = total_rt = 0
    for r in hasil:
        print(f"{r['nama']:<8} {r['at']:>4} {r['bt']:>4} {r['ct']:>5} {r['tat']:>5} {r['wt']:>5} {r['rt']:>5}")
        total_tat += r['tat']
        total_wt  += r['wt']
        total_rt  += r['rt']
    n = len(hasil)
    print("-"*60)
    print(f"{'Rata-rata':<8} {'':>4} {'':>4} {'':>5} {total_tat/n:>5.2f} {total_wt/n:>5.2f} {total_rt/n:>5.2f}")

# ── FCFS ────────────────────────────────────────────────────
def fcfs(proses):
    urut = sorted(proses, key=lambda x: x[1])  # sort by AT
    waktu = 0
    hasil = []
    for nama, at, bt, pr in urut:
        mulai = max(waktu, at)
        selesai = mulai + bt
        tat = selesai - at
        wt  = tat - bt
        rt  = mulai - at
        waktu = selesai
        hasil.append({"nama": nama, "at": at, "bt": bt, "ct": selesai,
                       "tat": tat, "wt": wt, "rt": rt})
    return hasil

# ── SJF (non-preemptive) ────────────────────────────────────
def sjf(proses):
    sisa   = list(proses)
    waktu  = 0
    hasil  = []
    selesai = []
    while sisa:
        tersedia = [p for p in sisa if p[1] <= waktu]
        if not tersedia:
            waktu = min(p[1] for p in sisa)
            continue
        pilih = min(tersedia, key=lambda x: x[2])
        sisa.remove(pilih)
        nama, at, bt, pr = pilih
        mulai   = waktu
        selesai_t = mulai + bt
        tat = selesai_t - at
        wt  = tat - bt
        rt  = mulai - at
        waktu = selesai_t
        hasil.append({"nama": nama, "at": at, "bt": bt, "ct": selesai_t,
                       "tat": tat, "wt": wt, "rt": rt})
    return hasil

# ── Round Robin ─────────────────────────────────────────────
def round_robin(proses, q):
    urut   = sorted(proses, key=lambda x: x[1])
    antrian = deque()
    waktu  = 0
    sisa_bt = {p[0]: p[2] for p in urut}
    rt_catat = {}
    ct_catat = {}
    indeks   = 0          # pointer proses yang belum masuk antrian
    antrian.append(urut[0])
    indeks = 1

    while antrian:
        nama, at, bt, pr = antrian.popleft()

        # catat response time pertama kali disentuh
        if nama not in rt_catat:
            rt_catat[nama] = max(waktu, at) - at

        eksekusi = min(q, sisa_bt[nama])
        waktu   += eksekusi
        sisa_bt[nama] -= eksekusi

        # masukkan proses baru yang sudah arrive selama eksekusi ini
        while indeks < len(urut) and urut[indeks][1] <= waktu:
            antrian.append(urut[indeks])
            indeks += 1

        if sisa_bt[nama] > 0:
            antrian.append((nama, at, bt, pr))   # kembali ke antrian
        else:
            ct_catat[nama] = waktu

    hasil = []
    for nama, at, bt, pr in urut:
        tat = ct_catat[nama] - at
        wt  = tat - bt
        rt  = rt_catat[nama]
        hasil.append({"nama": nama, "at": at, "bt": bt, "ct": ct_catat[nama],
                       "tat": tat, "wt": wt, "rt": rt})
    return hasil

# ── Priority (non-preemptive, angka kecil = prioritas tinggi) ─
def priority(proses):
    sisa  = list(proses)
    waktu = 0
    hasil = []
    while sisa:
        tersedia = [p for p in sisa if p[1] <= waktu]
        if not tersedia:
            waktu = min(p[1] for p in sisa)
            continue
        pilih = min(tersedia, key=lambda x: x[3])   # sort by priority
        sisa.remove(pilih)
        nama, at, bt, pr = pilih
        mulai     = waktu
        selesai_t = mulai + bt
        tat = selesai_t - at
        wt  = tat - bt
        rt  = mulai - at
        waktu = selesai_t
        hasil.append({"nama": nama, "at": at, "bt": bt, "ct": selesai_t,
                       "tat": tat, "wt": wt, "rt": rt})
    return hasil

# ── Main ─────────────────────────────────────────────────────
if __name__ == "__main__":
    tampil_tabel(fcfs(PROSES),          "FCFS")
    tampil_tabel(sjf(PROSES),           "SJF (Non-Preemptive)")
    tampil_tabel(round_robin(PROSES, 2),"Round Robin (q=2)")
    tampil_tabel(round_robin(PROSES, 4),"Round Robin (q=4)")
    tampil_tabel(priority(PROSES),      "Priority (Non-Preemptive)")
