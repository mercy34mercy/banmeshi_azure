import csv
import sqlite3
import json
from typing import Text

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
                recipeId text UNIQUE,
                recipeMaterial text,
                recipeTitle text,
                recipeUrl text,
                smallImageUrl text)''')
    
    con.commit()					# データベース更新の確定
    con.close()						# データベースを閉じる
    
    
def add_recipe(jsondata):
    con = sqlite3.connect(db_path_recipe)
    cur = con.cursor()
    # print(jsondata)
 
    
    text = ""
    i = 0
    for data in jsondata["data"]:
            text = ""
            for l in range(len(data["recipeMaterial"])):
                if i != 0:
                    text += ","
                text += data["recipeMaterial"][l]
                i+=1
            # print(text)
            # print(data["recipeMaterial"])
            try:
                cur.execute('insert into RECIPE(foodImageUrl,mediumImageUrl,recipeCost,recipeId,recipeMaterial,recipeTitle,recipeUrl,smallImageUrl) values (?,?,?,?,?,?,?,?);', (data["foodImageUrl"],data["mediumImageUrl"],data["recipeCost"],data["recipeId"],data["recipeTitle"],text,data["recipeUrl"],data["smallImageUrl"]))
                print("succsess")
            except:
                try:
                    cur.execute('update RECIPE set foodImageUrl=? ,mediumImageUrl=? ,recipeCost=? ,recipeMaterial=? ,recipeTitle=? ,recipeUrl=? ,smallImageUrl=?  where recipeId = ?',(data["foodImageUrl"],data["mediumImageUrl"],data["recipeCost"],text,data["recipeTitle"],data["recipeUrl"],data["smallImageUrl"],data["recipeId"]))
                    
                except Exception as e:
                    print('=== エラー内容 ===')
                    print('type:' + str(type(e)))
                    print('args:' + str(e.args))
                    print('message:' + e.message)
                    print('error:' + str(e))
                    
            
                        
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
    cur.execute('SELECT categoryId FROM BANMESHI')
    datas=cur.fetchall()
    
    jsonify = ({
        "data":[]
        })

    for data in datas:
        categorys = str(data) 
        category = categorys.split("/")
        for i in category:
            if i >= "0" and i <= "9":
                print(i)
                add_data={
                    "categoy":str(i)
                }
        
        
      
        jsonify["data"].append(add_data)
        
    # try:
    #      for row in cur.execute('SELECT * FROM BANMESHI'):
    #         print(row)
    #         data.append(row)
    # except sqlite3.Error as e:		# エラー処理
    #     print("Error occurred:", e.args[0])
    #     return e
    return jsonify


def get_db_recipe():
    data  = []
    con = sqlite3.connect(db_path_recipe)  # データベースに接続
    cur = con.cursor()				# カーソルを取得
    cur.execute('SELECT recipeMaterial  FROM RECIPE')
    datas=cur.fetchall()
    for data in datas:
        print(data)
    return data

# json形式でPOSTされたデータをsqlに直してjsonデータを返却する
def get_db_recipe_one(jsondata):
    
    data  = []
     
    # POSTされたjsonを分けて保存する
    q_data = ""
    
    l = 0
    for i in jsondata:
        print(i)
        if l!=0:
             q_data+=("AND")
        
        q_data+= ' recipeMaterial like \"%' +  i + "%\" "
        l+=1
       
    
    
    
        
    con = sqlite3.connect(db_path_recipe)  # データベースに接続
    cur = con.cursor()				# カーソルを取得
    cur.execute('SELECT * FROM RECIPE where %s ORDER BY random() LIMIT 1' %q_data)
    datas=cur.fetchall()
    jsonify = ({
          "data":[]
        })
    

    
    
    for data in datas:      
        materials = data[4].split(',')
        jsonnify2 =({ "recipeMaterial":[]
    })
        for material in materials:
            if len(str(material))>1:
                jsonnify2["recipeMaterial"].append(material)
        
        add_data = {
                "foodImageUrl": data[0],
                "mediumImageUrl":data[1],
                "recipeCost":data[2],
                "recipeId":data[3],
                "recipeMaterial":jsonnify2["recipeMaterial"],
                "threeRecipeMaterial":jsonnify2["recipeMaterial"][:3],
                "recipeTitle":data[5],
                "recipeUrl":data[6],
                "smallImageUrl":data[7]
              }
        jsonify["data"].append(add_data)
        
    print(jsonify)
    return jsonify


def get_db_one(category):
    con = sqlite3.connect(db_path)  # データベースに接続
    cur = con.cursor()				# カーソルを取得
    # cur.execute('SELECT * FROM BANMESHI where "%{}%"'.format(category))
    cur.execute('SELECT * FROM BANMESHI where categoryName = "クリスマスケーキ"')
    for row in cur:
        print(row)
# get_db()
# get_db_one("ケーキ")


def get():
    data = []
    con = sqlite3.connect(db_path)  # データベースに接続
    cur = con.cursor()				# カーソルを取得
    cur.execute('SELECT COUNT(*) FROM BANMESHI')
    data=cur.fetchall()
    print(data)
    
def get2():
    data = []
    con = sqlite3.connect(db_path_recipe)  # データベースに接続
    cur = con.cursor()				# カーソルを取得
    cur.execute('SELECT COUNT(*) FROM RECIPE')
    data=cur.fetchall()
    print(data)

def delete_db():
    con = sqlite3.connect(db_path_recipe)  # データベースに接続
    cur = con.cursor()				# カーソルを取得
    cur.execute('SELECT * FROM RECIPE')
    datas=cur.fetchall()

    for data in datas:       
        mate = data[4].split(',')
        if len(mate)<3:
            cur.execute('DELETE FROM RECIPE where recipeId = %s'%data[3])
        else:
            print("safe")

