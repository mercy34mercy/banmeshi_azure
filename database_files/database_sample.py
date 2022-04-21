import sqlite3
db_path = "banmeshi.db"			# データベースファイル名を指定
def updata():
    data={"categoryName":"ソーセージ・ウインナー","parentCategoryId":"66","categoryId":50,"categoryUrl":"https://recipe.rakuten.co.jp/category/10-66-50/"}
    con = sqlite3.connect(db_path)  # データベースに接続
    cur = con.cursor()				# カーソルを取得
    cur.execute('update BANMESHI set parentCategoryId=? ,categoryId=?, categoryUrl=? where categoryName=?',(data["parentCategoryId"],data["categoryUrl"],data["categoryName"],data["categoryId"]))


def get_db():
    data = []
    con = sqlite3.connect(db_path)  # データベースに接続
    cur = con.cursor()				# カーソルを取得
    cur.execute('SELECT * FROM BANMESHI')
    datas=cur.fetchall()
    for data in datas:
        print(data)

    return str(datas)

def get_db_one(category):
    con = sqlite3.connect(db_path)  # データベースに接続
    cur = con.cursor()				# カーソルを取得
    # cur.execute('SELECT * FROM BANMESHI where "%{}%"'.format(category))
    cur.execute('SELECT * FROM BANMESHI where categoryName like ?',category)
    for row in cur:
        print(row)
