import streamlit as st
from PIL import Image
import os
import uuid
from database import Session, Book
from faiss_store import build_index, search
import numpy as np

st.set_page_config(page_title="Smart Library Vision Ultra", layout="wide")

# Custom CSS for Attractive UI
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
h1 {
    color: #1f4e79;
}
.stButton>button {
    background-color: #1f4e79;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 Smart Library Vision Ultra")
st.markdown("### AI-Powered Book Recognition & Library Management")

session = Session()

# Sidebar Menu
menu = st.sidebar.selectbox("Navigation", ["Search Book", "Live Webcam Search", "Add New Book"])

# Build FAISS index once
if "index_ready" not in st.session_state:
    build_index()
    st.session_state.index_ready = True

# ---------------- SEARCH BOOK ----------------
if menu == "Search Book":

    st.subheader("Upload Book Cover")

    uploaded_file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption="Uploaded Image", width=300)

        match_file, distance = search(image)

        if match_file:
            confidence = max(0, 100 - distance)

            if confidence > 60:
                book = session.query(Book).filter(
                    Book.image_path == f"covers/{match_file}"
                ).first()

                with col2:
                    matched_image = Image.open(f"covers/{match_file}")
                    st.image(matched_image, caption="Matched Book", width=300)

                st.success("✅ Book Found in Library")
                st.write(f"**Title:** {book.title}")
                st.write(f"**Author:** {book.author}")
                st.write(f"**Genre:** {book.genre}")
                st.write(f"**Shelf:** {book.shelf}")
                st.write(f"**Confidence:** {round(confidence,2)}%")
            else:
                st.error("❌ Book Not Found")
        else:
            st.error("Library is empty.")

# ---------------- LIVE WEBCAM ----------------
elif menu == "Live Webcam Search":

    st.subheader("Capture Book Using Webcam")

    camera_image = st.camera_input("Take a picture")

    if camera_image:
        image = Image.open(camera_image).convert("RGB")
        st.image(image, width=300)

        match_file, distance = search(image)

        if match_file:
            confidence = max(0, 100 - distance)

            if confidence > 60:
                book = session.query(Book).filter(
                    Book.image_path == f"covers/{match_file}"
                ).first()

                matched_image = Image.open(f"covers/{match_file}")
                st.image(matched_image, caption="Matched Book", width=300)

                st.success("✅ Book Found in Library")
                st.write(f"**Title:** {book.title}")
                st.write(f"**Author:** {book.author}")
                st.write(f"**Genre:** {book.genre}")
                st.write(f"**Shelf:** {book.shelf}")
                st.write(f"**Confidence:** {round(confidence,2)}%")
            else:
                st.error("❌ Book Not Found")

# ---------------- ADD BOOK ----------------
elif menu == "Add New Book":

    st.subheader("Add New Book to Library")

    title = st.text_input("Book Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    shelf = st.text_input("Shelf Location")
    image_file = st.file_uploader("Upload Book Cover", type=["jpg","png","jpeg"])

    if st.button("Add Book"):

        if title and author and genre and shelf and image_file:

            if not os.path.exists("covers"):
                os.makedirs("covers")

            unique_name = str(uuid.uuid4()) + ".jpg"
            image_path = os.path.join("covers", unique_name)

            image = Image.open(image_file)
            image.save(image_path)

            book = Book(
                title=title,
                author=author,
                genre=genre,
                shelf=shelf,
                image_path=image_path
            )

            session.add(book)
            session.commit()

            build_index()

            st.success("✅ Book Added Successfully!")
        else:
            st.warning("Please fill all fields.")