import requests
from bs4 import BeautifulSoup
import time
import collections
import matplotlib.pyplot as plt
import networkx as nx
import japanize_matplotlib
from janome.tokenizer import Tokenizer
import datetime
from gensim.models import KeyedVectors
from gensim.models import word2vec

model_dir = r"C:\Users\admin\Desktop\project\20170201\entity_vector\entity_vector.model.bin"

model = KeyedVectors.load_word2vec_format(model_dir, binary=True)
index = model.index_to_key

dt_now = datetime.datetime.now()
t = Tokenizer()

def create_network_graph(word, keywords, G, color):
    if not G.has_node(word):
        G.add_node(word, color=color)
    for keyword in keywords:
        # Ensure keyword is a string, not a list
        if keyword[0]=="[" and keyword[-1]=="]":
            keyword = keyword[1:-1]
        if not G.has_node(keyword):
            G.add_node(keyword, color=color)
        if not G.has_edge(word, keyword) and word!=keyword:
            G.add_edge(word, keyword)

def make_word(keyword):
    a = []
    similar_list = model.most_similar(positive=[keyword], topn=5)
    for similar_set in similar_list:
        a.append(similar_set[0])
    return a

def main():
    G = nx.Graph()
    word = "りんご"
    lis = make_word(word)
    create_network_graph(word, lis, G, "red")
    print(word)
    print(lis)

    for i, keyword in enumerate(lis):
        lis2 = make_word(keyword)
        create_network_graph(keyword, lis2, G, "lightblue")
        print(keyword)
        print(lis2)
        for j, keyword2 in enumerate(lis2):
            lis3 = make_word(keyword2)
            print(keyword)
            print(lis3)
            create_network_graph(keyword2, lis3, G, "lightgreen")

    
    print(nx.number_of_nodes(G))
    

    node_colors = [G.nodes[node]['color'] for node in G.nodes]  # 全ノードの色を取得

    japanize_matplotlib.japanize()
    pos = nx.spring_layout(G,k=1.5,iterations=10000)
    #pos = nx.planar_layout(G)
    
    plt.figure(figsize=(15, 15))
    nx.draw(G, pos, alpha = 0.9,with_labels=True, font_family='IPAexGothic', node_size=1000, node_color=node_colors,arrows=True)
    plt.savefig("photo/word2vec-%s日%s-%s-%s.png" % (dt_now.day, dt_now.hour, dt_now.minute, dt_now.second), bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
    main()
