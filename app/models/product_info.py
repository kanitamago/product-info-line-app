from app import db

class Product_item(db.Model):
    __tablename__ = "product_item"
    id = db.Column(db.Integer, primary_key=True)
    #img, img_link, title, price, point, top_review, recent_review
    search_word = db.Column(db.Text)
    img = db.Column(db.Text)
    img_link = db.Column(db.Text)
    title = db.Column(db.Text)
    price = db.Column(db.Text)
    point = db.Column(db.Text)
    top_review = db.Column(db.Text)
    recent_review = db.Column(db.Text)

    def __init__(self, search_word, img, img_link, title, price, point, top_review, recent_review):
        self.search_word = search_word
        self.img = img
        self.img_link = img_link
        self.title = title
        self.price = price
        self.point = point
        self.top_review = top_review
        self.recent_review = recent_review

    def __repr__(self):
        return """
            <PRODUCT ITEM>
            id: {}
            search_word: {}
            img: {}
            img_link: {}
            title: {}
            price: {}
            point: {}
            top_review: {}
            recent_review: {}
        """.format(self.id, self.search_word, self.img, self.img_link, self.title, self.price, self.point, self.top_review, self.recent_review)
