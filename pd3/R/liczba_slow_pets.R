setwd("~/Documents/repozytorium/iad/padr/pd3/R")
source(file.path("funkcje", "wczytanie_csv.R"))
path <- file.path("", "media", "tmakowski", "Dysk", "dane_csv")
dt_posts <- load_csvs(
    sciezka=path,
    rodzaj="Posts",
    kolumny=c("Id", "CreationDate", "Body"),
    wybrane_fora=c("pets")
)

wypisz_slowa <- function(post) {
    require('qdap')
    require('data.table')
    require('stringi')
    
    data.table(
        table(
            stri_extract_all_words(
                bracketX(post, "angle"))))
}

# Ustawienia
k <- 500
wynik <- data.table(WORD=character(), FREQ=numeric())
dane <- dt_posts[, .(Body)]

for (i in 1:ceiling(dim(dane)[1] / k)) {
    cat(paste("Step ", i, ": ", sep=""))
    tic <- Sys.time()
    wynik <- rbindlist(
        list(
            wynik,
            wypisz_slowa(
                dane[(k*(i-1)+1):min(k*i, dim(dane)[1]),]
            )
        )
    )[,.(FREQ=sum(FREQ)),by=.(WORD)]
    print(Sys.time()-tic)
}
fwrite(wynik, file.path("dane_raw", "slowa_pets.csv"))
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


### Zabawa na wyciągniętych słowach 
slowa_raw <- fread(file.path("dane_raw", "slowa_pets.csv"))

# Spłaszczenie wszystkich słów do małych znaków
slowa_lowercase <- slowa_raw[,.(WORD=stri_trans_tolower(WORD), FREQ)][,.(FREQ=sum(FREQ)),by=.(WORD)]

zwierze <- c(#"pet", "pets", 
             "cat", "cats", "kitten", "kitty", "kitties", "kittens", "kitten's", "feline", "leopard",
             "dog", "dogs", "dog's", "doggie", "doggy", "pup", "pups", "puppy", "puppies", "canine", "wolf",
             "rabbit", "rabbits", "rabbit's", "bunny", "bunnies",
             "fish", "fishes", "goldfish", "tuna", "catfish", "crabs",
             "bird", "birds", "parrot", "parrots", "chicken", "turkey", 
             "snake", "snakes", "gecko", "geckos", "lizard", "lizards", "dragon", "reptile",  "reptiles",
             "flea", "fleas", "worm", "worms", "tick", "bug",  "bugs",  "mite", "ant", "ants", "maggots",
             "turtle", "turtles", "tortoise", "tortoises",
             "horse", "horses",
             "snail", "snails", 
             "crickets",
             "rat", "rats",
             "shrimp",    
             "ferret", "ferrets",
             "hamster", "hamsters")

slowa_zwierze <- slowa_lowercase[WORD %in% zwierze, ]
fwrite(slowa_zwierze, file.path("dane", "pets_slowa_chmura.csv"))
# ^^^

## Wyścig szczurów ##
koty <- c("cat", "cats", "kitten", "kitty", "kitties", "kittens", "kitten's", "feline", "leopard")
psy <- c("dog", "dogs", "dog's", "doggie", "doggy", "pup", "pups", "puppy", "puppies", "canine", "wolf")
króliki <- c("rabbit", "rabbits", "rabbit's", "bunny", "bunnies")
ptaki <- c("bird", "birds", "parrot", "parrots", "chicken", "turkey")
gady <- c("snake", "snakes", "gecko", "geckos", "lizard", "lizards", "dragon", "reptile",  "reptiles")
robaki <- c("flea", "fleas", "worm", "worms", "tick", "bug",  "bugs",  "mite", "ant", "ants", "maggots", "crickets")
żółwie <- c("turtle", "turtles", "tortoise", "tortoises")
fretki <- c("ferret", "ferrets")
konie <- c("horse", "horses")
ślimaki <- c("snail", "snails")
gryzonie <- c("rat", "rats", "hamster", "hamsters")
wodne <- c("fish", "fishes", "goldfish", "tuna", "catfish", "crabs", "shrimp")

#koty, psy, króliki, ptaki, gady, robaki, żółwie, fretki, konie, ślimaki, gryzonie, wodne
# "koty", "psy", "króliki", "ptaki", "gady", "robaki", "żółwie", "fretki", "konie", "ślimaki", "gryzonie", "wodne"

