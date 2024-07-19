import requests
from bs4 import BeautifulSoup
import time
import collections
import matplotlib.pyplot as plt
import networkx as nx
import japanize_matplotlib
from janome.tokenizer import Tokenizer



def get_Gsearch_results(keyword,num_pages=5):
    #url = f"https://www.google.com/search?q={keyword}"
    #print(url)
    search_results=[]
    headers={
        "User-Agent":
            #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
            #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15"
           # "Mozilla/5.0(Windows NT 10.0;WIn64;x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/45.0.3029.110 Safari/537.3"
        #"Mozilla/5.0(Windows NT 10.0;WIn64;x64) AppleWebKit/555.35(KHTML, like Gecko) Chrome/48.20.3029.1100 Safari/545.3"
        #"Mozilla/5.0(Windows NT 10.0;WIn64;x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/45.0.3029.110 Safari/537.3"
        #"Mozilla/5.0(Windows NT 10.0;WIn64;x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/45.0.3029.110 Safari/537.3"
        "Mozilla/5.0(Windows NT 10.0;WIn64;x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/45.0.3029.110 Safari/537.3"
    
        #,
    }
    for page in range(num_pages):
        start = page * 10
        
        url = f"https://www.google.com/search?q={keyword}&start={start}"
        
        response = requests.get(url, headers=headers)
        time.sleep(2)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("h3")
        search_results.extend([r.text for r in results])

    return search_results

t=Tokenizer()

def make_lis(firstword,G,color):
    #Moco=""
    assoc = get_Gsearch_results(firstword)
    saihin =[]
    saihin.append(firstword)
    for a_text in assoc:        
        for token in t.tokenize(a_text):
            pos = token.part_of_speech.split(',')
            if pos[0]=="名詞" and (pos[1]=='一般' or pos[1]=='固有名詞')and token.surface!='-' and 'サ変接続' not in pos:
                saihin.append(token.surface)
    c = collections.Counter(saihin)
    a = [i[0] for i in c.items() if i[1] >= 5]
    print(a)
    create_network_graph(firstword,a,G,color)
    return a
    
    
def create_network_graph(firstword,keywords,G,color):
    """for i, keyword in enumerate(keywords):
        G.add_node(keyword,color = color)
        if i > 0:
            G.add_edge(keywords[0], keyword)"""
    if not G.has_node(firstword):
        G.add_node(firstword, color=color)  # ノード追加時に色を設定
    for i,keyword in enumerate(keywords):
        if i>0: 
            if not G.has_node(keyword):
                G.add_node(keyword, color=color)  # ノード追加時に色を設定
            if not G.has_edge(firstword, keyword):
                G.add_edge(firstword, keyword)
    
import datetime

dt_now = datetime.datetime.now()

def main():
    G = nx.Graph()
    lis = make_lis("りんご",G,"yellow")
    for i, keyword in enumerate(lis):
        lis2 = make_lis(keyword,G,"lightblue")
        for j in lis2:
            make_lis(j,G,"lightgreen")
    japanize_matplotlib.japanize()
    pos = nx.spring_layout(G, k=0.3,iterations=10000)
    #pos = nx.planar_layout(G)
    node_colors = [G.nodes[node]['color'] for node in G.nodes] 

    plt.figure(figsize=(20,20))
    nx.draw(G, pos,with_labels=True, font_family='IPAexGothic',node_size=1000,node_color = node_colors)
    plt.savefig("test/photo/%s日%s-%s-%s.png" %(dt_now.day,dt_now.hour,dt_now.minute,dt_now.second), bbox_inches="tight")
    plt.show()
        
#print(lis)
    
#create_network_graph(['リンゴ', 'りんご', '通販', '青森', 'サイト', '林檎'])

if __name__=="__main__":
    main()