# Import libraries
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load dataset
file_path = 'data.csv'  # Asumsikan file berada di folder yang sama dengan script

# Load dataset
data = pd.read_csv(file_path)

# Streamlit Title with Header
st.title("Gambaran Umum Keadaan Sekolah Dasar Tiap Provinsi Tahun 2023")
st.markdown("""
### Oleh: Muhammad Alif Ramadhan M. (1301210533)

Dataset ini berisi informasi tentang keadaan sekolah dasar di Indonesia pada tahun 2023 yang mencakup berbagai faktor penting. 
Data yang terkandung di dalamnya meliputi jumlah sekolah, siswa, guru, tenaga kependidikan, dan berbagai indikator lainnya 
di setiap provinsi di Indonesia. Dengan proyek ini, kami bertujuan untuk menyediakan visualisasi interaktif yang memudahkan 
pembaca dalam memahami distribusi dan kondisi pendidikan di seluruh provinsi Indonesia. Aplikasi ini juga memungkinkan eksplorasi 
lebih dalam terhadap berbagai pola yang bisa membantu pengambilan keputusan dalam peningkatan kualitas pendidikan, pemerataan 
akses pendidikan, dan pengelolaan sumber daya yang lebih baik.

Sebagai tujuan utama, proyek ini bertujuan untuk memperkenalkan informasi penting mengenai kualitas pendidikan di tingkat 
sekolah dasar berdasarkan data yang sudah tersedia, serta memberikan gambaran visual yang dapat dijadikan referensi oleh berbagai pihak 
untuk mengidentifikasi peluang dan tantangan dalam sektor pendidikan Indonesia.
""")

# Sidebar Content
st.sidebar.title("Navigasi & Analisis Lainnya")

# Sidebar: Filter untuk Provinsi
provinsi_options = st.sidebar.multiselect(
    "Pilih Provinsi untuk Dilihat:",
    options=data["Provinsi"].unique(),
    default=data["Provinsi"].unique()
)

# Sidebar: Menampilkan data berdasarkan filter Provinsi
filtered_data = data[data["Provinsi"].isin(provinsi_options)]
st.sidebar.markdown("### Data yang Diperbarui Berdasarkan Pilihan Provinsi")
st.sidebar.dataframe(filtered_data)

# Sidebar: Menampilkan statistik deskriptif untuk provinsi terpilih
filtered_desc_stats = filtered_data.describe()
st.sidebar.markdown("### Statistik Deskriptif untuk Provinsi Terpilih")
st.sidebar.write(filtered_desc_stats)

# Menampilkan semua provinsi tanpa filter
st.subheader("Data untuk Semua Provinsi")
st.dataframe(data)
st.markdown("""
Tabel di atas menunjukkan data lengkap mengenai sekolah dasar di seluruh provinsi Indonesia pada tahun 2023. 
Data ini mencakup jumlah sekolah, siswa, ruang kelas, guru, tenaga kependidikan, dan angka putus sekolah. 
Tabel ini dapat digunakan untuk analisis lebih mendalam mengenai kondisi pendidikan di setiap provinsi. 
Anda dapat menyesuaikan tabel ini menggunakan filter yang tersedia di sidebar untuk melihat data spesifik berdasarkan provinsi pilihan Anda.
""")

# Proses Data: Pivot Table untuk Sekolah Negeri dan Swasta
data_pivot = data.pivot_table(
    values="Siswa", 
    index="Provinsi", 
    columns="Status", 
    aggfunc="sum"
).reset_index()

# Mengganti nama kolom untuk mempermudah
data_pivot.columns.name = None
data_pivot.rename(columns={"Negeri": "Sekolah Negeri", "Swasta": "Sekolah Swasta"}, inplace=True)

