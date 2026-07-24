# 📡 Dashboard Analitik Deskriptif Alert & Downtime Perangkat Jaringan (LibreNMS)

## Deskripsi

Project ini merupakan hasil Praktik Kerja Lapangan (PKL) di PT Naraya Telematika yang bertujuan melakukan analisis deskriptif terhadap data event perangkat jaringan yang diperoleh dari LibreNMS.

Dashboard dikembangkan menggunakan Python dan Streamlit sehingga data dapat divisualisasikan secara interaktif untuk membantu tim Network Operation Center (NOC) dalam melakukan monitoring serta menentukan prioritas maintenance perangkat jaringan.

# Tujuan

- Menganalisis aktivitas event perangkat jaringan.
- Mengetahui perangkat dengan jumlah event terbanyak.
- Mengetahui pola waktu terjadinya event.
- Mengetahui distribusi tingkat severity.
- Menentukan prioritas maintenance perangkat jaringan.
- Menyediakan dashboard monitoring interaktif.

# Fitur Dashboard

Dashboard memiliki beberapa fitur utama:

- Executive Summary
- KPI Monitoring
- Filter berdasarkan:
  - Jenis Event
  - Severity
- Top Device
- Top Hardware
- Event per Jam
- Event per Hari
- Severity Distribution
- Priority Maintenance
- Data Event
- Download Data CSV

# Dataset

Dataset diperoleh dari LibreNMS API, kemudian diproses menggunakan Python.

Dataset utama terdiri dari:

- devices.csv
- eventlog.csv

Selanjutnya dilakukan proses:

- Data Cleaning
- Data Merging
- Feature Engineering
- Exploratory Data Analysis (EDA)

Hasil akhir menghasilkan:

- dashboard_dataset.csv
- top_device.csv
- top_hardware.csv
- event_per_jam.csv
- event_per_hari.csv
- severity_distribution.csv
- priority_maintenance.csv
- top_message.csv

# Struktur Folder

Churn_Wifi_Project
│
├── assets
│     ├── dashboard_home.png
│     ├── dashboard_filter.png
│     └── priority.png
│
├── dashboard
│   ├── utils
│   │     ├── _pycache_
│   │     │     ├── __init__.cpython-314.pyc
│   │     │     └── severity_helper.cpython-314.pyc
│   │     ├── _init_.py
│   │     └── severity_helper.py
│   │
│   └── app.py
│
├── scripts
│    └── api
│       ├── eda.py
│       ├── cleaning.py
│       └── quality_assessment.py
│
├── data
│   ├── raw
│   │   ├── alerts_full.csv
│   │   ├── devices.csv
│   │   ├── eventlog_full.csv
│   └── processed
│       ├── dashboard_dataset.csv
│       ├── top_device.csv
│       ├── top_hardware.csv
│       ├── event_per_jam.csv
│       ├── event_per_hari.csv
│       ├── severity_distribution.csv
│       ├── priority_maintenance.csv
│       ├── top_message.csv
│       └── dataset_final.csv
│
├── check_severity.py
├── requirements.txt
└── README.md

# Teknologi

Project ini menggunakan:

- Python
- Pandas
- Plotly
- Streamlit
- LibreNMS API

# Cara Menjalankan

## Clone Repository

```bash
git clone <repository-url>

Masuk ke folder project

```bash
cd Churn_Wifi_Project

Install library

```bash
pip install -r requirements.txt

Jalankan dashboard

```bash
streamlit run dashboard/app.py

# Hasil Dashboard

Dashboard menampilkan informasi berupa:

- Total Device
- Total Event
- Jenis Event
- Severity
- Top Device
- Top Hardware
- Event per Jam
- Event per Hari
- Priority Maintenance

Dashboard juga mendukung filtering data secara interaktif.

# Insight Analisis

Beberapa insight yang dihasilkan antara lain:

- Mengetahui perangkat yang paling sering menghasilkan event.
- Menentukan jam paling sibuk berdasarkan aktivitas event.
- Mengetahui hari dengan aktivitas event tertinggi.
- Menentukan distribusi severity event.
- Menentukan perangkat dengan prioritas maintenance tertinggi.

# Pengembangan Selanjutnya

Beberapa pengembangan yang dapat dilakukan:

- Integrasi database MySQL/PostgreSQL.
- Auto-refresh data dari LibreNMS API.
- Notifikasi Telegram atau Email.
- Prediksi downtime menggunakan Machine Learning.
- Prediksi anomaly detection.

# Author

Nama : Calvin Febrian Anthonio

Program Studi Fisika

Universitas Brawijaya

PKL PT Naraya Telematika