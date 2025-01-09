import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt
import community as community_louvain
from matplotlib import cm
import matplotlib.font_manager as fm
# Matplotlibでのネットワークグラフの出力（必要に応じて追加可能）
import json
import add_click_macro_update


# 日本語フォントの設定
font_path = 'C:/Windows/Fonts/meiryo.ttc'  # 例: メイリオフォント
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

# CSVファイルの読み込み
file_path = 'pca_result.csv'
data = pd.read_csv(file_path, index_col=0)

# コサイン類似度の計算
cosine_sim_matrix = cosine_similarity(data)

# コサイン類似度をデータフレームに変換
cosine_sim_df = pd.DataFrame(cosine_sim_matrix, index=data.index, columns=data.index)

# 自分自身との類似度を除外し、上三角行列を取得（組み合わせ的に重複を消すための処理）
cosine_sim_df.values[np.tril_indices_from(cosine_sim_df)] = np.nan

# networkxグラフの生成
graph = nx.Graph()

# ノードの追加
for name in data.index:
    graph.add_node(name)

# エッジの追加
edges = []
threshold = 0.069
for name in data.index:
    similarities = cosine_sim_df[name].dropna()
    for other_name, similarity in similarities.items():
        if similarity > threshold:
            edges.append((name, other_name, similarity))

# コサイン類似度が高い順にソート
edges = sorted(edges, key=lambda x: x[2], reverse=True)

# エッジを追加（条件: コサイン類似度が0.25以上のペア）
for edge in edges:
    graph.add_edge(edge[0], edge[1], weight=edge[2])

# エッジを持つノードのみを保持
nodes_with_edges = set()
for edge in graph.edges:
    nodes_with_edges.add(edge[0])
    nodes_with_edges.add(edge[1])

graph = graph.subgraph(nodes_with_edges).copy()

# ノード数とエッジ数を表示
num_nodes = graph.number_of_nodes()
num_edges = graph.number_of_edges()
print(f'ノード数: {num_nodes}')
print(f'エッジ数: {num_edges}')
print(f'エッジ条件: {threshold}より大きい')

# Louvain法でクラスタリング
partition = community_louvain.best_partition(graph)

# クラスタごとのノード数をカウント（ノードが1つのクラスタを除外）
cluster_counts = pd.Series(partition).value_counts().sort_index()
cluster_counts = cluster_counts[cluster_counts > 1]

# ノードが1つのクラスタのノードをグラフから削除
nodes_to_remove = [node for node, comm in partition.items() if cluster_counts.get(comm, 0) <= 1]
graph.remove_nodes_from(nodes_to_remove)

# 更新後のノード数を表示
updated_num_nodes = graph.number_of_nodes()
print(f'更新後のノード数: {updated_num_nodes}')

print(f'クラスタ数（ノードが1つのクラスタを除外）: {len(cluster_counts)}')
print(f'各クラスタに属するノード数（ノードが1つのクラスタを除外）:\n{cluster_counts}')

# 次数中心性の計算
degree_centrality = nx.degree_centrality(graph)

# 次数中心性が高い上位20名を取得
top_20_degree_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:30]

# 結果を表示
print("\n次数中心性が高い上位20名:")
for name, centrality in top_20_degree_centrality:
    print(f'{name}: {centrality}')


# クラスタごとのエッジの重み（コサイン類似度）の平均値を計算
cluster_edge_weights = {}
for edge in graph.edges(data=True):
    community = partition[edge[0]]
    if community in cluster_edge_weights:
        cluster_edge_weights[community].append(edge[2]['weight'])
    else:
        cluster_edge_weights[community] = [edge[2]['weight']]

cluster_avg_weights = {community: np.mean(weights) for community, weights in cluster_edge_weights.items()}

# 全クラスタの要約統計量を計算
all_weights = [weight for weights in cluster_edge_weights.values() for weight in weights]
summary_stats = {
    '平均値': np.mean(all_weights),
    '標準偏差': np.std(all_weights),
    '最小値': np.min(all_weights),
    '25パーセンタイル': np.percentile(all_weights, 25),
    '中央値': np.median(all_weights),
    '75パーセンタイル': np.percentile(all_weights, 75),
    '最大値': np.max(all_weights)
}

# 要約統計量の表示
summary_df = pd.DataFrame(summary_stats, index=['要約統計量']).T
print(summary_df)

# 要約統計量のヒストグラムを作成
plt.figure(figsize=(12, 8))
plt.hist(all_weights, bins=30, alpha=0.7, color='blue')
plt.xlabel('コサイン類似度')
plt.ylabel('頻度')
plt.title('全クラスタのコサイン類似度のヒストグラム')
plt.grid(True)
plt.show()

