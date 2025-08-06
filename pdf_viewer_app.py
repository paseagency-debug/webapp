import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import zipfile

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(page_title="📄 PDF Preview & JPG Converter", layout="wide")

# -------------------------------
# SIDEBAR
# -------------------------------
with st.sidebar:
    st.title("📚 PDF Utility App")
    st.markdown("Upload a PDF to:")
    st.markdown("- Preview pages 📖")
    st.markdown("- Convert pages to JPG 🖼️")
    st.markdown("- Download all JPGs as ZIP 📦")
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

    # --- VIEW MODE OPTIONS ---
    st.success(f"✅ PDF loaded! Total pages: {total_pages}")
    view_mode = st.radio("Choose mode:", ["📖 Preview Page", "🖼️ Convert to JPG & Download"], horizontal=True)

    if view_mode == "📖 Preview Page":
        selected_page = st.slider("Select a page to preview", 1, total_pages, 1)

        page = doc[selected_page - 1]
        zoom = 2
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img_bytes = pix.tobytes("png")

        st.image(img_bytes, caption=f"Page {selected_page}", use_column_width=True)

    elif view_mode == "🖼️ Convert to JPG & Download":
        st.info("⏳ Converting all PDF pages to JPG...")

        # Create ZIP in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
            for i in range(total_pages):
                page = doc[i]
                mat = fitz.Matrix(2, 2)
                pix = page.get_pixmap(matrix=mat, alpha=False)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # Save each image to BytesIO and write to ZIP
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format="JPEG")
                zip_file.writestr(f"page_{i+1}.jpg", img_byte_arr.getvalue())

                # Optional preview in UI
                st.image(img, caption=f"🖼️ Page {i + 1}", use_column_width=True)

        st.success("✅ Conversion complete!")

        # Download button
        zip_buffer.seek(0)
        st.download_button(
            label="📦 Download All JPGs as ZIP",
            data=zip_buffer,
            file_name="converted_images.zip",
            mime="application/zip"
        )

else:
    st.info("📤 Upload a PDF file to begin.")
