import mysql.connector
#sqlに接続
cnx = mysql.connector.connect(
host='192.168.2.2',
port='3306',
user='root',
password='root',
database='test_database',
    )
cursor_=cnx.cursor()

#データを取得
def show():
  row = cursor_.fetchall()[0][0]
  return (row)  

#sqlから受け取った文字を見やすくする
def wash(stri):
  stri=stri.replace("'","")
  stri=stri.replace("(","")
  stri=stri.replace(",","")
  stri=stri.replace("[","")
  stri=stri.replace("]","")
  stri=stri.replace(")","##")
  return(stri)

name_list=["'トトロ'","'皆川茜'"]#サンプルデータ
name_id_list=[]
series_list=["'ジブリ'","'クズの本懐'"]#サンプルデータ
series_id_list=[]
attribute_list=[]

for i in range(len(series_list)):
    cursor_.execute(f"select id from series where series_name = {series_list[i]}")
    series_id=show()
    cursor_.execute(f"select id from items where title = {name_list[i]} and series_id = {series_id}")
    name_id=show()
    name_id_list.append(name_id)
for name_id in name_id_list:
    cursor_.execute(f"select question_id from item_answers where item_id = {name_id}")
    attributes=cursor_.fetchall()
    for attribute in attributes:
       attribute_id=wash(str(attribute))
       cursor_.execute(f"select question from questions where id = {attribute_id}")
       attribute_list.append(wash(str(cursor_.fetchall())))
    cursor_.execute(f"select title from items where id ={name_id}")
    print(f"{wash(str(cursor_.fetchall()))}:{wash(str(attribute_list))}")