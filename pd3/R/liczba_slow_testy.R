library('stringi')
source(file.path("funkcje", "wczytanie_csv.R"))


#path <- file.path("", "media", "tmakowski", "Dysk", "dane_csv")
path <- file.path("..", "dane_csv")
dt_raw <- load_csvs(
    sciezka=path,
    rodzaj="Posts",
    kolumny=c("Id", "OwnerUserId", "CreationDate", "Body")
    #,wybrane_fora=c("coffee", "ai")
    #,wykluczone_fora=c("stackoverflow")
)

#x <- unname(unlist(dt_raw[1:4, .(Body)]))
#x
#library('rvest')
#html_text(read_html(x))
#y <- stri_replace_all_regex(x, "</?p*>", "")  # wywalenie <p> </p>
#z <- stri_extract_all_words(y)

#data.table(table(z[[1]]))

ogarnij_posta <- function(post) {
    require('rvest')
    require('data.table')
    
    post_bez_html <- html_text(read_html(post)) 
    slowa <- stri_extract_all_words(post_bez_html)
    dt_liczba_slow <- data.table(table(slowa))
    return(dt_liczba_slow)
}

testowa <- dt_raw[1:2, .(Body)]
testowa

#library('rvest')
#lapply(testowa, strip_html)

library('rvest')
html_text(read_html(testowa$Body[1:2]))
lapply(list(testowa$Body), function(x) html_text(read_html(x)))
#typeof(testowa)
#lapply(testowa, ogarnij_posta)
#rbindlist(lapply(testowa, ogarnij_posta), fill=TRUE)#[,.(LiczbaSlow=sum(N), by=.(Slowo=x)]



#html_text(read_html(ee))
#lapply(testowa[,.(Body)], ogarnij_posta)

#test <- rbindlist(lapply(x, ogarnij_posta), fill=TRUE)
#test[,
#    .(LiczbaSlow=sum(N)),
#    by=.(Slowo=x)
#][order(LiczbaSlow, decreasing=TRUE),][1:10]