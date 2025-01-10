#from calendar import c
#from cgi import print_directory
#from cmath import e, log
from encodings import utf_8
from this import d
import neologdn
import os
import os.path
import MeCab
import glob


#文章をまとめたフォルダからファイル名を取得
path = r'D:\zemi\project_novel\test'
extension = '*.txt'
path_search = os.path.join(path, extension)
file_path = glob.glob(path_search)
file = [os.path.basename(f) for f in file_path]

#Mecab用インスタンス
tagger = MeCab.Tagger("-Owakati")
tagger.parse('')

#分かち書き後に不要な単語を除去（品詞で指定）
def wakati_text(text):

# 分けてノードごとにする
    node = tagger.parseToNode(text)
    terms = []
    print(terms)
    #必要な名詞の種類
    a={"一般","形容動詞語幹"}

    #必要な動詞の種類
    b={"自立"}

    while node:

        # 単語
        term = node.surface

        # 品詞
        pos = node.feature.split(',')

        # 品詞が条件と一致している単語を保存
        if len(term)<7:

            if pos[0]=="動詞" and pos[1] in b:
                terms.append(term)
                with open("doshi.log", 'a', encoding="utf_8") as f:
                    f.write(term+" ")
            elif pos[0]=="形容詞":
                terms.append(term)
                with open("keyoshi.log", 'a', encoding="utf_8") as f:
                    f.write(term+" ")
            elif pos[0]=="名詞" and pos[1] in a:
                terms.append(term)
                print(pos[1])
                with open("meshi.log", 'a', encoding="utf_8") as f:
                    f.write(term+" ")

        node = node.next

    # 連結
    text_result = ' '.join(terms)
    return text_result

#テキストファイルを1つずつ開いて処理
for index in range(len(file)):
        FILE_NAME = file[index]
        index=index + 1
        with open(FILE_NAME, "r", encoding="utf_8") as f:
            eetext = f.read()
        text=neologdn.normalize(eetext)
        print(tagger.parse(text))
        with open("doshi.log", 'a', encoding="utf_8") as f:
            f.write("\n\n"+FILE_NAME+"\n")
        with open("keyoshi.log", 'a', encoding="utf_8") as f:
            f.write("\n\n"+FILE_NAME+"\n")
        with open("meshi.log", 'a', encoding="utf_8") as f:
            f.write("\n\n"+FILE_NAME+"\n")

        with open("as.log", 'a', encoding="utf_8") as f:
            f.write(wakati_text(text)+" ")