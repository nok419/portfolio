#開発用　テーブルが存在するか検索する
import mysql.connector
def show(table_name):
    query3 = "SHOW TABLES"
    cursor_.execute(query3)
    rows = cursor_.fetchall()
    ch=0
    for row in rows:
        row=str(row)
        if row == f"('{table_name}',)":
            ch=1
        print (row)
    cursor_.execute(f"select count(*) from {table_name};")
    print(cursor_.fetchall())
    return ch
        
cnx = mysql.connector.connect(
host='192.168.2.2',
port='3306',
user='root',
password='root',
database='test_database',
    )
cursor_=cnx.cursor()

print(show("253initem_answers_id"))