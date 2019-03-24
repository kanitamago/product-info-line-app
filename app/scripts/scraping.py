from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
from random import randint

PATH = r"C:/Users/Masato/Downloads/chromedriver_win32/chromedriver.exe"
URL = "https://www.amazon.co.jp/"
#search_word = "けいおん"

def main():
    product_list = get_page(search_word)
    imgs, img_links, titles, prices, points, top_reviews, recent_reviews = get_info(product_list)
    products = zip(imgs, img_links, titles, prices, points, top_reviews, recent_reviews)
    for img, img_link, title, price, point, top_review, recent_review in products:
        result = """
            イメージ画像: {}

            商品リンク: {}

            タイトル: {}

            値段: {}

            評価: {}

            トップレビュー: {}

            最新レビュー: {}
                  """.format(img, img_link, title, price, point, top_review, recent_review)
        print(result)

def get_page(search_word):

    #商品リスト
    product_list = []

    #ブラウザ非表示の設定
    #options = Options()
    #options.add_argument('--headless')

    #ドライバー生成
    print("---ドライバー作成---\n")
    #driver = webdriver.Chrome(executable_path=PATH, chrome_options=options)
    driver = webdriver.Chrome(executable_path=PATH)

    #アマゾンにアクセス
    print("---Amazonにアクセス---\n")
    driver.get(URL)

    #商品名を入力する
    print("---商品名入力---\n")
    searchText = driver.find_element_by_id("twotabsearchtextbox")
    searchText.send_keys(search_word)

    #検索ボタンをクリック
    print("---検索ボタンクリック---\n")
    searchButton = driver.find_element_by_css_selector(".nav-search-submit .nav-input")
    searchButton.click()

    #読み込み待ち
    print("---読み込み待ち（2秒）---\n")
    time.sleep(2)

    #下までスクロールさせておく
    print("---下までスクロール---\n")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:

        #検索結果の1画面に表示されている商品数を取得
        print("---検索結果の1画面に表示されている商品数を取得---")
        result_items = driver.find_element_by_class_name("s-result-list").get_attribute("innerHTML")
        result_items = count_items(result_items)
        print("取得結果: ", result_items)

        for switch_idx, item_id in enumerate(result_items):

            #スクレイピング用のページソース
            source = {}

            #ページ遷移のチェック
            print("\n---ページ遷移のチェック---")
            print("id = {} ".format(item_id))
            checked = transition_check(driver, driver.find_element_by_id(item_id))
            li = None
            if checked:
                print("---遷移成功---\n")
                li = driver.find_element_by_id(item_id)
            else:
                print("---遷移失敗---\n")
                continue

            #サムネ画像を取得
            print("---サムネ画像取得---\n")
            try:
                source["img"] = li.find_element_by_css_selector(".a-spacing-base .a-section").get_attribute("innerHTML")
            except:
                source["img"] = "画像なし"
            #商品リンクを取得
            print("---商品リンク取得---\n")
            try:
                source["img_link"] = li.find_element_by_css_selector(".a-spacing-base").get_attribute("innerHTML")
            except:
                source["img_link"] = "リンクなし"
            #タイトルを取得
            print("---タイトル取得---\n")
            try:
                source["title"] = li.find_element_by_css_selector(".a-link-normal .s-access-title").get_attribute("innerHTML")
            except:
                source["title"] = "タイトルなし"
            #値段を取得
            print("---値段取得---\n")
            try:
                source["price"] = li.find_element_by_css_selector(".a-link-normal .a-color-price").get_attribute("innerHTML")
            except:
                source["price"] = "不明"
            #評価を取得
            print("---評価取得---\n")
            try:
                source["point"] = li.find_element_by_css_selector(".a-declarative .a-icon-star .a-icon-alt").get_attribute("innerHTML")
            except:
                source["point"] = "評価なし"

            #個々の商品ページへのリンクを持ったオブジェクトを取得
            #product_info = li.find_element_by_css_selector(".a-link-normal .a-text-normal")
            #個別の商品ページへ飛ぶ
            #product_info.click()

            #読み込み待ち
            print("---読み込み待ち（5秒）---\n")
            time.sleep(5)

            #---以降、商品の詳細ページ---

            #スクレイピングするページに移動した上で、下までスクロール
            print("---スクレイピングする個別ページに移動---\n")
            driver.switch_to.window(driver.window_handles[switch_idx+1])

            print("---下までスクロール---\n")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            print("---トップレビューと最新レビュー取得---")
            try:
                top_review = driver.find_element_by_css_selector("#reviewsMedley .a-row #cm-cr-dp-review-list .celwidget .a-expander-content")
                source["top_review"] = top_review.get_attribute("innerHTML")
                #最新のレビューに切り替える
                review_elem = driver.find_element_by_css_selector("#reviewsMedley .a-row #cm-cr-dp-review-sort-type #cm-cr-sort-dropdown")
                review_select_elem = Select(review_elem)
                review_select_elem.select_by_value("recent")

                #読み込み待ち
                print("---読み込み待ち（5秒間）---")
                time.sleep(5)

                recent_review = driver.find_element_by_css_selector("#reviewsMedley .a-row #cm-cr-dp-review-list .celwidget .review-text")
                source["recent_review"] = recent_review.get_attribute("innerHTML")
                print("---レビュー取得成功---\n")
            except:
                print("---レビューなし---\n")
                source["top_review"] = "レビューなし"
                source["recent_review"] = "レビューなし"

            #商品データをリストに格納
            product_list.append(source)

            #最初のページに戻る
            print("---最初のページに戻る---\n")
            driver.switch_to.window(driver.window_handles[0])

        print("---ドライバー停止---\n")
        driver.close()
        driver.quit()
    except:
        pass

    return product_list

