import streamlit as st
import time

# --- MOBİL ODAKLI TEMİZ AYARLAR ---
st.set_page_config(page_title="TKM Hızlı", layout="centered")

# Gereksiz boşlukları ve menüleri gizleyen CSS
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stButton>button {
            height: 120px;
            font-size: 50px !important;
            border-radius: 20px;
        }
        .skor-text { font-size: 30px; font-weight: bold; text-align: center; }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_db():
    return {"p1": None, "p2": None, "s1": 0, "s2": 0}

db = get_db()

# --- ROL SEÇİMİ (Sadece ilk girişte) ---
if "rol" not in st.session_state:
    st.subheader("Rolünü Seç:")
    c1, c2 = st.columns(2)
    if c1.button("OYUNCU 1"): st.session_state.rol = "p1"; st.rerun()
    if c2.button("OYUNCU 2"): st.session_state.rol = "p2"; st.rerun()
    st.stop()

rol = st.session_state.rol
rakip = "p2" if rol == "p1" else "p1"

# --- SKOR PANELİ ---
st.markdown(f"<div class='skor-text'>🔴 {db['s1']}  —  🔵 {db['s2']}</div>", unsafe_allow_html=True)
st.divider()

# --- OYUN MANTIĞI ---
if db["p1"] and db["p2"]:
    # Sonuç Hesaplama
    p1, p2 = db["p1"], db["p2"]
    win_map = {"🪨": "✂️", "📄": "🪨", "✂️": "📄"}
    
    if p1 == p2:
        st.warning(f"BERABERE! ({p1} vs {p2})")
    elif win_map[p1] == p2:
        if "counted" not in st.session_state: db["s1"] += 1; st.session_state.counted = True
        st.success(f"P1 KAZANDI! {p1} > {p2}")
    else:
        if "counted" not in st.session_state: db["s2"] += 1; st.session_state.counted = True
        st.info(f"P2 KAZANDI! {p2} > {p1}")

    if st.button("YENİ TUR 🔄", use_container_width=True):
        db["p1"], db["p2"] = None, None
        if "counted" in st.session_state: del st.session_state.counted
        st.rerun()

elif db[rol] is None:
    st.write(f"Sıra Sende: **{rol.upper()}**")
    col1, col2, col3 = st.columns(3)
    if col1.button("🪨"): db[rol] = "🪨"; st.rerun()
    if col2.button("📄"): db[rol] = "📄"; st.rerun()
    if col3.button("✂️"): db[rol] = "✂️"; st.rerun()

else:
    st.write("⌛ Rakip hamlesi bekleniyor...")
    time.sleep(1)
    st.rerun()
