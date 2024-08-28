from flask import Flask, request, jsonify    #　jsonifyによってPythonのデータをJSON形式に変換する
from flask_cors import CORS    #　異なるポート番号(オリジン)間でのリクエストの許可が可能になる→フロントエンドとバックエンドのURLの送受信に必要
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)    #　Flaskアプリケーションの作成

#　CORSを適用して、すべてのオリジンからのリクエストを許可
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.before_request
def before_request():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        headers = response.headers
        headers['Access-Control-Allow-Origin'] = '*'
        headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
        headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response


@app.route('/scrape', methods=['POST'])    #　/scrapeというURLに対してPOSTリクエストを処理するエンドポイントを定義

def scrape():    # フロントエンドからURLを受け取る
    data = request.json    #　HTTPリクエストのボディ部分からJSON形式でデータを取得
    url = data.get('url') 

    if not url:
        return jsonify({"error": "URL is required"}), 400    # URLが提供されなかった場合、400 のステータスコードとともにエラーメッセージを返す

    try:
        # 指定されたURLのページをリクエスト
        response = requests.get(url)
        response.raise_for_status()

        # 正しいエンコーディングを推測して設定
        response.encoding = response.apparent_encoding

        # BeautifulSoupでHTMLをパース
        soup = BeautifulSoup(response.text, 'html.parser')

        # すべての画像タグを取得
        img_tags = soup.find_all('img')
        img_urls = [img['src'] for img in img_tags if 'src' in img.attrs]

        # 絶対URLを作成する（もし相対URLが含まれている場合）
        img_urls = [requests.compat.urljoin(url, img_url) for img_url in img_urls]

        # フロントエンドに画像URLを返す
        return jsonify({"images": img_urls})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
