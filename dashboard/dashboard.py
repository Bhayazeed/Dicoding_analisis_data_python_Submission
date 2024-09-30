import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


@st.cache_data
def load_data():
    gabungan_df = pd.read_csv('https://raw.githubusercontent.com/Bhayazeed/Dicoding_analisis_data_python_Submission/refs/heads/main/dashboard/main_data.csv')  
    date_columns = ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']
    for col in date_columns:
        gabungan_df[col] = pd.to_datetime(gabungan_df[col])
    return gabungan_df

gabungan_df = load_data()


orders_2017_df = gabungan_df[gabungan_df['order_purchase_timestamp'].dt.year == 2017]

st.title("Dashboard E-commerce Analysis 2017")

analysis_option = st.sidebar.selectbox(
    "Pilih analisis",("Cicilan customer per Negara Bagian", "Kategori dengan Cicilan >3", "Tingkat Pengiriman Tepat Waktu")
)

if analysis_option == "Cicilan customer per Negara Bagian":
    st.header("Analisis Cicilan customer per Negara Bagian")
    
    cicilan_negara_bagian = orders_2017_df.groupby(['customer_state', 'payment_installments'])['order_id'].count().unstack().fillna(0)
    negara_cicilan_teratas = cicilan_negara_bagian.sum(axis=1).sort_values(ascending=False)
    
    top_n = st.slider("Pilih berapa negara bagian:", 5, 27, 10)
    
    fig1, ax1 = plt.subplots(figsize=(14, 8))
    sns.barplot(x=negara_cicilan_teratas.head(top_n).index, y=negara_cicilan_teratas.head(top_n).values, ax=ax1)
    plt.xlabel('Negara Bagian Pelanggan')
    plt.ylabel('Jumlah Cicilan')
    plt.title(f'Top {top_n} Negara Bagian berdasarkan Cicilan (2017)')
    plt.xticks(rotation=45, ha='right')
    
    for i, nilai in enumerate(negara_cicilan_teratas.head(top_n).values):
        ax1.text(i, nilai, f'{nilai:,.0f}', ha='center', va='bottom')
    
    st.pyplot(fig1)
    
    st.subheader("Hasil Analisis Customer per Negara Bagian:")
    st.write(f"""
    Berdasarkan analisis diatas, Kita dapat mengamati beberapa pola:
    
    1. Pada Negara bagian yang paling sering dilihat adalah Sau Paulo ({negara_cicilan_teratas.index[0]}) yang paling sering dilihat dalam mengambil cicilan.
    2. Terdapat perbedaan signifikan antara negara bagian teratas dan terbawah dalam penggunaan pembayaran cicilan.
    3. Data ini dapat digunakan untuk menyesuaikan strategi pemasaran dan penawaran produk berdasarkan preferensi pembayaran di setiap negara bagian.
             
    Pelanggan di wilayah ini lebih cenderung menggunakan cicilan karena tingginya volume transaksi.Fokus pada promosi cicilan di wilayah ini, dengan opsi cicilan yang menarik untuk meningkatkan penjualan lebih lanjut.         
             """)

elif analysis_option == "Kategori dengan Cicilan >3":
    st.header("Kategori Produk dengan Cicilan >3")
    
    cicilan_category_lebih_3 = orders_2017_df[orders_2017_df['payment_installments'] > 3].groupby('product_category_name_english').size().sort_values(ascending=False)
    
    top_n = st.slider("Pilih top n kategori:", 5, 20, 10)
    
    fig2, ax2 = plt.subplots(figsize=(14, 8))
    sns.barplot(x=cicilan_category_lebih_3.head(top_n).index, y=cicilan_category_lebih_3.head(top_n).values, ax=ax2)
    plt.xlabel('Kategori Produk')
    plt.ylabel('Jumlah Pesanan dengan >3 Cicilan')
    plt.title(f'Top {top_n} Kategori Produk dengan Cicilan >3 kali (2017)')
    plt.xticks(rotation=45, ha='right')
    
    for i, nilai in enumerate(cicilan_category_lebih_3.head(top_n).values):
        ax2.text(i, nilai, f'{nilai:,.0f}', ha='center', va='bottom')
    
    st.pyplot(fig2)
    
    st.subheader("Hasil Analisis Kategori Produk dengan bayaran cicilan lebih dari 3:")
    st.write(f"""
    Berdasarkan analisis diatas, Kita dapat mengamati beberapa pola:
    
    1. Bed, Bath, and Table memiliki cicilan > 3 kali terbanyak, diikuti oleh Health & Beauty, dan Furniture & Decor.
    2. Produk di kategori ini memiliki kecenderungan dibeli dengan cicilan lebih panjang, mungkin karena harganya yang relatif lebih tinggi.
                
    Negara bagian dengan transaksi cicilan tertinggi kemungkinan memiliki pengeluaran yang lebih besar untuk produk premium seperti bed,bath dan table. Ini memperlihatkan preferensi belaja yang lebih matang dan skema cicilan jangka panjang untuk memfasilitasi pembelian barang bernilai lebih tinggi            
                """)

elif analysis_option == "Tingkat Pengiriman Tepat Waktu":
    st.header("Analisis Tingkat Pengiriman Tepat Waktu")
    
    orders_2017_df['delivery_difference'] = (orders_2017_df['order_delivered_customer_date'] - orders_2017_df['order_estimated_delivery_date']).dt.days
    tepat_waktu_bulanan = orders_2017_df.groupby(orders_2017_df['order_purchase_timestamp'].dt.month).apply(lambda df: (df['delivery_difference'] <= 0).mean() * 100)
    
    fig3, ax2 = plt.subplots(figsize=(12, 6))
    sns.barplot(x=tepat_waktu_bulanan.index, y=tepat_waktu_bulanan.values, alpha=0.8, ax=ax2)
    average_tepat_waktu_bulanan = tepat_waktu_bulanan.mean()
    ax2.axhline(y=average_tepat_waktu_bulanan, color='r', linestyle='--', label='Rata-rata Bulanan')
    
    highlight_months = [11, 12]
    for bulan in highlight_months:
        ax2.patches[bulan - 1].set_facecolor('gold')
    
    for i, v in enumerate(tepat_waktu_bulanan.values):
        ax2.text(i, v + 0.5, f'{v:.1f}%', ha='center', va='bottom')
    
    plt.title('Tingkat Pengiriman Tepat Waktu Bulanan pada 2017')
    plt.xlabel('Bulan')
    plt.ylabel('Tingkat Pengiriman Tepat Waktu (%)')
    plt.xticks(range(12), ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
    plt.legend(['Rata-rata Bulanan'])
    
    st.pyplot(fig3)
    
    st.subheader("Hasil Analisis Kategori Produk dengan bayaran cicilan lebih dari 3:")
    st.write(f"""
    Berdasarkan analisis diatas, Kita dapat mengamati beberapa pola:
    
    1. Pada November, terjadi penurunan drastis tingkat pengiriman tepat waktu (87,6%), sementara bulan lain rata-rata di atas 95%.
    2. Ini kemungkinan disebabkan oleh lonjakan pesanan selama periode liburan.
                    
    Penurunan signifikan pada bulan November dapat dipicu oleh lonjakan pesanan akibat promosi besar seperti Black Friday, yang menyebabkan overload pada kapasistas pengiriman                
                    """)









