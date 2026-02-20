# Smart Library Vision Ultra

Smart Library Vision Ultra is an AI-powered visual library management system that enables users to search for books using book cover images instead of traditional text-based queries. The system uses deep learning for feature extraction and similarity matching, providing an intelligent and modern solution for library search and management.

This project is built entirely in Python using Streamlit for the web interface and PyTorch (ResNet50) for computer vision-based feature extraction.

---

## Project Overview

Traditional library systems rely on searching by title, author, or ISBN. Smart Library Vision Ultra introduces a visual search system where users can:

- Upload a book cover image to find the corresponding book
- Capture a live image using a webcam for real-time recognition
- Add new books dynamically through the web interface
- Store and manage book records in a local database
- View similarity confidence scores for matched results

The system extracts deep visual features from book cover images and compares them using cosine similarity to identify the most similar book in the database.

---

## Key Features

- Image-based book search
- Live webcam-based recognition
- Add new books through the UI
- Automatic deep feature extraction using ResNet50
- Cosine similarity-based matching
- Confidence score display
- SQLite database integration
- Clean and responsive Streamlit interface
- Scalable design for expanding book collections

---

## Technology Stack

- Python
- Streamlit
- PyTorch (ResNet50 pretrained model)
- Scikit-learn (cosine similarity)
- SQLAlchemy
- SQLite
- Pillow
- NumPy

---

## System Architecture

1. User uploads or captures a book cover image.
2. The image is processed using a pretrained ResNet50 model.
3. Deep feature embeddings are extracted.
4. Stored book cover features are compared using cosine similarity.
5. The best match above a defined threshold is selected.
6. Book metadata is retrieved from the SQLite database.
7. Results are displayed with match confidence.

---

## Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/SmartLibraryVision-Ultra.git
cd SmartLibraryVision-Ultra
```

Replace YOUR_USERNAME with your GitHub username.

---

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt is not available:

```bash
pip install streamlit torch torchvision pillow numpy scikit-learn sqlalchemy requests
```

---

## Running the Application

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

## Project Structure

```
SmartLibraryVisionUltra/
│
├── app.py                # Main Streamlit application
├── database.py           # Database configuration and model
├── image_model.py        # ResNet50 feature extractor
├── faiss_store.py        # Cosine similarity search engine
├── requirements.txt      # Project dependencies
├── library.db            # SQLite database
└── covers/               # Stored book cover images
```

---

## How to Use

### Search Using Image Upload
1. Go to the "Search Book" section.
2. Upload a book cover image.
3. View matched book details and confidence score.

### Search Using Webcam
1. Go to the "Live Webcam Search" section.
2. Capture an image using your camera.
3. View matched results instantly.

### Add New Book
1. Navigate to the "Add New Book" section.
2. Enter book details.
3. Upload the book cover image.
4. Click "Add Book".
5. The system updates the feature index automatically.

---

## Database Schema

The system uses SQLite for local storage.

Book Table Fields:

- id (Primary Key)
- title
- author
- genre
- shelf
- image_path

---

## Future Enhancements

- Role-based authentication
- Cloud database integration
- Large-scale indexing optimization
- Hybrid text and image search
- Docker containerization
- REST API backend
- Analytics dashboard

---

## Academic and Practical Relevance

This project demonstrates:

- Computer vision integration in web applications
- Deep learning-based feature extraction
- Image similarity search systems
- Full-stack Python development
- Database design and integration
- Real-time webcam processing
- Modern UI development using Streamlit

It can be extended for:

- Digital libraries
- Retail product recognition
- Visual inventory management
- Archive digitization systems

---

## Author

Mohamed Mustak M

---

## License

This project is developed for educational and research purposes.