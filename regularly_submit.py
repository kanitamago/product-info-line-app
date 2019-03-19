import requests
import time
from datetime import datetime
from app.models.product_info import Product_item

TOKEN = "FHmKUhZRwFkRLmAqWldLW60voP7yrpGhQORnBzjL273"
API = "https://notify-api.line.me/api/notify"
HEADERS = {'Authorization': 'Bearer ' + TOKEN}

def regularly_submit():
    print("定期実行")
    from random import sample
    product_items = Product_item.query.order_by(Product_item.id.desc()).all()
    submit_product = sample(product_items, 1)

    search_word = submit_product[0].search_word
    img = submit_product[0].img
    img_link = submit_product[0].img_link
    title = submit_product[0].title
    price = submit_product[0].price
    point = submit_product[0].point
    top_review = submit_product[0].top_review
    recent_review = submit_product[0].recent_review

    sw_m = "\n■検索ワード\n" + search_word
    link_m = "\n■商品へのリンク\n" + img_link
    title_m = "\n■タイトル\n" + title
    price_m = "\n■値段\n" + price
    point_m = "\n■評価\n" + point
    top_m = "\n■トップレビュー\n" + top_review
    recent_m = "\n■最新レビュー\n" + recent_review

    for submit_count, message in enumerate([sw_m, img, link_m, title_m, price_m, point_m, top_m, recent_m]):
        if submit_count == 1:
            if "画像なし" == img:
                img_m = "\n■{}".format(img)
                payload = {"message": img}
                requests.post(API, data=payload, headers=HEADERS)
            else:
                img = requests.get(img).content
                files = {"imageFile": img}
                img_m = "\n■{}のイメージ画像".format(title)
                payload = {"message": img_m}
                requests.post(API, data=payload, headers=HEADERS, files=files)
        else:
            payload = {"message": message}
            requests.post(API, data=payload, headers=HEADERS)
        time.sleep(1)
if __name__ == "__main__":
    regularly_submit()
