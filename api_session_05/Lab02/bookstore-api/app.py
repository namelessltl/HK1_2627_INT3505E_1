from flask import Flask
from models import db
from routes.book import books_bp
import os


app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'mock_bookstore.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
app.register_blueprint(books_bp)

with app.app_context():
    db.create_all()
    
    from models import Category, Author, Book
    if not db.session.execute(db.select(Book)).first():
        c1 = Category(name="Van hoc", slug="van-hoc")
        c2 = Category(name="Cong nghệ thong tin", slug="cong-nghe-thong-tin")
        db.session.add_all([c1, c2])
        db.session.commit()

        a1 = Author(name="Nguyen Nhat Anh", bio="Nha van chuyen viet cho thanh thieu nien.")
        a2 = Author(name="Robert C. Martin", bio="Ky su phan mem, tac gia sach Clean Code.")
        db.session.add_all([a1, a2])
        db.session.commit()

        b1 = Book(
            title="Mat Biec",
            isbn="978-604-2-14521-3",
            price_vnd=110000,
            stock=50,
            category_id=c1.id,
            authors=[a1]
        )
        b2 = Book(
            title="Clean Code - Ma Sach",
            isbn="978-0-13-235088-4",
            price_vnd=350000,
            stock=30,
            category_id=c2.id,
            authors=[a2]
        )
        db.session.add_all([b1, b2])
        db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
