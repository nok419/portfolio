#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from itertools import combinations
import csv
import networkx as nx
from pyvis.network import Network
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser
from datetime import datetime
import json  # 追加
import add_click_macro_update  # 追加

class NetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Analysis Application")
        self.root.geometry("1000x800")
        self.file_path = ""
        self.data = None
        self.start_date = None
        self.end_date = None

        # GUI Elements
        self.file_label = tk.Label(root, text="CSVファイルを選択してください:")
        self.file_button = tk.Button(root, text="ファイルを選択", command=self.choose_file)
        
        # IDフィルタ
        self.date_label = tk.Label(root, text="idでフィルタ:")
        self.date_check = tk.IntVar()
        self.date_checkbox = tk.Checkbutton(root, text="適用", variable=self.date_check, command=self.update_filters)
        self.start_date_label = tk.Label(root, text="開始を選択してください:")
        self.start_date_var = tk.StringVar(root)
        self.start_date_menu = ttk.Combobox(root, textvariable=self.start_date_var, state='disabled')
        self.end_date_label = tk.Label(root, text="終了を選択してください:")
        self.end_date_var = tk.StringVar(root)
        self.end_date_menu = ttk.Combobox(root, textvariable=self.end_date_var, state='disabled')
        
        # サブカテゴリ1フィルタ
        self.era_label = tk.Label(root, text="サブカテゴリ1でフィルタ:")
        self.era_check = tk.IntVar()
        self.era_checkbox = tk.Checkbutton(root, text="適用", variable=self.era_check, command=self.update_filters)
        self.start_era_label = tk.Label(root, text="選択してください:")
        self.start_era_menu = tk.Listbox(root, selectmode='multiple', height=6, exportselection=0)

        # サブカテゴリ2フィルタ
        self.place_label = tk.Label(root, text="サブカテゴリ2でフィルタ:")
        self.place_check = tk.IntVar()
        self.place_checkbox = tk.Checkbutton(root, text="適用", variable=self.place_check, command=self.update_filters)
        self.place_menu = tk.Listbox(root, selectmode='multiple', height=6, exportselection=0)
        
        self.run_button = tk.Button(root, text="実行", command=self.run_analysis)
        self.output_label = tk.Label(root, text="")
        self.status_label = tk.Label(root, text="")
        self.details_label = tk.Label(root, text="")

        # Layout (左側: ファイル選択とIDの絞り込み)
        self.file_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.file_button.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.date_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.date_checkbox.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.start_date_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.start_date_menu.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.end_date_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.end_date_menu.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        # Layout (右側: サブカテゴリ1とサブカテゴリ2)
        self.era_label.grid(row=1, column=2, padx=10, pady=10, sticky='e')
        self.era_checkbox.grid(row=1, column=3, padx=10, pady=10, sticky='e')
        self.start_era_label.grid(row=2, column=2, padx=10, pady=10, sticky='e')
        self.start_era_menu.grid(row=2, column=3, padx=10, pady=10, sticky='e')
        self.place_label.grid(row=3, column=2, padx=10, pady=10, sticky='e')
        self.place_checkbox.grid(row=3, column=3, padx=10, pady=10, sticky='e')
        self.place_menu.grid(row=4, column=3, padx=10, pady=10, sticky='e')

        self.run_button.grid(row=5, column=0, columnspan=4, pady=20)
        self.output_label.grid(row=6, column=0, columnspan=4, pady=10)
        self.status_label.grid(row=7, column=0, columnspan=4, pady=10)
        self.details_label.grid(row=8, column=0, columnspan=4, pady=10)

    def update_filters(self):
        # チェックボックスの状態に基づいてリストボックスの有効/無効を切り替える
        self.start_date_menu['state'] = 'normal' if self.date_check.get() else 'disabled'
        self.end_date_menu['state'] = 'normal' if self.date_check.get() else 'disabled'
        self.start_era_menu['state'] = 'normal' if self.era_check.get() else 'disabled'
        self.place_menu['state'] = 'normal' if self.place_check.get() else 'disabled'

    def choose_file(self):
        # CSVファイルを選択し、列名を指定してデータを読み込む
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            self.file_label.config(text=f"選択されたファイル: {self.file_path}")
            with open(self.file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            max_columns = max(len(line.split(',')) for line in lines)
            column_names = ['id', 'サブカテゴリ1', 'サブカテゴリ2'] + [f'人名{i}' for i in range(1, max_columns - 2)]
            self.data = pd.read_csv(self.file_path, names=column_names, header=None)
            self.data['id'] = pd.to_numeric(self.data['id'], errors='coerce')

            # 日付、サブカテゴリ1、サブカテゴリ2のリストボックスを更新
            dates = sorted(self.data['id'].dropna().unique())
            self.start_date_menu['values'] = dates
            self.end_date_menu['values'] = dates
            self.start_date_var.set(dates[0])
            self.end_date_var.set(dates[-1])

            # サブカテゴリ1をIDに基づいて並べ替え、重複を除去
            unique_eras = self.data[['id', 'サブカテゴリ1']].dropna().drop_duplicates(subset=['サブカテゴリ1']).sort_values(by='id')['サブカテゴリ1'].tolist()
            self.start_era_menu.delete(0, tk.END)
            for era in unique_eras:
                self.start_era_menu.insert(tk.END, era)
            
            # サブカテゴリ2のリストボックスを更新
            places = sorted(self.data['サブカテゴリ2'].dropna().unique())
            self.place_menu.delete(0, tk.END)
            for place in places:
                self.place_menu.insert(tk.END, place)
            
            messagebox.showinfo("ファイル読み込み成功", "ファイルが正常に読み込まれました")
            self.update_filters()
        
    def run_analysis(self):
        try:
            self.status_label.config(text="ネットワークを構築しています...")
            self.root.update_idletasks()

            self.apply_filters()

            min_date = self.data['id'].min()
            max_date = self.data['id'].max()
            co_occurrence_dict = self.count_co_occurrences()
            self.save_co_occurrences(co_occurrence_dict)
            self.create_network(co_occurrence_dict, min_date, max_date)
            degree_summary = self.calculate_degree_summary(co_occurrence_dict)

            # PyVisで生成したHTMLファイルを開く前にカスタマイズ
            output_file = f"co_occurrence_network_{min_date}_to_{max_date}.html"
            add_click_macro_update.yobidasi(output_file)

            # ここで要約統計量を表示
            summary_text = (
                f"ネットワーク構築日: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"ノード数: {degree_summary['ノード数']}\n"
                f"エッジ数: {degree_summary['エッジ数']}\n"
                f"平均次数: {degree_summary['平均次数']:.2f}\n"
                f"中央値次数: {degree_summary['中央値次数']}\n"
                f"次数標準偏差: {degree_summary['次数標準偏差']:.2f}\n"
                f"最大次数: {degree_summary['最大次数']}\n"
                f"最小次数: {degree_summary['最小次数']}\n"
                f"データの範囲: {min_date} から {max_date}"
            )
            self.details_label.config(text=summary_text)

            self.status_label.config(text="ネットワーク構築が完了しました")
        except Exception as e:
            messagebox.showerror("エラー", f"エラー: {e}")
            self.status_label.config(text="エラーが発生しました")

    def apply_filters(self):
        if self.date_check.get():
            self.filter_data_date()
        if self.era_check.get():
            self.filter_data_era()
        if self.place_check.get():
            self.filter_data_place()

    def filter_data_date(self):
        # 日付範囲でデータをフィルタリング
        self.data = self.data[(self.data['id'] >= int(self.start_date_var.get())) & (self.data['id'] <= int(self.end_date_var.get()))]

    def filter_data_era(self):
        # サブカテゴリ1でデータをフィルタリング (or条件)
        selected_eras = [self.start_era_menu.get(i) for i in self.start_era_menu.curselection()]
        if selected_eras:
            self.data = self.data[self.data['サブカテゴリ1'].isin(selected_eras)]

    def filter_data_place(self):
        # サブカテゴリ2でデータをフィルタリング (or条件)
        selected_places = [self.place_menu.get(i) for i in self.place_menu.curselection()]
        if selected_places:
            self.data = self.data[self.data['サブカテゴリ2'].isin(selected_places)]

    def count_co_occurrences(self):
        # 共起関係をカウントする
        co_occurrence_dict = {}
        for index, row in self.data.iterrows():
            names = row[3:].dropna().tolist()
            for name_pair in combinations(names, 2):
                sorted_pair = tuple(sorted(name_pair))
                if sorted_pair in co_occurrence_dict:
                    co_occurrence_dict[sorted_pair] += 1
                else:
                    co_occurrence_dict[sorted_pair] = 1
        return co_occurrence_dict

    def save_co_occurrences(self, co_occurrence_dict):
        # 共起関係をCSVファイルに保存
        output_csv_path = 'co_occurrence_data.csv'
        with open(output_csv_path, 'w', encoding='utf-8-sig', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['人名1', '人名2', '共起回数'])
            for (name1, name2), count in co_occurrence_dict.items():
                writer.writerow([name1, name2, count])
        
        # ノード接続情報をJSONファイルに保存
        node_connections_dict = {}
        for names_pair in co_occurrence_dict.keys():
            node1, node2 = names_pair
            if node1 not in node_connections_dict:
                node_connections_dict[node1] = []
            if node2 not in node_connections_dict:
                node_connections_dict[node2] = []
            node_connections_dict[node1].append(node2)
            node_connections_dict[node2].append(node1)

        output_json_path = 'node_connections.json'
        with open(output_json_path, 'w', encoding='utf-8-sig') as jsonfile:
            json.dump(node_connections_dict, jsonfile, ensure_ascii=False, indent=4)

        print(f"ノードの接続情報が {output_json_path} に保存されました。")

    def create_network(self, co_occurrence_dict, min_date, max_date):
        # PyVisを使ってネットワークを作成
        net = Network()

        # エッジを追加しながらノードを追加
        for names_pair, weight in co_occurrence_dict.items():
            node1, node2 = names_pair
            
            # ノード名が有効か確認
            if not node1 or not node2:
                continue  # 無効なノード名をスキップ
            
            # ノードを先に追加
            if node1 not in net.node_ids:
                net.add_node(node1, title=f"Connected Nodes: {node2}")
            if node2 not in net.node_ids:
                net.add_node(node2, title=f"Connected Nodes: {node1}")

            # エッジを追加
            net.add_edge(node1, node2, value=weight)

            # 既存ノードのタイトルを更新
            net.get_node(node1)['title'] += f", {node2}"
            net.get_node(node2)['title'] += f", {node1}"

        # 物理シミュレーションを有効化
        net.show_buttons(filter_=['physics', 'nodes'])
        net.toggle_physics(False)
        
        # 結果をHTMLファイルに保存
        output_file = f"co_occurrence_network_{min_date}_to_{max_date}.html"
        net.save_graph(output_file)

    def calculate_degree_summary(self, co_occurrence_dict):
        # NetworkXを使って次数分布の要約統計量を計算
        G = nx.Graph()

        for names_pair, weight in co_occurrence_dict.items():
            if pd.isna(names_pair[0]) or pd.isna(names_pair[1]):
                continue  # 無効なエッジをスキップ

            G.add_edge(names_pair[0], names_pair[1], weight=weight)

        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()

        if num_nodes == 0 or num_edges == 0:
            return {
                'ノード数': 0,
                'エッジ数': 0,
                '平均次数': 0,
                '中央値次数': 0,
                '次数標準偏差': 0,
                '最大次数': 0,
                '最小次数': 0
            }

        degrees = [deg for node, deg in G.degree()]
        
        degree_summary = {
            'ノード数': num_nodes,
            'エッジ数': num_edges,
            '平均次数': np.mean(degrees) if len(degrees) > 0 else 0,
            '中央値次数': np.median(degrees) if len(degrees) > 0 else 0,
            '次数標準偏差': np.std(degrees) if len(degrees) > 0 else 0,
            '最大次数': np.max(degrees) if len(degrees) > 0 else 0,
            '最小次数': np.min(degrees) if len(degrees) > 0 else 0
        }

        return degree_summary
    

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkApp(root)
    root.mainloop()
