import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)

def insertion_argsort(np.ndarray[double] t):
    """
    sortowanie przez wstawianie - permutacja sortująca
    """
    cdef int n = len(t)
    cdef np.ndarray[np.int32_t] o = np.arange(n, dtype=np.int32) # [0,1,2,..,n-1]
    cdef int j
    cdef int ocur
    for i in range(1, n):
        # t[o[0]] <= t[o[1]] <= ... <= t[o[i-1]]
        ocur = o[i]
        j = i
        while j > 0:
            if t[o[j-1]] <= t[ocur]:
                break
            o[j] = o[j-1]
            j -= 1
        o[j] = ocur
    return o

def Mnn(np.ndarray[double, ndim=2] X, int M):
    """
    X - macierz rzeczywista
    M - wartosc naturalna
    """
    cdef int n = X.shape[0]
    
    cdef np.ndarray[double, ndim=2] Odl = np.zeros(shape=(n,n))
    # DLA KAŻDEGO wektorka (n) musimy znaleźć ich odległości od siebie.
    for i in range(n):
        for j in range(n):
            Odl[i,j] = np.sum((X[i,:]-X[j,:])**2)
    
    cdef np.ndarray[np.int32_t, ndim=2] MacierzSortujaca = np.empty(shape=(n,M),dtype = np.int32)
    for i in range(n):
        MacierzSortujaca[i]=insertion_argsort(Odl[i,:])[1:M+1]

    return MacierzSortujaca
            