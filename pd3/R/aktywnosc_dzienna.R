library('data.table')
library('stringi')

source(file.path("funkcje", "wczytanie_csv.R"))
path <- file.path("", "media", "tmakowski", "Dysk", "dane_csv")
dt_posts <- load_csvs(
    sciezka=path,
    rodzaj="Posts",
    kolumny=c("Id", "CreationDate")
)

dt_dni <- dt_posts[,.(
    Id,
    Forum,
    Date=stri_datetime_parse(CreationDate, format="y-M-dd'T'HH:mm:ss")
)][,.(
    Id,
    Forum,
    Weekday=stri_datetime_format(Date, format="ccc"),
    WeekdayNr=stri_datetime_format(Date, format="c")
)]

dt_agg_dni <- dt_dni[
    !is.na(Weekday),      # wyrzucenie NA
    .(Count=.N),          # zliczenie
    by=.(Forum, Weekday, WeekdayNr)
] 

# DT ze średnią i odchyleniem standardowym
dt_mean_sd_dni <- dt_agg_dni[,
    .(
        ForumMean=mean(Count),
        ForumSd=sd(Count)
    ),
    by=.(Forum)
]

dt_per_forum_dni <- dt_agg_dni[ # Podpięcie średniej i odchylenia
    dt_mean_sd_dni,
    on=c("Forum" = "Forum")
][,
    .(
        Forum,
        Weekday,
        WeekdayNr,
        Z=(Count-ForumMean)/ForumSd    # standaryzacja
    )
]

dt_agg_dni_total <- dt_dni[
    !is.na(Weekday),
    .(Count=.N),
    by=.(Weekday, WeekdayNr)
]

tot_mean <- mean(dt_agg_total$Count)
tot_sd <- sd(dt_agg_total$Count)

dt_total_dni <- dt_agg_dni_total[,
    TotalZ:=(Count-tot_mean)/tot_sd
]

fwrite(dt_total_dni, file.path("dane", "aktywnosc_dzienna_total.csv"))
fwrite(dt_per_forum_dni, file.path("dane", "aktywnosc_dzienna.csv"))
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


### Wyniki ###
library('ggplot2')
dni <- c("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
dt_dane_total_dni <- fread(file.path("dane", "aktywnosc_dzienna_total.csv"))
dt_dane_per_forum_dni <- fread(file.path("dane", "aktywnosc_dzienna.csv"))

(
    plt <- ggplot()
        +geom_line(data=dt_dane_per_forum_dni,
                   aes(x=factor(Weekday, dni), y=Z, color=Forum, group=Forum), show.legend=FALSE)
        +geom_line(data=dt_dane_total_dni,
                   aes(x=factor(Weekday, dni), y=TotalZ, group=1), size=1.25)
)
