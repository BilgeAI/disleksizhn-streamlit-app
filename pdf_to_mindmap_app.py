
import streamlit as st
import fitz  # PyMuPDF
import networkx as nx
import matplotlib.pyplot as plt
import re

st.title("📄→🧠 PDF'ten Zihin Haritası Oluşturucu")

uploaded_file = st.file_uploader("PDF dosyanızı yükleyin", type=["pdf"])
if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    st.subheader("📜 PDF Metni (İlk 1000 karakter)")
    st.text(full_text[:1000] + "..." if len(full_text) > 1000 else full_text)

    # Metinden anahtar başlıkları çıkar (örnek: büyük/küçük harfle başlayan satırlar)
    lines = full_text.split("\n")
    candidates = [line.strip() for line in lines if 3 < len(line.strip()) < 80]
    headings = [line for line in candidates if line == line.title() or line.isupper()]
    headings = list(dict.fromkeys(headings))  # tekrarları kaldır

    if headings:
        st.subheader("🧠 Zihin Haritası (Başlıklar Arası Bağlantı)")
        G = nx.Graph()
        for i in range(len(headings)-1):
            G.add_edge(headings[i], headings[i+1])
        fig, ax = plt.subplots(figsize=(10, 6))
        nx.draw(G, with_labels=True, node_color='skyblue', node_size=1800, font_size=10, edge_color='gray', ax=ax)
        st.pyplot(fig)
    else:
        st.warning("Başlık benzeri bir yapı bulunamadı. PDF farklı formatta olabilir.")
