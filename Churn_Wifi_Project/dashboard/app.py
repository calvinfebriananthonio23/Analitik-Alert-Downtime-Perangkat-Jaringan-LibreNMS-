import streamlit as st
import pandas as pd
import plotly.express as px

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from utils.severity_helper import generate_severity_insight

df = pd.read_csv(
    BASE_DIR / "data" / "processed" / "dashboard_dataset.csv"
)

priority = pd.read_csv(
    BASE_DIR / "data" / "processed" / "priority_maintenance.csv"
)

# KONFIGURASI HALAMAN

st.set_page_config(
    page_title="LibreNMS Analytics Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# LOAD DATA

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "dashboard_dataset.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(
        DATA_PATH,
        low_memory=False
    )

    df["datetime"] = pd.to_datetime(df["datetime"])

    return df


df = load_data()

# HEADER

st.title("📡 LibreNMS Analytics Dashboard")

st.markdown("""
### Analitik Deskriptif Event & Downtime Perangkat Jaringan

Dashboard ini menampilkan hasil analisis data Event Log dari LibreNMS
untuk membantu tim NOC mengidentifikasi perangkat yang membutuhkan
prioritas maintenance.
""")

st.divider()

# SIDEBAR FILTER

st.sidebar.header("🔍 Filter Data")

severity = st.sidebar.multiselect(
    "Severity",
    options=sorted(df["severity"].unique()),
    default=sorted(df["severity"].unique())
)

event_type = st.sidebar.multiselect(
    "Jenis Event",
    options=sorted(df["type_x"].unique()),
    default=sorted(df["type_x"].unique())
)

hardware = st.sidebar.multiselect(
    "Hardware",
    options=sorted(df["hardware"].dropna().unique()),
    default=sorted(df["hardware"].dropna().unique())
)

hari = st.sidebar.multiselect(
    "Hari",
    options=df["Hari"].unique(),
    default=df["Hari"].unique()
)

df = load_data()

df_filtered = df[
    (df["severity"].isin(severity))
    &
    (df["type_x"].isin(event_type))
    &
    (df["hardware"].isin(hardware))
    &
    (df["Hari"].isin(hari))
]

st.info(
    f"Menampilkan {len(df_filtered):,} event dari total {len(df):,} event."
)

# KPI

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "🖥 Total Device",
    df["device_id"].nunique()
)

c2.metric(
    "📑 Total Event",
    len(df)
)

c3.metric(
    "⚠ Jenis Event",
    df["type_x"].nunique()
)

c4.metric(
    "💻 Hardware",
    df["hardware"].nunique()
)

st.divider()

# RINGKASAN ANALISIS

top_device = (
    df_filtered["hostname_y"]
    .value_counts()
    .idxmax()
)

top_device_event = (
    df_filtered["hostname_y"]
    .value_counts()
    .max()
)

top_hardware = (
    df_filtered["hardware"]
    .value_counts()
    .idxmax()
)

top_severity = (
    df_filtered["severity"]
    .value_counts()
    .idxmax()
)

st.success(f"""
### 📌 Ringkasan Analisis

- **Total Device :** {df['device_id'].nunique()}

- **Total Event :** {len(df):,}

- **Perangkat dengan Event Terbanyak :**
  **{top_device}** ({top_device_event:,} event)

- **Hardware Dominan :**
  **{top_hardware}**

- **Severity Dominan :**
  **{top_severity}
""")

# GRAFIK 1

col1, col2 = st.columns(2)

# ---------------- TOP DEVICE ----------------

