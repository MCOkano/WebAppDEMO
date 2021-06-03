from typing import Text
from flask import Flask,render_template,request

#DBアクセス用ライブラリ
import pyodbc

#DB接続
def connectSQL():
    server = 'mcdev001.database.windows.net'
    database = 'DMRE_Demo_1st'
    username = 'mcroot'
    password = 'mlG0klf$3_6r'   
    driver= '{ODBC Driver 17 for SQL Server}'
    conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()
    print("SQL Connect OK")
    return conn,cursor

#DB切断
def closeSQL(_cursor,_conn):
    _cursor.close()
    _conn.close()
    print("SQL Close OK")
    return

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main_page_GET():
    text = "ここに結果が出力されます"
    return render_template("page_top.html",text=text)

@app.route("/", methods=["POST"])
def main_page_POST():

    cn,cur = connectSQL()

    cur.execute("select * from Table_D_テストテーブル")
    rows = cur.fetchall()
#    rows = [['1','2021-05-01','入庫','AAAA'],['2','2021-05-02','入庫','BBBB'],['3','2021-05-01','出庫','CCCC'],['4','2021-05-03','入庫','DDDD'],['5','2021-05-01','出庫','EEEE'],['6','2021-05-02','入庫','FFFF'],['7','2021-05-04','出庫','GGGG']]
    closeSQL(cur,cn)

    rows2 = []

    searchdate = request.form["searchdate"]
    search_kind = request.form["search_kind"]
    print("検索日付：" + searchdate)
    print("検索種別：" + search_kind)
    if searchdate != "":
        text = "入力された検索日は" + searchdate + "です。"
        for r in rows:
            if searchdate == r[1]:
                if search_kind != 'なし':
                    if search_kind == r[2]:
                        add_data = r[0] , r[1] , r[2] , r[3]
                        rows2.append(add_data)
                else:
                    add_data = r[0] , r[1] , r[2] , r[3]
                    rows2.append(add_data)
                print(rows2)
 
        print("rows2 count:" + str(len(rows2)))
        if len(rows2) == 0:
            text = "該当するデータがありませんでした。"
            return render_template("page_top.html",text=text)
        else:
            return render_template("page.html",text=text,arr=rows2)

    else:

        text = "検索日の指定はありません。"
        for r in rows:
            if search_kind != 'なし':
                if search_kind == r[2]:
                    add_data = r[0] , r[1] , r[2] , r[3]
                    rows2.append(add_data)
            else:
                add_data = r[0] , r[1] , r[2] , r[3]
                rows2.append(add_data)
                print(rows2)
 
        print("rows2 count:" + str(len(rows2)))
        if len(rows2) == 0:
            text = "該当するデータがありませんでした。"
            return render_template("page_top.html",text=text)
        else:
            return render_template("page.html",text=text,arr=rows2)








## 実行
if __name__ == "__main__":
    app.run(debug=True)