load_csvs <- function (sciezka, rodzaj, kolumny=NULL, wykluczone_fora=NULL, wybrane_fora=NULL) {
    stopifnot(!is.null(kolumny))
    
    # Wymagane pakiety
    require('stringi')
    require('data.table')
    
    cat("Rozpoczynam wczytywanie...\n")
    
    if (is.null(wybrane_fora)) {
        nazwy_csv <- list.files(sciezka, pattern=paste(".*_", rodzaj, sep=""))                        # odczytanie nazw csv
        nazwy_csv <- nazwy_csv[!(nazwy_csv %in% paste(wykluczone_fora, "_", rodzaj, ".csv", sep=""))] # wykluczenie wybranych nazw
        
        nazwy_forow <- stri_replace_first_fixed(
            stri_extract_first_regex(nazwy_csv, "[^\\.]*(\\.meta)?"),  # oczytanie: "FORUM_RODZAJ" z nazw csv
            paste("_", rodzaj, sep=""), "")                            # usunięcie "_RODZAJ" z nazw
    } else {
        nazwy_forow <- wybrane_fora
        nazwy_csv <- paste(nazwy_forow, "_", rodzaj, ".csv", sep="")
    }
    
    dlugosc_tekstu <- 13 + max(sapply(nazwy_forow, nchar)) # "Przetwarzam: " + nazwa forum
    
    dt_final <- data.table() # stworzenie pustej ramki
    for (nr_pliku in 1:length(nazwy_csv)) {
        cat(format(
            paste("\rWczytuję:", nazwy_forow[nr_pliku]),           # informacja o tym, co obecnie wczytuje
            width=dlugosc_tekstu))
        dt_final <- rbindlist(                                      # dołączenie nowo wczytanej csvki do tych, które już są
            list(
                dt_final,
                fread(
                    input=file.path(sciezka, nazwy_csv[nr_pliku]),  # scieżka pliku
                    sep=",",                                        # separator
                    select=kolumny                                  # wybrane kolumy
                )[,Forum:=nazwy_forow[nr_pliku]]),                  # dopisanie nazwy forum
            fill=TRUE)
    }
    cat("\nGotowe\n") # żeby ładnie było
    
    return(dt_final)
}