import streamlit as st
from PIL import Image
import os
import uuid
from database import Session, Book
from faiss_store import build_index, search

# Page configuration
st.set_page_config(page_title="Smart Library Vision Ultra", layout="wide")

# Custom UI styling
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

st.title("Smart Library Vision Ultra")
st.write("AI-Powered Visual Book Recognition System")

session = Session()

# Build feature index once
if "index_ready" not in st.session_state:
    build_index()
    st.session_state.index_ready = True

# Sidebar navigation
menu = st.sidebar.selectbox(
    "Navigation",
    ["Search Book (Upload)", "Search Book (Webcam)", "Add New Book"]
)

# Strict threshold for exact matching
STRICT_THRESHOLD = 0.95


# ---------------------------------------------------
# SEARCH USING UPLOAD
# ---------------------------------------------------
if menu == "Search Book (Upload)":

    st.subheader("Upload Book Cover")

    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption="Uploaded Image", width=300)

        match_file, best_score = search(image)

        st.write("Similarity Score:", round(best_score, 4))

        if match_file and best_score >= STRICT_THRESHOLD:
            book = session.query(Book).filter(
                Book.image_path == f"covers/{match_file}"
            ).first()

            if book:
                with col2:
                    matched_image = Image.open(f"covers/{match_file}")
                    st.image(matched_image, caption="Matched Book", width=300)

                st.success("Book Found")
                st.write("Title:", book.title)
                st.write("Author:", book.author)
                st.write("Genre:", book.genre)
                st.write("Shelf:", book.shelf)
        else:
            st.error("Book Not Found")


# ---------------------------------------------------
# SEARCH USING WEBCAM
# ---------------------------------------------------
elif menu == "Search Book (Webcam)":

    st.subheader("Capture Book Using Webcam")

    camera_image = st.camera_input("Take a picture")

    if camera_image:
        image = Image.open(camera_image).convert("RGB")

        st.image(image, caption="Captured Image", width=300)

        match_file, best_score = search(image)

        st.write("Similarity Score:", round(best_score, 4))

        if match_file and best_score >= STRICT_THRESHOLD:
            book = session.query(Book).filter(
                Book.image_path == f"covers/{match_file}"
            ).first()

            if book:
                matched_image = Image.open(f"covers/{match_file}")
                st.image(matched_image, caption="Matched Book", width=300)

                st.success("Book Found")
                st.write("Title:", book.title)
                st.write("Author:", book.author)
                st.write("Genre:", book.genre)
                st.write("Shelf:", book.shelf)
        else:
            st.error("Book Not Found")


# ---------------------------------------------------
# ADD NEW BOOK
# ---------------------------------------------------
elif menu == "Add New Book":

    st.subheader("Add New Book to Library")

    title = st.text_input("Book Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    shelf = st.text_input("Shelf Location")
    image_file = st.file_uploader("Upload Book Cover", type=["jpg", "png", "jpeg"])

    if st.button("Add Book"):

        if title and author and genre and shelf and image_file:

            if not os.path.exists("covers"):
                os.makedirs("covers")

            unique_name = str(uuid.uuid4()) + ".jpg"
            image_path = os.path.join("covers", unique_name)

            image = Image.open(image_file).convert("RGB")
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

            # Rebuild index after adding book
            build_index()

            st.success("Book Added Successfully")
        else:
            st.warning("Please fill all fields")
