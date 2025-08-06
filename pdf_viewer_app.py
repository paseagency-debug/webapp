import streamlit as st
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="PDF Viewer", layout="wide")

st.title("📄 PDF Upload and Preview App")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    # Read PDF with PyMuPDF
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        st.success(f"PDF loaded successfully! Total pages: {len(doc)}")
        
        # Choose page number to view
        page_number = st.slider("Select page", 1, len(doc), 1)
        page = doc[page_number - 1]

        # Render page to image
        zoom = 2  # Increase resolution
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        # Convert to byte stream for display
        image_bytes = pix.tobytes("png")
        st.image(image_bytes, caption=f"Page {page_number}", use_column_width=True)
else:
    st.info("Please upload a PDF file to begin.")
