import streamlit as st
import fitz  # PyMuPDF
import io
from PIL import Image

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(page_title="📄 PDF Preview & Converter", layout="wide")

# -------------------------------
# SIDEBAR
# -------------------------------
with st.sidebar:
    st.title("📚 PDF Utility App")
    st.markdown("Upload a PDF to:")
    st.markdown("- Preview pages 📖")
    st.markdown("- Convert pages to JPG 🖼️")
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit + PyMuPDF")

# -------------------------------
# MAIN AREA
# -------------------------------
st.title("📄 PDF Upload and Preview Tool")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)

    # --- PREVIEW SETTINGS ---
    st.success(f"✅ PDF loaded successfully! Total pages: {total_pages}")
    view_mode = st.radio("Choose mode:", ["📖 Preview Page", "🖼️ Convert to JPG"], horizontal=True)

    if view_mode == "📖 Preview Page":
        selected_page = st.slider("Select a page to preview", 1, total_pages, 1)

        page = doc[selected_page - 1]
        zoom = 2
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img_bytes = pix.tobytes("png")

        st.image(img_bytes, caption=f"Page {selected_page}", use_column_width=True)

    elif view_mode == "🖼️ Convert to JPG":
        st.info("Converting all PDF pages to JPG...")

        for i in range(total_pages):
            page = doc[i]
            mat = fitz.Matrix(2, 2)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            st.image(img, caption=f"🖼️ Page {i + 1}", use_column_width=True)

        st.success("✅ Conversion complete!")

else:
    st.info("📤 Upload a PDF file from the sidebar to begin.")
