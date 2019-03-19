from app import app
from app.scripts import scraping, to_myline
from flask import render_template, request, url_for, redirect
from app import db
from app.models.product_info import Product_item
from random import sample
import time
from datetime import datetime

@app.route("/")
def index():
    try:
        product_items = Product_item.query.order_by(Product_item.id.desc()).all()
        show_products = sample(product_items, 6)
        #img, img_link, title, price, point
        ids = [show_product.id for show_product in show_products]
        imgs = [show_product.img for show_product in show_products]
        img_links = [show_product.img_link for show_product in show_products]
        titles = [show_product.title for show_product in show_products]
        prices = [show_product.price for show_product in show_products]
        points = [show_product.point for show_product in show_products]
        results = zip(ids, imgs, img_links, titles, prices, points)
    except:
        results = []
    return render_template("index.html", results=results)

@app.route("/register", methods=["GET"])
def register():
    product_items = Product_item.query.order_by(Product_item.id.desc()).all()
    search_words = set([product_item.search_word for product_item in product_items])
    return render_template("register.html", search_words=search_words)

@app.route("/registered", methods=["GET", "POST"])
def register_product():
    if request.method == "POST":
        search_word = request.form["search_word"]
        product_items = Product_item.query.order_by(Product_item.id.desc()).all()
        search_words = set([product_item.search_word for product_item in product_items])
        if search_word in search_words:
            return render_template("register.html", search_words=search_words, error="既に登録されている商品名です")
        product_list = scraping.get_page(search_word)
        imgs, img_links, titles, prices, points, top_reviews, recent_reviews = scraping.get_info(product_list)
        products = zip(imgs, img_links, titles, prices, points, top_reviews, recent_reviews)
        for img, img_link, title, price, point, top_review, recent_review in products:
            product = Product_item(search_word=search_word, img=img, img_link=img_link, title=title, price=price, point=point, top_review=top_review, recent_review=recent_review)
            db.session.add(product)
            db.session.commit()
        return redirect(url_for('register'))
    return redirect(url_for('register'))

@app.route("/delete/<search_word>", methods=["GET", "POST"])
def delete_product(search_word):
    if request.method == "POST":
        delete_items = Product_item.query.filter(Product_item.search_word == search_word).all()
        for delete_item in delete_items:
            db.session.delete(delete_item)
            db.session.commit()
        return redirect(url_for('register'))
    return redirect(url_for('register'))

@app.route("/submit/<int:id>", methods=["GET", "POST"])
def submit_line(id):
    if request.method == "POST":
        product = Product_item.query.filter(Product_item.id == id).first()
        search_word = product.search_word
        img = product.img
        img_link = product.img_link
        title = product.title
        price = product.price
        point = product.point
        top_review = product.top_review
        recent_review = product.recent_review
        to_myline.page_submit(search_word, img, img_link, title, price, point, top_review, recent_review)
        return redirect(url_for('index'))
    return redirect(url_for('index'))