with col1:

    st.subheader("📊 Top 10 Device dengan Event Terbanyak")

    top_device = (
        df_filtered.groupby("hostname_y")
        .size()
        .reset_index(name="Jumlah Event")
        .sort_values("Jumlah Event", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top_device,
        x="Jumlah Event",
        y="hostname_y",
        orientation="h",
        color="Jumlah Event",
        text="Jumlah Event"
    )

    fig.update_layout(
        yaxis_title="Device",
        xaxis_title="Jumlah Event",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# INSIGHT TOP DEVICE
# ======================================================

device_teratas = top_device.iloc[0]["hostname_y"]
jumlah_event = top_device.iloc[0]["Jumlah Event"]

persentase = (jumlah_event / len(df_filtered)) * 100

st.info(
    f"""
**Insight**

Perangkat **{device_teratas}** menghasilkan **{jumlah_event:,} event**
atau sekitar **{persentase:.1f}%** dari seluruh event yang sedang ditampilkan.

Perangkat ini menjadi prioritas utama untuk dilakukan monitoring dan maintenance.

Perangkat ini merupakan salah satu perangkat dengan jumlah event terbanyak selama periode pengamatan.
Banyaknya event tidak selalu menunjukkan bahwa perangkat mengalami kerusakan,
namun dapat mengindikasikan adanya aktivitas atau perubahan kondisi yang terjadi secara berulang.
Penyebabnya dapat berupa perubahan status interface (up/down), pembaruan sensor monitoring,
tingginya penggunaan CPU, perubahan suhu perangkat, konfigurasi yang belum stabil,
atau karena perangkat tersebut memang menangani trafik jaringan yang lebih besar dibanding perangkat lainnya.

Untuk memastikan penyebab sebenarnya, tim NOC disarankan melakukan pemeriksaan lebih lanjut terhadap log perangkat,
mengevaluasi interface yang sering berubah status, memeriksa kondisi hardware seperti suhu dan kipas, serta memonitor utilisasi CPU dan memori.
Selain itu, perlu dipastikan apakah event yang muncul merupakan gangguan yang benar-benar memerlukan penanganan atau hanya merupakan false alarm yang tidak berdampak terhadap layanan jaringan.

"""
)

# ---------------- TOP HARDWARE ----------------

with col2:

    st.subheader("💻 Top Hardware")

    top_hw = (
        df_filtered.groupby("hardware")
        .size()
        .reset_index(name="Jumlah Event")
        .sort_values("Jumlah Event", ascending=False)
    )

    fig = px.bar(
        top_hw,
        x="hardware",
        y="Jumlah Event",
        color="Jumlah Event",
        text="Jumlah Event"
    )

    fig.update_layout(
        xaxis_title="Hardware",
        yaxis_title="Jumlah Event",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

# INSIGHT TOP HARDWARE

hardware_teratas = top_hw.iloc[0]["hardware"]
hardware_event = top_hw.iloc[0]["Jumlah Event"]

persen_hw = (hardware_event / len(df_filtered)) * 100

st.info(
    f"""
**Insight**

Hardware **{hardware_teratas}** menghasilkan **{hardware_event:,} event**
atau sekitar **{persen_hw:.1f}%** dari seluruh event.

Hardware ini merupakan perangkat yang paling dominan pada data yang sedang dianalisis.

Hardware dengan jumlah event tertinggi tidak selalu menunjukkan bahwa jenis hardware tersebut memiliki kualitas yang buruk atau lebih sering mengalami gangguan.
Tingginya jumlah event dapat dipengaruhi oleh jumlah perangkat yang menggunakan hardware tersebut,
banyaknya layanan yang dijalankan, atau karakteristik perangkat yang secara alami menghasilkan lebih banyak log monitoring.

Oleh karena itu, tim NOC sebaiknya tidak langsung menyimpulkan bahwa hardware tersebut bermasalah.
Analisis perlu dilanjutkan dengan membandingkan jumlah event terhadap jumlah perangkat yang menggunakan hardware yang sama sehingga diperoleh rata-rata event per perangkat.
Apabila jumlah event yang tinggi berasal dari banyak perangkat, kondisi tersebut masih dapat dianggap normal. Namun, jika sebagian besar event hanya berasal dari satu perangkat,
maka perangkat tersebut perlu menjadi prioritas untuk dilakukan investigasi lebih lanjut.
"""
)

# GRAFIK 2

col3, col4 = st.columns(2)

# ---------------- EVENT PER JAM ----------------

with col3:

    st.subheader("📈 Event per Jam")

    event_jam = (
        df_filtered.groupby("Jam")
        .size()
        .reset_index(name="Jumlah Event")
    )

    fig = px.line(
        event_jam,
        x="Jam",
        y="Jumlah Event",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Jam",
        yaxis_title="Jumlah Event"
    )

    st.plotly_chart(fig, use_container_width=True)
    
# INSIGHT EVENT PER JAM

jam_terpadat = event_jam.loc[
    event_jam["Jumlah Event"].idxmax(),
    "Jam"
]

jumlah_jam = event_jam["Jumlah Event"].max()

st.info(
    f"""
**Insight**

Puncak aktivitas event terjadi pada pukul **{jam_terpadat}:00**
dengan total **{jumlah_jam:,} event**.

Jam tersebut merupakan waktu yang paling sibuk sehingga tim NOC
perlu meningkatkan monitoring pada periode tersebut.

Tim NOC disarankan meningkatkan pemantauan pada jam tersebut
serta melakukan analisis terhadap jenis event yang dominan untuk 
memastikan apakah lonjakan merupakan aktivitas normal atau indikasi awal adanya gangguan jaringan.
"""
)

# ---------------- EVENT PER HARI ----------------

with col4:

    st.subheader("📅 Event per Hari")

    urutan_hari = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    event_hari = (
        df_filtered.groupby("Hari")
        .size()
        .reindex(urutan_hari, fill_value=0)
        .reset_index()
    )

    event_hari.columns = ["Hari", "Jumlah Event"]

    fig = px.bar(
        event_hari,
        x="Hari",
        y="Jumlah Event",
        color="Jumlah Event",
        text="Jumlah Event"
    )

    fig.update_layout(
        xaxis_title="Hari",
        yaxis_title="Jumlah Event",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
    
# INSIGHT EVENT PER HARI

hari_terpadat = event_hari.loc[
    event_hari["Jumlah Event"].idxmax(),
    "Hari"
]

jumlah_hari = event_hari["Jumlah Event"].max()

st.info(
    f"""
**Insight**

Jumlah event paling banyak terjadi pada hari **{hari_terpadat}**
sebanyak **{jumlah_hari:,} event**.

Hari tersebut merupakan periode dengan aktivitas jaringan paling tinggi sehingga
tim NOC dapat meningkatkan pengawasan pada hari tersebut.

Tim NOC disarankan memberikan perhatian lebih pada hari Senin
dengan memonitor perangkat dan jenis event yang paling sering muncul,
sehingga potensi gangguan dapat dideteksi lebih awal.
"""
)
    
# PRIORITY MAINTENANCE

st.divider()

st.subheader("🔧 Priority Maintenance")

st.dataframe(
    priority,
    use_container_width=True
)

device_prioritas = priority.iloc[0]["hostname_y"]

score = priority.iloc[0]["Priority_Score"]

st.success(
    f"""
### 🎯 Kesimpulan Analisis

Perangkat **{device_prioritas}** memiliki **Priority Score**
tertinggi sebesar **{score:,}**.

Perangkat ini direkomendasikan menjadi prioritas utama
untuk dilakukan monitoring dan maintenance oleh tim NOC.
"""
)

# SEVERITY DISTRIBUTION

st.divider()

st.subheader("📋 Tingkat Severity Event")

severity_info = pd.DataFrame({
    "Severity": [1, 2, 3, 4, 5],

    "Level": [
        "Information",
        "Status",
        "Operational",
        "Warning",
        "Critical"
    ],

    "Arti": [
        "Informasi normal",
        "Perubahan status perangkat",
        "Aktivitas operasional jaringan",
        "Indikasi gangguan hardware",
        "Gangguan serius yang perlu segera ditangani"
    ],

    "Contoh Event": [
        "BGP Session Up",
        "Device Status Changed",
        "ifOperStatus, Sensor Updated",
        "Temperature, Fanspeed",
        "BGP Session Down, Polling Timeout"
    ],

    "Rekomendasi": [
        "Tidak memerlukan tindakan",
        "Verifikasi apakah perubahan normal",
        "Monitor apabila sering berulang",
        "Periksa kondisi hardware",
        "Segera investigasi oleh Tim NOC"
    ]
})

st.dataframe(
    severity_info,
    use_container_width=True,
    hide_index=True
)

st.info(
"""
### 📖 Cara Membaca Severity

- **Severity 1–2** → Informasi dan perubahan status normal yang umumnya tidak memerlukan tindakan khusus.
- **Severity 3** → Aktivitas operasional jaringan. Perlu dipantau apabila terjadi berulang pada perangkat yang sama.
- **Severity 4** → Peringatan adanya indikasi gangguan perangkat, seperti suhu tinggi atau kecepatan kipas rendah.
- **Severity 5** → Kondisi kritis yang dapat memengaruhi layanan jaringan dan memerlukan investigasi segera oleh Tim NOC.
"""
)

st.divider()

st.subheader("🥧 Severity Distribution")

severity_summary = (
    df_filtered.groupby("severity")
    .size()
    .reset_index(name="Jumlah Event")
)

fig = px.pie(
    severity_summary,
    names="severity",
    values="Jumlah Event",
    title="Distribusi Severity Event"
)

st.plotly_chart(fig, use_container_width=True)
st.info(generate_severity_insight(df_filtered))

# INSIGHT SEVERITY

severity_terbanyak = severity_summary.loc[
    severity_summary["Jumlah Event"].idxmax(),
    "severity"
]

jumlah_severity = severity_summary["Jumlah Event"].max()

persentase = (
    jumlah_severity /
    severity_summary["Jumlah Event"].sum()
) * 100


# DATA EVENT

st.divider()

st.subheader("📄 Data Event")

st.dataframe(
    df_filtered.sort_values("datetime", ascending=False),
    use_container_width=True
)

# DOWNLOAD

csv = df_filtered.to_csv(index=False)

st.download_button(
    label="📥 Download Data Hasil Filter",
    data=csv,
    file_name="dashboard_dataset.csv",
    mime="text/csv"
)

# FOOTER

st.divider()

st.caption(
    """
    📡 LibreNMS Analytics Dashboard

    PKL PT Naraya Telematika

    Dibuat menggunakan Python • Streamlit • Plotly
    """
)
