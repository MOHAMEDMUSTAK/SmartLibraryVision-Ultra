import os
import requests
from database import Session, Book
# Create covers folder if not exists
if not os.path.exists("covers"):
    os.makedirs("covers")
# Sample books with ISBN
books_data = [
    ("Data Structures and Algorithms", "Mark Allen", "Computer Science", "A1", "9780131103627"),
    ("Clean Code", "Robert C. Martin", "Programming", "A2", "9780132350884"),
    ("Artificial Intelligence", "Stuart Russell", "AI", "B1", "9780136042594"),
    ("Python Crash Course", "Eric Matthes", "Programming", "A3", "9781593279288"),
    ("Deep Learning", "Ian Goodfellow", "AI", "B2", "9780262035613"),
    ("Computer Networks", "Andrew Tanenbaum", "Networking", "C1", "9780132126953"),
    ("Operating System Concepts", "Silberschatz", "OS", "C2", "9781118063330"),
    ("Introduction to Algorithms", "Thomas H. Cormen", "Algorithms", "A4", "9780262033848"),
    ("Database System Concepts", "Abraham Silberschatz", "Database", "D1", "9780073523323"),
    ("Machine Learning", "Tom Mitchell", "ML", "B3", "9780070428072")
]
session = Session()
for title, author, genre, shelf, isbn in books_data:
    image_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
    image_path = f"covers/{isbn}.jpg"
    try:
        response = requests.get(image_url)
        
        if response.status_code == 200:
            with open(image_path, "wb") as f:
                f.write(response.content)
            book = Book(
                title=title,
                author=author,
                genre=genre,
                shelf=shelf,
                image_path=image_path
            )
            session.add(book)
            print(f"Added: {title}")
        else:
            print(f"Cover not found for {title}")
    except Exception as e:
        print(f"Error downloading {title}: {e}")
session.commit()
print("All books added successfully!")