# コサイン類似度の平均値が高い上位5クラスタを取得
top_5_clusters = sorted(cluster_avg_weights.items(), key=lambda x: x[1], reverse=True)[:20]

# 上位5クラスタの情報を表示
for community, avg_weight in top_5_clusters:
    nodes_in_cluster = [node for node, comm in partition.items() if comm == community]
    num_nodes_in_cluster = len(nodes_in_cluster)
    print(f'クラスタ {community}:')
    print(f'  ノード数: {num_nodes_in_cluster}')
    print(f'  エッジの重みの平均値: {avg_weight:.4f}')
    print(f'  ノード名: {nodes_in_cluster}')

# ノードの次数を計算し、上位20ノードを表示
degree_dict = dict(graph.degree())
sorted_degrees = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)
top_20_degrees = sorted_degrees[:20]

# 上位20ノードの情報を表示
print("上位20ノードの次数:")
for node, degree in top_20_degrees:
    print(f"ノード: {node}, 次数: {degree}")

# クラスタごとの色を定義
num_clusters = len(cluster_counts)
colors = plt.get_cmap('tab20', num_clusters).colors  # 多様な色を使用


# Pyvisネットワークの生成
net = Network()

# ノードの追加（クラスタごとの色付け）
for node in graph.nodes:
    community = partition[node]
    if community in cluster_counts.index:  # ノードが1つのクラスタを除外
        color = 'rgb({}, {}, {})'.format(int(colors[community % len(colors)][0] * 255), 
                                          int(colors[community % len(colors)][1] * 255), 
                                          int(colors[community % len(colors)][2] * 255))
        #size = 100 * cluster_avg_weights.get(community, 1)  # 平均エッジ重みでノードサイズを調整
        net.add_node(node, label=node,  color=color)

# エッジの追加（固定色: 非常に薄い灰色）
edge_color = 'rgba(128, 128, 128)'  # 非常に薄い灰色
for edge in graph.edges(data=True):
    net.add_edge(edge[0], edge[1], value=edge[2]['weight'], color=edge_color)

# 物理演算を追加
net.show_buttons(filter_=['physics', 'nodes', 'interaction'])

# HTMLファイルとして保存
output_file = 'seiyuu_network_louvain.html'
net.save_graph(output_file)

# 結果のファイルパスを表示
print(f'ネットワークグラフは {output_file} に保存されました。')

# 要約統計量をCSVファイルに保存
summary_df.to_csv('cluster_summary_stats.csv', encoding='utf-8-sig')
#クラスタごとのノード数に基づくヒストグラムの作成
plt.figure(figsize=(12, 8))
plt.hist(cluster_counts, bins=range(1, cluster_counts.max() + 2), alpha=0.7, color='green', edgecolor='black')
plt.xlabel('クラスタのノード数')
plt.ylabel('頻度')
plt.title('クラスタごとのノード数のヒストグラム')
plt.xticks(range(1, cluster_counts.max() + 1), rotation=90)  # x軸のラベルを90度回転
plt.grid(True)
plt.tight_layout()  # レイアウトを自動調整
plt.show()