def get_info(product_list):

    imgs = []
    img_links = []
    titles = []
    prices = []
    points = []
    top_reviews = []
    recent_reviews = []
    print(product_list)
    print("---スクレイピング開始---\n")
    for source in product_list:
        print("ソース: \n", source)
        img_soup = BeautifulSoup(source["img"], "html.parser")
        img = img_soup.select(".s-access-image")[0].get("src")
        imgs.append(img)

        imgLink_soup = BeautifulSoup(source["img_link"], "html.parser")
        img_link = imgLink_soup.select(".a-link-normal")[0].get("href")
        img_links.append(img_link)

        title = source["title"].replace("&amp;", " ")
        titles.append(title)

        price = source["price"]
        prices.append(price)

        point = source["point"]
        points.append(point)

        topReview_soup = BeautifulSoup(source["top_review"], "html.parser")
        top_review_result = topReview_soup.select(".a-expander-content")
        top_review = ""
        if not top_review_result:
            top_review = source["top_review"]
        else:
            top_review = top_review_result[0].text
        top_review = top_review.replace("<br>", "").replace('<span class="">', "").replace("</span>", "")
        top_reviews.append(top_review)

        recentReview_soup = BeautifulSoup(source["recent_review"], "html.parser")
        recent_review_result = recentReview_soup.select(".a-expander-content")
        recent_review = ""
        if not recent_review_result:
            recent_review = source["recent_review"]
        else:
            recent_review = recent_review_result[0].text
        recent_review = recent_review.replace("<br>", "").replace('<span class="">', "").replace("</span>", "")
        recent_reviews.append(recent_review)

    print("---スクレイピング終了---\n")

    return (imgs, img_links, titles, prices, points, top_reviews, recent_reviews)

def transition_check(driver, li):
    #3回ブラウザバックできる = 個別商品ページではない
    # Falseを返す
    print("個別ページをクリック")
    li.find_element_by_css_selector(".a-link-normal .a-text-normal").click()
    print("ブラウザバック")
    driver.switch_to.window(driver.window_handles[0])
    driver.back()
    driver.back()
    check_source1 = driver.page_source
    driver.back()
    check_source2 = driver.page_source
    if check_source1 == check_source2:
        #driver.switch_to.window(driver.window_handles[0])
        driver.forward()
        driver.forward()
        return True
    else:
        driver.forward()
        driver.forward()
        return False

def count_items(result_items):
    import re
    pattern = "result_[0-9]{2}|result_[0-9]"
    result_items = re.findall(pattern, result_items)
    return result_items

if __name__ == "__main__":
    main()
