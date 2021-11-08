import csv
import sqlite3

db_path = "banmeshi.db"			# データベースファイル名を指定
db_path_recipe = "recipe.db"


def initialize_db():
    con = sqlite3.connect(db_path)  # データベースに接続
    cur = con.cursor()				# カーソルを取得
    # small {"categoryName":"しめさば","parentCategoryId":"72","categoryId":2026,"categoryUrl":"https://recipe.rakuten.co.jp/category/11-72-2026/"}
    # medium {"categoryName":"牛肉","parentCategoryId":"10","categoryId":275,"categoryUrl":"https://recipe.rakuten.co.jp/category/10-275/"}
    # large {"categoryName":"西洋料理","categoryId":"25","categoryUrl":"https://recipe.rakuten.co.jp/category/25/"}
    cur.execute('''CREATE TABLE BANMESHI
		(categoryName text primary key,
		parentCategoryId text,
		categoryId text,
		categoryUrl text,
        category text)''')
    # cur.execute('''CREATE TABLE BANMESHI
  #              (categoryName text, parentCategoryId text, categoryId text, categoryUrl real)''')

    con.commit()					# データベース更新の確定
    con.close()						# データベースを閉じる
    
    
# foodImageUrl
# mediumImageUrl
# nickname
# pickup
# rank
# recipeCost
# recipeDescription
# recipeId
# recipeIndication
# recipeMaterial
# recipePublishday
# recipeTitle
# recipeUrl
# shop
# smallImageUrl

def initialize_recipe_db():
    con = sqlite3.connect(db_path_recipe)
    cur = con.cursor()
    cur.execute('''CREATE TABLE RECIPE
                (foodImageUrl text,
                mediumImageUrl text,
                recipeCost text,
                recipeId text,
                recipeMaterial text,
                recipeTitle text,
                recipeUrl text,
                smallImageUrl text)''')
    
    con.commit()					# データベース更新の確定
    con.close()						# データベースを閉じる
    
    
def add_recipe(jsondata):
    con = sqlite3.connect(db_path_recipe)
    cur = con.cursor()
    
    for size in range(len( jsondata["result"])):
        data = jsondata["result"][size]
        try:
            cur.execute('insert into RECIPE(foodImageUrl,mediumImageUrl,recipeCost,recipeId,recipeMaterial,recipeTitle,recipeUrl,smallImageUrl) values (?,?,?,?,?,?,?,?);', (data["foodImageUrl"],data["mediumImageUrl"],data["recipeCost"],data["recipeId"],data["recipeMaterial"],data["recipeTitle"],data["recipeUrl"],data["smallImageUrl"]))
        except:
            try:
                cur.execute('update RECIPE set foodImageUrl=? ,mediumImageUrl=? ,recipeCost=? ,recipeMaterial=? ,recipeTitle=? ,recipeUrl=? ,smallImageUrl=?  where recipeId = ?',(data["foodImageUrl"],data["mediumImageUrl"],data["recipeCost"],data["recipeMaterial"],data["recipeTitle"],data["recipeUrl"],data["smallImageUrl"],data["recipeId"]))
            except Exception as e:
                            print('=== エラー内容 ===')
                            print('type:' + str(type(e)))
                            print('args:' + str(e.args))
                            print('message:' + e.message)
                            print('error:' + str(e))
                            return e  
                        
    con.commit()					# データベース更新の確定
    con.close()						# データベースを閉じる
    


def add_db(responses):
    con = sqlite3.connect(db_path)  # データベースに接続
    cur = con.cursor()				# カーソルを取得
    # SQL文の実行
    # try:
    for response in responses:
        for category in responses[response]:
            for data in responses[response][category]:
                if(category!='large'):
                    try:
                        cur.execute('insert into BANMESHI(categoryName,parentCategoryId,categoryId,categoryUrl,category) values (?,?,?,?,?);', (data["categoryName"],data["parentCategoryId"],data["categoryId"],data["categoryUrl"],category))
                    except:
                        try:
                            cur.execute('update BANMESHI set parentCategoryId=? ,categoryId=?, categoryUrl=?, category=? where categoryName=?',(data["parentCategoryId"],data["categoryUrl"],data["categoryId"],category,data["categoryName"]))
                        except Exception as e:
                            print('=== エラー内容 ===')
                            print('type:' + str(type(e)))
                            print('args:' + str(e.args))
                            print('message:' + e.message)
                            print('error:' + str(e))
                            return e       
                elif(category=='large'):
                    try:
                        cur.execute('insert into BANMESHI(categoryName,parentCategoryId,categoryId,categoryUrl,category) values (?,0,?,?,?);', (data["categoryName"],data["categoryId"],data["categoryUrl"],category))
                    except:
                        try:
                            cur.execute('update BANMESHI set parentCategoryId=0 ,categoryId=?, categoryUrl=?, category=? where categoryName=?',(data["categoryUrl"],data["categoryId"],category,data["categoryName"]))
                        except Exception as e:
                            print('=== エラー内容 ===')
                            print('type:' + str(type(e)))
                            print('args:' + str(e.args))
                            print('message:' + e.message)
                            print('error:' + str(e))
                            return e       
    # except sqlite3.Error as e:		# エラー処理
    #     print("Error occurred:", e.args[0])

    con.commit()					# データベース更新の確定
    con.close()						# データベースを閉じる


def get_db():
    data = []
    con = sqlite3.connect(db_path)  # データベースに接続
    cur = con.cursor()				# カーソルを取得
    cur.execute('SELECT categoryName FROM BANMESHI')
    datas=cur.fetchall()
    for data in datas:
        print(data)
    # try:
    #      for row in cur.execute('SELECT * FROM BANMESHI'):
    #         print(row)
    #         data.append(row)
    # except sqlite3.Error as e:		# エラー処理
    #     print("Error occurred:", e.args[0])
    #     return e
    return data


def get_db_recipe():
    data  = []
    con = sqlite3.connect(db_path_recipe)  # データベースに接続
    cur = con.cursor()				# カーソルを取得
    cur.execute('SELECT * FROM RECIPE')
    datas=cur.fetchall()
    for data in datas:
        print(data)
    return data

def get_db_one(category):
    con = sqlite3.connect(db_path)  # データベースに接続
    cur = con.cursor()				# カーソルを取得
    # cur.execute('SELECT * FROM BANMESHI where "%{}%"'.format(category))
    result=cur.execute('SELECT * FROM BANMESHI where categoryName = "クリスマスケーキ"')
    for row in cur:
        print(row)
# get_db()
# get_db_one("ケーキ")