"""# 特定のノードとその接続を含むサブグラフを作成
target_nodes = ["鈴木 愛奈"]
subgraph_nodes = set(target_nodes)

for node in target_nodes:
    subgraph_nodes.update(graph.neighbors(node))

# 2階層のノードを含むサブグラフを作成
subgraph = graph.subgraph(subgraph_nodes)

# サブグラフのノード数とエッジ数を出力
num_nodes = subgraph.number_of_nodes()
num_edges = subgraph.number_of_edges()
print(f'サブグラフのノード数: {num_nodes}')
print(f'サブグラフのエッジ数: {num_edges}')

# Pyvisネットワークの生成
net = Network()

# ノードの追加
for node in subgraph.nodes():
    if node in target_nodes:
        color = 'red'  # 特定の3人のノードを赤に設定
        size = 30  # 一番大きい
    else:
        neighbors = [(neighbor, subgraph[node][neighbor]['weight']) for neighbor in subgraph.neighbors(node)]
        top_5_neighbors = sorted(neighbors, key=lambda x: x[1], reverse=True)[:5]
        top_5_names = [neighbor for neighbor, _ in top_5_neighbors]
        
        if any(n in target_nodes for n in top_5_names):
            color = 'yellow'  # コサイン類似度上位5名を黄色に設定
            size = 25
        else:
            color = 'blue'
            size = 20  # 二番目に大きい
    
    net.add_node(node, label=node, color=color, size=size)

# エッジの追加（コサイン類似度に基づいて色の濃淡を設定）
for edge in subgraph.edges(data=True):
    similarity = edge[2]['weight']
    intensity = int(similarity * 255)
    edge_color = f'rgba({intensity}, {intensity}, {intensity}, 0.6)'  # コサイン類似度が高いほど濃く
    net.add_edge(edge[0], edge[1], value=similarity, color=edge_color)

# 物理演算を追加
net.show_buttons(filter_=['physics', 'nodes', 'interaction'])

# HTMLファイルとして保存
output_file = 'target_seiyuu_suzuki.html'
net.save_graph(output_file)

# 指定された3人のノードの次数を出力
for node in target_nodes:
    degree = subgraph.degree(node)
    print(f"ノード: {node}, 次数: {degree}")

    # 各ノードがつながっているノードのコサイン類似度上位5ノードの名前を出力
    neighbors = [(neighbor, subgraph[node][neighbor]['weight']) for neighbor in subgraph.neighbors(node)]
    top_5_neighbors = sorted(neighbors, key=lambda x: x[1], reverse=True)[:5]
    
    print(f"{node} のコサイン類似度上位5ノード:")
    for neighbor, similarity in top_5_neighbors:
        print(f"  ノード: {neighbor}, コサイン類似度: {similarity}")
"""

# 特定のノードごとにネットワークを生成
target_nodes = ["堀川 りょう"]

for target in target_nodes:
    subgraph_nodes = {target}
    subgraph_nodes.update(graph.neighbors(target))

    # 2階層のノードを含むサブグラフを作成
    subgraph = graph.subgraph(subgraph_nodes)

    # サブグラフのノード数とエッジ数を出力
    num_nodes = subgraph.number_of_nodes()
    num_edges = subgraph.number_of_edges()
    print(f'サブグラフのノード数 ({target}): {num_nodes}')
    print(f'サブグラフのエッジ数 ({target}): {num_edges}')

    # Pyvisネットワークの生成
    net = Network()

    # 特定のノードのコサイン類似度上位5名を取得
    neighbors = [(neighbor, subgraph[target][neighbor]['weight']) for neighbor in subgraph.neighbors(target)]
    top_5_neighbors = sorted(neighbors, key=lambda x: x[1], reverse=True)[:5]
    top_5_names = [neighbor for neighbor, _ in top_5_neighbors]

    # ノードの追加
    for node in subgraph.nodes():
        if node == target:
            color = 'red'  # 特定のノードを赤に設定
            size = 30  # 一番大きい
        elif node in top_5_names:
            color = 'yellow'  # コサイン類似度上位5名を黄色に設定
            size = 25
        else:
            color = 'blue'
            size = 20  # 二番目に大きい

        net.add_node(node, label=node, color=color, size=size)

    # エッジの追加（コサイン類似度に基づいて色の濃淡を設定）
    for edge in subgraph.edges(data=True):
        similarity = edge[2]['weight']
        intensity = int(similarity * 255)
        edge_color = f'rgba({intensity}, {intensity}, {intensity}, 0.6)'  # コサイン類似度が高いほど濃く
        net.add_edge(edge[0], edge[1], value=similarity, color=edge_color)

    # 物理演算を追加
    net.show_buttons(filter_=['physics', 'nodes', 'interaction'])

    # HTMLファイルとして保存
    output_file = f'{target}_network.html'
    net.save_graph(output_file)
    print(f'ネットワークグラフは {output_file} に保存されました。')

    # 指定されたノードの次数を出力
    degree = subgraph.degree(target)
    print(f"ノード: {target}, 次数: {degree}")

    # 各ノードがつながっているノードのコサイン類似度上位5ノードの名前を出力
    print(f"{target} のコサイン類似度上位5ノード:")
    for neighbor, similarity in top_5_neighbors:
        print(f"  ノード: {neighbor}, コサイン類似度: {similarity}")

    
    # サブグラフのノードリストを保存するための辞書を作成
    node_connections = {}

    # 各ノードに対してその隣接ノードをリストとして追加
    for node in subgraph.nodes():
        node_connections[node] = list(subgraph.neighbors(node))

    # JSONファイルに保存
    with open('node_connections.json', 'w', encoding='utf-8-sig') as f:
        json.dump(node_connections, f, ensure_ascii=False, indent=4)

    print("サブグラフのノード接続情報が 'node_connections.json' に保存されました。")
    
    add_click_macro_update.yobidasi(output_file)
