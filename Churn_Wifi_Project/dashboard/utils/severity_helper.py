import pandas as pd

# DATABASE EVENT

EVENT_INFO = {

    "BGP Session Down": {
        "level": "Critical",
        "arti": "Koneksi BGP antar router terputus.",
        "rekomendasi": [
            "Periksa status peer BGP.",
            "Periksa routing.",
            "Pastikan koneksi WAN normal."
        ]
    },

    "Polling took longer than 5 minutes": {
        "level": "Critical",
        "arti": "LibreNMS gagal melakukan polling perangkat tepat waktu.",
        "rekomendasi": [
            "Periksa server LibreNMS.",
            "Periksa koneksi ke perangkat.",
            "Restart poller jika diperlukan."
        ]
    },

    "Temperature": {
        "level": "Warning",
        "arti": "Sensor suhu melewati batas normal.",
        "rekomendasi": [
            "Periksa suhu ruang server.",
            "Periksa pendingin.",
            "Pastikan airflow baik."
        ]
    },

    "Fanspeed": {
        "level": "Warning",
        "arti": "Kecepatan kipas berada di bawah batas normal.",
        "rekomendasi": [
            "Periksa kipas.",
            "Bersihkan debu.",
            "Pastikan kipas masih bekerja."
        ]
    },

    "ifOperStatus": {
        "level": "Operational",
        "arti": "Status interface jaringan berubah.",
        "rekomendasi": [
            "Periksa interface.",
            "Periksa kabel.",
            "Monitor apabila sering terjadi."
        ]
    },

    "Sensor Updated": {
        "level": "Operational",
        "arti": "Sensor mengirimkan pembaruan data monitoring.",
        "rekomendasi": [
            "Aktivitas monitoring normal.",
            "Periksa bila terjadi sangat sering."
        ]
    },

    "Device status changed": {
        "level": "Status",
        "arti": "Status perangkat berubah menjadi Up atau Down.",
        "rekomendasi": [
            "Pastikan perubahan memang terjadi.",
            "Periksa penyebab perangkat Down."
        ]
    },

    "BGP Session Up": {
        "level": "Information",
        "arti": "Koneksi BGP kembali normal.",
        "rekomendasi": [
            "Tidak diperlukan tindakan."
        ]
    }

}

def cari_info_event(message):
    
    for keyword, info in EVENT_INFO.items():

        if keyword.lower() in message.lower():

            return info

    return {
        "level":"Unknown",
        "arti":"Belum terdapat deskripsi event.",
        "rekomendasi":[
            "Periksa log perangkat."
        ]
    }
    
def generate_severity_insight(df):
    
    # ==========================
    # Hitung jumlah severity
    # ==========================
    severity_chart = (
        df.groupby("severity")
        .size()
        .reset_index(name="Jumlah Event")
    )

    severity_dominan = severity_chart.loc[
        severity_chart["Jumlah Event"].idxmax(),
        "severity"
    ]

    jumlah_event = severity_chart["Jumlah Event"].max()
    total_event = severity_chart["Jumlah Event"].sum()

    persen = jumlah_event / total_event * 100

    # ==========================
    # Ambil event pada severity dominan
    # ==========================
    df_severity = df[df["severity"] == severity_dominan]

    top_event = (
        df_severity["message"]
        .value_counts()
        .head(3)
        .reset_index()
    )

    top_event.columns = ["message", "Jumlah"]

    # ==========================
    # Cari informasi event utama
    # ==========================
    event_utama = top_event.iloc[0]["message"]

    info = cari_info_event(event_utama)

    # ==========================
    # Susun daftar Top Event
    # ==========================
    daftar_event = ""

    for _, row in top_event.iterrows():

        daftar_event += (
            f"• {row['message']} "
            f"({row['Jumlah']} event)\n"
        )

    # ==========================
    # Susun rekomendasi
    # ==========================
    rekomendasi = ""

    for item in info["rekomendasi"]:

        rekomendasi += f"• {item}\n"

    # ==========================
    # Insight
    # ==========================
    insight = f"""
### 📊 Insight Severity

Severity yang paling dominan adalah **Severity {severity_dominan}**
dengan total **{jumlah_event:,} event**
({persen:.1f}% dari seluruh event).

### 🔍 Top Event

{daftar_event}

### 📖 Makna

{info['arti']}

### 🔧 Rekomendasi Tim NOC

{rekomendasi}
"""

    return insight