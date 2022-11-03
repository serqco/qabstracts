

dd=space.for.basics
where=!is.na(dd$code)

ggplot(dd[where,], aes(x=paste(venue), y=wordspct, fill=code)) + 
       geom_col() + theme_light()
