

dd=pctNWC_by_code_ven_struc
where=(as.character(dd$code) %in% (core.codes))

ggplot(dd[where,], aes(x=paste(venue), y=wordspct, fill=code)) + 
       geom_col() + theme_light()


dd=totalNWC_by_code_ven_dsgn
where=(dd$topic != 'none')

ggplot(dd[where,], aes(x=paste(has_design), y=icount+ucount, fill=code)) + 
  geom_col() + theme_light()
