xml_do_csv <- function(xml_path, csv_path, kolumny=NULL) {
    stopifnot(!is.null(kolumny))
    
    require('data.table')
    require('XML')
    
    xml_file <- file(xml_path, "r")
   
    readLines(xml_file, n=2) # przewinięcie śmieci
    
    repeat({
        linia <- readLines(xml_file, n=1)
        if (length(linia) == 0 || !isXMLString(linia)) break
        
        # Zapisanie linii
        fwrite(
            data.table(t(xmlAttrs(xmlParseString(linia))), kolumny, with=FALSE),
            file=csv_path,
            append=TRUE)
    })
    
    close(xml_file)
}