import pandas as pd

def pd_to_markdown(df):
    """
    df -- ramka, którą chcemy wypisać
    """
    assert isinstance(df, pd.core.frame.DataFrame)
    
    nrows,ncols = df.shape
    col_lens = []
    
    # Zliczenie szerokości kolumn
    for col in range(ncols):
        col_lens.append(max(max([len(str(war)) for war in df.iloc[:nrows, col]]), len(df.columns[col])))
    
    # Nagłówki
    for col in range(ncols):
        print(f"| {df.columns[col]:{col_lens[col]}s} ", end="")
    print("|")
    
    # "Linia pozioma"
    for col in range(ncols):
        print("|", "-"*(col_lens[col]+2), sep="", end="")
    print("|")
              
    for row in range(nrows):
        for col in range(ncols):
            print(f"| {str(df.iloc[row, col]):{col_lens[col]}s} ", end="")
        print("|")