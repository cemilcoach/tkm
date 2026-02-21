import streamlit as st
import time

# --- SAYFA AYARLARI (MOBİL İÇİN) ---
st.set_page_config(
    page_title="TKM Arena",
    page_icon="🥊",
    layout="centered", # Mobilde içeriği ortalar
    initial_sidebar_state="collapsed" # Yan menüyü gizle
)

# --- CSS İLE MOBİL GÖRÜNÜMÜ İYİLEŞTİRME ---
# Butonları büyütür ve boşlukları ayarlar.
st.markdown("""
<style>
    .stButton>button {
        height: 3em;
        font-size: 20px;
        font-weight: bold;
    }
    h1 { text-align: center; }
    .stRadio > div { justify-content: center; }
</style>
""", unsafe_allow_html=True)


# --- ORTAK HAFIZA (SUNUCU TARAFI) ---
# Bu kısım, iki farklı telefonun aynı veriyi görmesini sağlar.
@st.cache_resource
def get_shared_state():
    # p1/p2: Oyuncuların hamleleri
    # s1/s2: Skorlar
    # round_over: Tur bitti mi kontrolü (skorun tekrar tekrar artmaması için)
    return {"p1": None, "p2": None, "s1": 0, "s2": 0, "round_over": False}

shared = get_shared_state()

# --- YARDIMCI FONKSİYONLAR ---
def kazananı_bul(p1, p2):
    if p1 == p2: return "Berabere"
    kurallar = {"🪨 Taş": "✂️ Makas", "📄 Kağıt": "🪨 Taş", "✂️ Makas": "📄 Kağıt"}
    if kurallar[p1] == p2: return "P1"
    return "P2"

def hamle_yap(oyuncu_rolu, hamle):
    if oyuncu_rolu == "P1":
        shared["p1"] = hamle
    else:
        shared["p2"] = hamle
    st.rerun()

# --- UYGULAMA BAŞLIYOR ---
st.title("🥊 TKM Arena")
st.caption("Aynı linki arkadaşına gönder. Biriniz P1, diğeriniz P2 olun!")

# 1. ADIM: ROL SEÇİMİ
# Mobilde yan yana sığması için horizontal kullandık.
rol_secimi = st.radio("Önce Kim Olduğunu Seç:", ["🔴 1. Oyuncu (P1)", "🔵 2. Oyuncu (P2)"], horizontal=True)
benim_rolum = "P1" if rol_secimi.startswith("🔴") else "P2"

st.divider()

# SKOR TABLOSU (Her zaman en üstte)
col_s1, col_s2 = st.columns(2)
col_s1.metric("🔴 P1 Skor", shared["s1"])
col_s2.metric("🔵 P2 Skor", shared["s2"])

st.divider()

# --- OYUN MANTIĞI ---

# DURUM 1: İki oyuncu da hamle yaptıysa SONUCU GÖSTER
if shared["p1"] is not None and shared["p2"] is not None:
    if not shared["round_over"]:
        # Sonucu hesapla ve skoru güncelle (sadece 1 kez)
        sonuc = kazananı_bul(shared["p1"], shared["p2"])
        if sonuc == "P1": shared["s1"] += 1
        elif sonuc == "P2": shared["s2"] += 1
        shared["round_over"] = True # Tur bitti olarak işaretle

    st.subheader("🏁 Tur Sonucu")
    
    # Sonuçları görselleştir
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.markdown(f"**🔴 P1 Hamlesi:**")
        st.write(f"### {shared['p1']}")
    with res_col2:
        st.markdown(f"**🔵 P2 Hamlesi:**")
        st.write(f"### {shared['p2']}")
    
    sonuc_final = kazananı_bul(shared["p1"], shared["p2"])
    if sonuc_final == "Berabere":
        st.warning("🤝 Berabere!")
    elif sonuc_final == benim_rolum:
        st.balloons() # Kazananın ekranında balonlar
        st.success("🎉 KAZANDIN!")
    else:
        st.error("💀 KAYBETTİN!")

    # Yeni tur butonu (Mobilde tam genişlikte)
    if st.button("🔄 Yeni Tur Başlat", type="primary", use_container_width=True):
        shared["p1"] = None
        shared["p2"] = None
        shared["round_over"] = False
        st.rerun()

# DURUM 2: Oyun devam ediyor, hamle bekleniyor
else:
    benim_hamlem = shared["p1"] if benim_rolum == "P1" else shared["p2"]
    rakip_hamlesi = shared["p2"] if benim_rolum == "P1" else shared["p1"]

    # Alt Durum 2a: Ben henüz hamle yapmadım
    if benim_hamlem is None:
        st.subheader("⚡ Hamleni Yap!")
        # Mobilde kolay tıklama için büyük ve yan yana butonlar
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        if btn_col1.button("🪨", use_container_width=True): hamle_yap(benim_rolum, "🪨 Taş")
        if btn_col2.button("📄", use_container_width=True): hamle_yap(benim_rolum, "📄 Kağıt")
        if btn_col3.button("✂️", use_container_width=True): hamle_yap(benim_rolum, "✂️ Makas")
    
    # Alt Durum 2b: Ben yaptım, rakibi bekliyorum
    else:
        st.info(f"✅ Hamlen ({benim_hamlem}) alındı.")
        st.warning("⏳ Rakip bekleniyor... Ekran otomatik yenilenecek.")
        # Rakip hamle yapana kadar her 1.5 saniyede bir sayfayı yenile
        time.sleep(1.5)
        st.rerun()
