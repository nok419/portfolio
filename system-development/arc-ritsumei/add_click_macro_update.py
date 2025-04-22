from pyvis.network import Network
import json
import sys  # 追加
import webbrowser

#　読み込んだファイルにポップアップを追加する関数
def add_popup(html_content, json_data):
    # ポップアップ用のCSSとJavaScriptのコードを追加
    popup_script = f"""
    <style>
        #popup {{
            display: none;
            position: fixed;
            right: 10px;
            top: 10px;
            width: 300px;
            height: auto;
            background-color: white;
            border: 1px solid black;
            padding: 10px;
            z-index: 1000;
        }}
    </style>

    <div id="popup">
        <p id="popup-content">Node info will be displayed here</p>
    </div>

    <script>
        // 埋め込みJSONデータ
        var nodeData = {json.dumps(json_data)};

        // ノードがクリックされたときの処理
        network.on("click", function(params) {{
            if (params.nodes.length > 0) {{
                var nodeId = params.nodes[0];
                var nodeLabel = nodes.get(nodeId).label;
                var popup = document.getElementById("popup");
                var content = document.getElementById("popup-content");

                // ノード名をURL化して表示
                var nodeUrl = "https://www.dh-jac.net/db/shumei/results.php?-format=results-1p.htm&enter=default&-max=50&f42=" + encodeURIComponent(nodeLabel) + "&f3=&f43=&f40a=&f33%5B%5D=&f33%5B%5D=&f6%5B%5D=&f6%5B%5D=&-sortField1=&-sortField2=&-sortField3=&-sortField4=&-max=50&-Find=閲覧";
                var nodeLink = '<a href="' + nodeUrl + '" target="_blank">' + nodeLabel + '</a><br><br>';

                // JSONデータからノード名に基づく情報を取得し、それをURL化
                var links = "";
                if (nodeData[nodeLabel]) {{
                    nodeData[nodeLabel].forEach(function(name) {{
                        // 各名前をURL化してリンクを作成
                        var url = "https://www.dh-jac.net/db/shumei/results.php?-format=results-1p.htm&enter=default&-max=50&f42=" + encodeURIComponent(name) + "&f3=&f43=&f40a=&f33%5B%5D=&f33%5B%5D=&f6%5B%5D=&f6%5B%5D=&-sortField1=&-sortField2=&-sortField3=&-sortField4=&-max=50&-Find=閲覧";
                        links += '<a href="' + url + '" target="_blank">' + name + '</a><br>';
                    }});
                }} else {{
                    links = "No related data available for " + nodeLabel;
                }}

                // ポップアップにノード名とリンクを表示
                content.innerHTML = "<strong>Clicked Name:</strong><br>" + nodeLink + "<strong>Related Names:</strong><br>" + links;
                popup.style.display = "block";
            }}
        }});

        // ポップアップを閉じる機能も追加する（オプション）
        document.addEventListener("click", function(event) {{
            var popup = document.getElementById("popup");
            if (!event.target.closest("#popup") && !event.target.closest(".vis-network")) {{
                popup.style.display = "none";
            }}
        }});
    </script>
    """

    # ポップアップ用のスクリプトをHTMLに追加
    html_content = html_content.replace("</body>", popup_script + "</body>")
    return html_content



'''# メイン関数
if __name__ == "__main__":

    # HTMLをカスタマイズするファイルを読み込む
    origin_file_name = "co_occurrence_network_177900000_to_177901023.html"
    with open(origin_file_name, "r") as file:
        html_content = file.read()

    #表示させるデータを持ったjsonファイルを読み込む
    json_file_name = "node_connections.json"
    with open(json_file_name, "r", encoding="utf-8-sig") as file:
        json_data = json.load(file)

    # ポップアップを追加
    html_content = add_popup(html_content,json_data)

    # 新しいHTMLファイルとして保存
    save_file_name = origin_file_name.replace(".html", "_with_popup.html")
    with open(save_file_name, "w") as file:
        file.write(html_content)

    print(f"Custom HTML with popup has been saved to '{save_file_name}'.")
    webbrowser.open(save_file_name)'''

def yobidasi(origin_file):

    # HTMLをカスタマイズするファイルを読み込む
    origin_file_name = origin_file
    with open(origin_file_name, "r") as file:
        html_content = file.read()

    #表示させるデータを持ったjsonファイルを読み込む
    json_file_name = "node_connections.json"
    with open(json_file_name, "r", encoding="utf-8-sig") as file:
        json_data = json.load(file)

    # ポップアップを追加
    html_content = add_popup(html_content,json_data)

    # 新しいHTMLファイルとして保存
    save_file_name = origin_file_name.replace(".html", "_with_popup.html")
    with open(save_file_name, "w") as file:
        file.write(html_content)

    print(f"Custom HTML with popup has been saved to '{save_file_name}'.")
    webbrowser.open(save_file_name)

