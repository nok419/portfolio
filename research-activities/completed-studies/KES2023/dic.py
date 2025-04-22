import mysql.connector
import os

# 環境変数から情報を取得（非公開化しています）
cnx = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
)
cursor_ = cnx.cursor()

dics = ["question_groups", "questions", "question_categories"]

def clean_content(content):
    return content.replace(" ", "").replace("|", "").replace("+", "").replace("-", "").replace("'", "").replace("\n", "##")

for table in dics:
    with open(f"dic/{table}_dic.txt", "r", encoding="utf-8") as f:
        contents = clean_content(f.read()).split("##")

    with open(f"dic/{table}_dic2.txt", "r", encoding="utf-8") as f:
        con2s = clean_content(f.read()).split("##")

    for i in range(3, len(con2s) - 1):
        if table == "question_groups":
            culm = "group_name"
        elif table == "questions":
            culm = "question"
        elif table == "question_categories":
            culm = "category_name"
        cursor_.execute(f"UPDATE {table} SET {culm} = %s WHERE id = %s;", (contents[i], con2s[i]))
        cursor_.execute("COMMIT")
    cursor_.execute(f"SELECT * FROM {table};")
    print(cursor_.fetchall())

