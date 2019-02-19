
import numpy as np
import pyximport
pyximport.install(setup_args={'include_dirs':np.get_include()})
from spectral_aux import insertion_argsort, Mnn
from sklearn.cluster import KMeans

def bfs(graph, start):
    path = []
    queue = [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in path:
            path.append(vertex)
            queue.extend(graph[vertex])
    return path

def Mnn_graph(S):
    """
    S - macierz sąsiadów 
    """
    n = len(S)
    m = len(S[0])
    G = [[0]*n for i in range(n)] # macierz sąsiedzctwa
    for i in range(n):
        for j in range(1+i,n):
            for u in range(m):
                if int(S[i][u])==j or int(S[j][u])==i: 
                    G[j][i]=1
                    G[i][j]=1
                    break
    # sprawdź czy g jest spójny
    # wyszukiwanie bfs
    path = bfs(S,0)
    # wierzchołki, które są osiągalne z wierzchołka 0, powinny być wszystkie, czyli len(S)
    if n != len(path):
        for i in range(n):
            if i not in path:
                G[i][0]=1
                G[0][i]=1
                path.append(bfs(S,i))
            if n == len(path):
                return G
    
    return G

def Laplacian_eigen(G,k):
    
    """
    k>1 
    G - macierz sąsiadów
    """

    n = len(G)
    # wyznacz laplacjan czyli L=D-G gdzie dii to stopień itego wierzchołka
    L= [[0]*n for i in range(n)]
    for i in range(n):
        for j in range(n):
            if i==j:
                L[i][j]=np.sum(G[i])
            else:
                L[i][j]=-G[i][j]
    # L to laplasjan
    e_vals, e_vecs = np.linalg.eigh(L)
    return e_vecs.transpose()[1:(k+1)].transpose()

def spectral_clustering(X, k, M):
    
    Sasiedzi = Mnn(X,M)
    spojne = Mnn_graph(Sasiedzi)
    E = Laplacian_eigen(spojne, k)
    kmeans = KMeans(n_clusters=k, random_state=123).fit(E)

    return kmeans.labels_+1
    