dt_posty_zwierzaki <- dt_posts[,.(
        Id,
        CreationDate,
        Rozbicie=stri_extract_all_words(Body)
)][,.(
    Id,
    CreationDate,
    koty=lapply(Rozbicie, function(x) sum(koty %in% x)),
    psy=lapply(Rozbicie, function(x) sum(psy %in% x)),
    króliki=lapply(Rozbicie, function(x) sum(króliki %in% x)),
    ptaki=lapply(Rozbicie, function(x) sum(ptaki %in% x)),
    gady=lapply(Rozbicie, function(x) sum(gady %in% x)),
    robaki=lapply(Rozbicie, function(x) sum(robaki %in% x)),
    żółwie=lapply(Rozbicie, function(x) sum(żółwie %in% x)),
    fretki=lapply(Rozbicie, function(x) sum(fretki %in% x)),
    konie=lapply(Rozbicie, function(x) sum(konie %in% x)),
    ślimaki=lapply(Rozbicie, function(x) sum(ślimaki %in% x)),
    gryzonie=lapply(Rozbicie, function(x) sum(gryzonie %in% x)),
    wodne=lapply(Rozbicie, function(x) sum(wodne %in% x))
)]


dt_posty_zwierzaki_cumsum <- dt_posty_zwierzaki[,.(
    Id,
    CreationDate,
    koty=cumsum(koty),
    psy=cumsum(psy),
    króliki=cumsum(króliki),
    ptaki=cumsum(ptaki),
    gady=cumsum(gady),
    robaki=cumsum(robaki),
    żółwie=cumsum(żółwie),
    fretki=cumsum(fretki),
    konie=cumsum(konie),
    ślimaki=cumsum(ślimaki),
    gryzonie=cumsum(gryzonie),
    wodne=cumsum(wodne)
)]

fwrite(dt_posty_zwierzaki_cumsum, file.path("dane","pets_slowa_kategorie.csv"))


### Ostateczne wykresy ###
library('ggplot2')
library('ggwordcloud')
# --- Chmura --- #
slowa_zwierze <- fread(file.path("dane", "pets_slowa_chmura.csv"))
(
    ggplot(slowa_zwierze, aes(label=WORD, size=FREQ))
        + geom_text_wordcloud_area(eccentricity = 1)
        + scale_size_area(max_size = 50)
        + theme_minimal()
)

# --- Liczba wspomnień --- #
dt_posty_zwierzaki_cumsum <- fread(file.path("dane","pets_slowa_kategorie.csv"))[,
    Date:=stri_datetime_parse(CreationDate, format="y-M-dd'T'HH:mm:ss")
]
(
    ggplot(dt_posty_zwierzaki_cumsum, aes(x=Date))
    +geom_line(aes(y=psy, color="Psy"))
    +geom_line(aes(y=koty, color="Koty"))
    +geom_line(aes(y=króliki, color="Króliki"))
    +geom_line(aes(y=ptaki, color="Ptaki"))
    +geom_line(aes(y=gady, color="Gady"))
    +geom_line(aes(y=robaki, color="Robaki"))
    +geom_line(aes(y=żółwie, color="Żółwie"))
    +geom_line(aes(y=fretki, color="Fretki"))
    +geom_line(aes(y=konie, color="Konie"))
    +geom_line(aes(y=ślimaki, color="Ślimak"))
    +geom_line(aes(y=gryzonie, color="Gryzonie"))
    +geom_line(aes(y=wodne, color="Wodne"))
    +labs(x="Data", y="Liczba wystąpień", color="Kategoria")
    +scale_x_datetime(expand=c(0, 0))
    +scale_y_continuous(expand = c(0, 0))
    +theme_classic()
    +theme(
        axis.title=element_text(size=13),
        axis.text=element_text(size=10),
        legend.title=element_text(size=12),
        legend.text=element_text(size=10))
)
# ggsave("prezentacja/obrazki/pets_cumsum1.png", dpi=600)

(
    ggplot(dt_posty_zwierzaki_cumsum, aes(x=Date))
    +geom_line(aes(y=króliki, color="Króliki"))
    +geom_line(aes(y=ptaki, color="Ptaki"))
    +geom_line(aes(y=gady, color="Gady"))
    +geom_line(aes(y=robaki, color="Robaki"))
    +geom_line(aes(y=żółwie, color="Żółwie"))
    +geom_line(aes(y=fretki, color="Fretki"))
    +geom_line(aes(y=konie, color="Konie"))
    +geom_line(aes(y=ślimaki, color="Ślimak"))
    +geom_line(aes(y=gryzonie, color="Gryzonie"))
    +geom_line(aes(y=wodne, color="Wodne"))
    +labs(x="Data", y="Liczba wystąpień", color="Kategoria")
    +scale_x_datetime(expand=c(0, 0))
    +scale_y_continuous(expand=c(0, 0))
    +theme_classic()
    +theme(
        axis.title=element_text(size=13),
        axis.text=element_text(size=10),
        legend.title=element_text(size=12),
        legend.text=element_text(size=10))
)
# ggsave("prezentacja/obrazki/pets_cumsum2.png", dpi=600)
