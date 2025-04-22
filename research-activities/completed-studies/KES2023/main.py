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

# データ数を取得
def show():
    row = cursor_.fetchall()[0][0]
    return row

# 数値の入力を受け取る
def get_qid(valname):
    while True:
        number = input(f'{valname}を入力>>>')
        if number.isdecimal():
            return int(number)
        elif number == "":
            return number
        else:
            print("エラー")

# 参照するテーブルが既にあるか確認
def recycle(table_name):
    cursor_.execute("SHOW TABLES")
    rows = cursor_.fetchall()
    return any(str(row) == f"('{table_name}',)" for row in rows)

# SQLから受け取った文字を見やすくする
def wash(stri):
    return stri.replace("'", "").replace("(", "").replace(")", "").replace(",", "")

# 属性idと前提条件を入れる事で事前条件を設定
def condition_set(q_id, assumption):
    a = f"(カラム名 = {q_id})"
    if not recycle(f"{q_id}inテーブル名"):
        cursor_.execute(f"DROP TABLE IF EXISTS {q_id}inテーブル名;")
        cursor_.execute(f"CREATE TABLE {q_id}inテーブル名 (カラム名2 INT);")
        cursor_.execute(f"INSERT INTO {q_id}inテーブル名 (カラム名2) SELECT カラム名 FROM テーブル名 WHERE {a};")
        cnx.commit()

    assumption += f" INNER JOIN {q_id}inテーブル名 ON テーブル名.カラム名 = {q_id}inテーブル名.カラム名2"
    cursor_.execute(f"SELECT COUNT(*) FROM テーブル名 {assumption} WHERE {a};")
    volume = show()
    if q_id == "253":
        print(f"「自然な人間」キャラ数: {volume}")
    else:
        print(f"条件に合うキャラ数: {volume}")

    return assumption

# 指定グループ内のタグで確率分布を作成
def conditional_prob(q_id, assumption, check):
    a = f"(カラム名 = {q_id} AND answer_state=1)"
    if not recycle(f"{q_id}inテーブル名"):
        cursor_.execute(f"DROP TABLE IF EXISTS {q_id}inテーブル名;")
        cursor_.execute(f"CREATE TABLE {q_id}inテーブル名 (カラム名2 INT);")
        cursor_.execute(f"INSERT INTO {q_id}inテーブル名 (カラム名2) SELECT カラム名 FROM テーブル名 WHERE {a};")
        cnx.commit()

    join_query = f"{assumption} INNER JOIN {q_id}inテーブル名 ON テーブル名.カラム名 = {q_id}inテーブル名.カラム名2"
    cursor_.execute(f"SELECT COUNT(*) FROM テーブル名 {assumption} WHERE カラム名 IN ({check});")
    volume = show()

    cursor_.execute(f"SELECT COUNT(*) FROM テーブル名 {join_query} WHERE {a};")
    prob = (10000 * show() // volume) / 100
    return prob

def first():
    q_id = "253"
    a_jpname = ""
    assumption = ""
    new_assump = condition_set(q_id, assumption)
    a_q_ids = [q_id]

    # 事前条件設定
    while True:
        q_id = get_qid("前提条件の属性ID")
        if q_id is None:
            break
        q_id = str(q_id)
        if q_id == "":
            print("事前条件を設定しました")
            for sushi in a_q_ids:
                cursor_.execute(f"SELECT カラム名 FROM カラム名s WHERE id = {sushi}")
                a_jpname += wash(str(cursor_.fetchall()))
            print(a_jpname)
            second(new_assump)
            break
        new_assump = condition_set(q_id, new_assump)
        a_q_ids.append(q_id)

def second(assumption):
    # 条件設定
    while True:
        g_id = get_qid("属性グループIDを入力")
        if g_id is None:
            break
        g_id = str(g_id)
        if g_id == "":
            print("終了します")
            break
        probs = []
        shin_probs = []
        cursor_.execute(f"SELECT id FROM カラム名s WHERE カラム名_group_id = '{g_id}'")
        q_ids = cursor_.fetchall()
        exs = [int(wash(str(q_id3))) for q_id3 in q_ids]
        check = ",".join(map(str, exs))
        for q_id in exs:
            prob = conditional_prob(q_id, assumption, check)
            cursor_.execute(f"SELECT カラム名 FROM カラム名s WHERE id = {q_id}")
            jpname = wash(str(cursor_.fetchall()))
            shin_probs.append(f"{jpname}: {prob}")
            probs.append(prob)
        probs.sort(reverse=True)
        for prob in probs:
            for shin_prob in shin_probs:
                if str(prob) in shin_prob:
                    print(f"{shin_prob}%")

first()