# Visualisasi 1: Jumlah Siswa per Provinsi 🎓
st.subheader("🎓 Jumlah Siswa per Provinsi")
fig1 = px.bar(
    data,
    x="Provinsi",
    y="Siswa",
    title="Jumlah Siswa per Provinsi",
    labels={"Siswa": "Jumlah Siswa", "Provinsi": "Nama Provinsi"},
    color="Provinsi",
    template="plotly_white"
)
st.plotly_chart(fig1, use_container_width=True)
st.caption("""
Grafik ini menggambarkan distribusi jumlah siswa di setiap provinsi. Provinsi dengan jumlah siswa yang lebih banyak 
menunjukkan populasi sekolah dasar yang lebih besar. Hal ini mengindikasikan tantangan yang lebih besar dalam hal penyediaan 
fasilitas dan tenaga pendidik di provinsi-provinsi tersebut. Peningkatan jumlah siswa di suatu provinsi dapat menjadi petunjuk 
adanya kebutuhan untuk memperbesar kapasitas fasilitas pendidikan dan meningkatkan kualitas sumber daya manusia untuk mengakomodasi 
jumlah siswa yang terus bertambah.
""")

# Visualisasi 2: Perbandingan Jumlah Sekolah dan Ruang Kelas 🏢
st.subheader("🏢 Perbandingan Jumlah Sekolah dan Ruang Kelas")
fig2 = px.scatter(
    data,
    x="Sekolah",
    y="Ruang Kelas",
    size="Siswa",
    color="Provinsi",
    title="Perbandingan Jumlah Sekolah dan Ruang Kelas",
    labels={"Sekolah": "Jumlah Sekolah", "Ruang Kelas": "Jumlah Ruang Kelas"},
    hover_name="Provinsi",
    template="plotly_white"
)
st.plotly_chart(fig2, use_container_width=True)
st.caption("""
Grafik ini menunjukkan hubungan antara jumlah sekolah dan ruang kelas di setiap provinsi. Ukuran titik mewakili jumlah siswa 
di provinsi tersebut. Provinsi yang memiliki banyak sekolah, namun ruang kelas yang terbatas, dapat mengindikasikan masalah 
infrastruktur pendidikan. Misalnya, ruangan yang terbatas bisa memengaruhi kualitas pembelajaran, terutama dalam hal 
keterjangkauan dan kapasitas ruang bagi siswa.
""")

# Visualisasi 3: Korelasi Antarvariabel menggunakan Heatmap
st.subheader("🔍 Korelasi Antarvariabel")
correlation_matrix = data[["Siswa", "Sekolah", "Ruang Kelas", "Kepala Sekolah & Guru", "Tenaga Kependidikan", "Putus Sekolah"]].corr()

# Plot Heatmap
fig, ax = plt.subplots(figsize=(10, 7))  # Membuat objek figure dan axis
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)  # Menambahkan parameter 'ax'
st.pyplot(fig)  # Menyertakan 'fig' saat memanggil st.pyplot()
st.caption("""
Heatmap ini menunjukkan korelasi antar berbagai variabel dalam data pendidikan, seperti jumlah siswa, jumlah sekolah, ruang kelas, 
jumlah tenaga pendidik, dan angka putus sekolah. Korelasi yang tinggi antara dua variabel dapat memberikan insight tentang bagaimana 
hubungan antara faktor-faktor ini dapat mempengaruhi kualitas pendidikan.
""")

# Dashboard untuk Navigasi Multi-Metrik
tabs = st.tabs(["Infrastruktur Sekolah", "Tenaga Pendidik", "Angka Putus Sekolah"])

with tabs[0]:
    st.subheader("🏢 Infrastruktur Sekolah")
    # Visualisasi terkait Infrastruktur Sekolah
    fig_infrastructure = px.scatter(
        data,
        x="Sekolah",
        y="Ruang Kelas",
        size="Siswa",
        color="Provinsi",
        title="Perbandingan Jumlah Sekolah dan Ruang Kelas per Provinsi",
        template="plotly_white"
    )
    st.plotly_chart(fig_infrastructure, use_container_width=True)

