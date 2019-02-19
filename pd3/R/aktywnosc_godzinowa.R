library('data.table')
library('ggplot2')
library('stringi')

source(file.path("funkcje", "wczytanie_csv.R"))
path <- file.path("", "media", "tmakowski", "Dysk", "dane_csv")
dt_posts <- load_csvs(
    sciezka=path,
    rodzaj="Posts",
    kolumny=c("Id", "CreationDate", "OwnerUserId")
)


# Dodanie godzin i dni z uprzednio odczytanych dat
dt_godziny <- dt_posts[,.(
    Id,
    Forum,
    OwnerUserId=as.numeric(OwnerUserId),
    Date=stri_datetime_parse(CreationDate, format="y-M-dd'T'HH:mm:ss"))
][,.(
    Id,
    Forum,
    OwnerUserId,
    Hour=stri_datetime_format(Date, format="HH"),
    Weekday=stri_datetime_format(Date, format="ccc")
)][!is.na(Weekday),]

# Zliczenie liczby postów w godzinie
dt_agg_godziny <- dt_godziny[,
    .(Count=.N),
    by=.(Hour, Weekday)
]

# Wyliczenie średniej i odchylenia
dt_mean_sd_godziny <- dt_agg_godziny[,
    .(
         WeekdayMean=mean(Count),
         WeekdaySd=sd(Count)
    ),
    by=.(Weekday)
]

dt_per_forum_godziny <- dt_agg_godziny[ # Podpięcie średniej i odchylenia
    dt_mean_sd_godziny,
    on=c("Weekday" = "Weekday")
][,.(
        Weekday,
        Hour,
        Count,
        Z=(Count-WeekdayMean)/WeekdaySd)
]

fwrite(dt_per_forum_godziny, file.path("dane", "aktywnosc_godzinowa.csv"))
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

dt_users <- load_csvs(
    sciezka=path,
    rodzaj="Users",
    kolumny=c("Id", "Location")
)


dt_loc <- dt_godziny[
    dt_users,
    on=c("OwnerUserId" = "Id", "Forum" = "Forum"),
    nomatch=0
][Location!=""]

dt_loc_usa <- dt_loc[,
    czyUSA:=!is.na(stri_match_first_regex(dt_loc$Location, "United States")) | !is.na(stri_match_first_regex(dt_loc$Location, "USA"))
][
    czyUSA==TRUE,
]

dt_loc_usa_agg <- dt_loc_usa[,
    .(Count=.N),
    by=.(Hour, Weekday)
]

dt_mean_sd_godziny_usa <- dt_loc_usa_agg[,
    .(
        WeekdayMean=mean(Count),
        WeekdaySd=sd(Count)
    ),
    by=.(Weekday)
]

dt_per_forum_godziny_usa <- dt_loc_usa_agg[ # Podpięcie średniej i odchylenia
    dt_mean_sd_godziny_usa,
    on=c("Weekday" = "Weekday")
][,.(
    Weekday,
    Hour=(as.numeric(Hour)+19)%%24, # przesunięcie do EST
    Count,
    Z=(Count-WeekdayMean)/WeekdaySd)
]

fwrite(dt_per_forum_godziny_usa, file.path("dane", "aktywnosc_godzinowa_usa.csv"))

( # standaryzowane
    plt <- ggplot(dt_per_forum_godziny_usa,
                  aes(x=Hour, y=Z, color=factor(Weekday, dni), group=Weekday))
        +geom_line()
)
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


### Wyniki ###
library('ggplot2')
dni <- c("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
dt_dane_per_forum_godziny <- fread(file.path("dane", "aktywnosc_godzinowa.csv"))

(
    plt <- ggplot(dt_dane_per_forum_godziny, aes(x=Hour, y=Z, color=factor(Weekday, dni), group=Weekday))
    +geom_line()
    +labs(x="Godzina", y="Standaryzowana liczba postow", color="Dzien tygodnia")
    +scale_x_continuous(expand=c(0, 0))
    +scale_y_continuous(expand=c(0, 0))
    +theme_classic()
    +theme(
        axis.title=element_text(size=16),
        axis.text=element_text(size=13),
        legend.title=element_text(size=15),
        legend.text=element_text(size=13),
        panel.border=element_rect(colour = "black", fill=NA, size=0.6))
)

dt_per_forum_godziny_usa <- fread(file.path("dane", "aktywnosc_godzinowa_usa.csv"))
( # standaryzowane
    plt <- ggplot(dt_per_forum_godziny_usa,
                  aes(x=Hour, y=Z, color=factor(Weekday, dni), group=Weekday))
    +geom_line()
)