with tabs[1]:
    st.subheader("👩‍🏫 Tenaga Pendidik")
    # Visualisasi terkait Tenaga Pendidik
    fig_teachers = px.bar(
        data,
        x="Provinsi",
        y=["Kepala Sekolah & Guru", "Tenaga Kependidikan"],
        title="Jumlah Guru dan Tenaga Kependidikan per Provinsi",
        barmode="group",
        labels={"value": "Jumlah", "variable": "Jenis"},
        template="plotly_white"
    )
    st.plotly_chart(fig_teachers, use_container_width=True)

with tabs[2]:
    st.subheader("❌ Angka Putus Sekolah")
    # Visualisasi terkait Angka Putus Sekolah
    fig_dropout = px.bar(
        data,
        x="Provinsi",
        y="Putus Sekolah",
        title="Angka Putus Sekolah Berdasarkan Provinsi",
        labels={"Putus Sekolah": "Jumlah Putus Sekolah", "Provinsi": "Nama Provinsi"},
        color="Putus Sekolah",
        template="plotly_white"
    )
    st.plotly_chart(fig_dropout, use_container_width=True)

# Menampilkan Tabel Interaktif dan Statistik Terakhir
st.subheader("📊 Statistik dan Tabel Terakhir")
st.markdown("""
Di bawah ini adalah tabel interaktif dan statistik deskriptif terkait data yang telah dipilih. Anda bisa melihat lebih 
lanjut analisis berdasarkan filter provinsi yang telah dipilih sebelumnya.
""")
# Tabel interaktif menggunakan st.dataframe
st.dataframe(filtered_data)

# Statistik deskriptif berdasarkan pilihan provinsi
st.markdown("### Statistik Deskriptif untuk Provinsi Terpilih")
st.write(filtered_desc_stats)

# Kesimpulan
st.subheader("📍 Kesimpulan")

st.markdown("""
Berdasarkan visualisasi dan analisis yang telah dilakukan, kita dapat menarik beberapa kesimpulan mengenai keadaan pendidikan 
sekolah dasar di Indonesia pada tahun 2023. Beberapa hal yang dapat diperhatikan antara lain:

1. **Distribusi Siswa dan Sekolah**: Terdapat variasi yang cukup besar antara provinsi dalam jumlah siswa dan sekolah. Provinsi-provinsi dengan jumlah siswa yang lebih banyak cenderung memiliki tantangan lebih besar dalam hal infrastruktur pendidikan dan kebutuhan akan guru serta tenaga pendidik yang berkualitas.

2. **Keterbatasan Ruang Kelas**: Meskipun beberapa provinsi memiliki jumlah sekolah yang banyak, jumlah ruang kelas yang terbatas menunjukkan adanya ketidakseimbangan infrastruktur yang dapat mempengaruhi kualitas pendidikan. Oleh karena itu, peningkatan kapasitas ruang kelas sangat diperlukan di provinsi-provinsi tertentu.

3. **Korelasi antara Variabel**: Analisis korelasi menunjukkan hubungan yang signifikan antara jumlah siswa, jumlah sekolah, dan keberadaan tenaga pendidik. Provinsi dengan angka putus sekolah yang tinggi cenderung memiliki lebih sedikit tenaga kependidikan, yang menunjukkan betapa pentingnya keberadaan tenaga pendidik dalam mendukung kelancaran pendidikan dan mengurangi angka putus sekolah.

4. **Tantangan dalam Mengurangi Angka Putus Sekolah**: Beberapa provinsi masih menunjukkan angka putus sekolah yang cukup tinggi. Hal ini menunjukkan adanya kebutuhan untuk memperbaiki akses pendidikan dan fasilitas yang ada, serta menyediakan lebih banyak dukungan bagi siswa yang berisiko putus sekolah.

Secara keseluruhan, aplikasi ini memberikan gambaran yang lebih jelas mengenai tantangan dan peluang yang ada dalam sektor pendidikan Indonesia. Dengan visualisasi interaktif ini, pihak berwenang dan pengambil keputusan dapat merumuskan kebijakan yang lebih tepat sasaran dalam upaya meningkatkan kualitas pendidikan di seluruh provinsi.
""")

# End of Streamlit app
