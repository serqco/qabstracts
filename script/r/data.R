# Read data and create helper data
# to be read with source()

# We define a lot of tables (dataframes), some for plotting, others auxiliary.
# Table names are of the form C_by_R where
# C describes what is in the columns and
# R describes what makes the identity of a row.
#
# Abbreviations:
# art=article, ven=venue, sent=sentence
# Suffixes:  N: count, S: sentences, C: characters, W:words

library(sqldf)  # needs install before

#----- read input data:
datafile = "results/prestudy2-results.tsv"
codings_by_sent = read.delim(datafile)

#----- declare SQL fragments:
no.duplicates = "C.codername='Lutz'"  # coder 'A' should always exist
primary.code = "C.words is not null"

#----- R constants:
codeorder = c('h-background', 'a-background', 'background',
              'h-objective', 'a-objective', 'objective',
              'h-design', 'a-design', 'design',
              'h-method', 'a-method', 'method',
              'h-result', 'a-result', 'result',
              'h-conclusion', 'a-conclusion', 'conclusion'
             )
topicorder = c('background', 'objective', 'method', 'design', 
               'result', 'conclusion',  'other')

#----- helper routines:

with.order = function(df) {
  if ("code" %in% names(df))
    df$code = ordered(df$code, levels=rev(codeorder))
  if ("topic" %in% names(df))
    df$topic = ordered(df$topic, levels=rev(topicorder))
  df
  
}

#----- derived tables:
'
tbl = with.order(sqldf(sprintf("
    select x, y, z 
    from codings C
    where %s and %s
    group by fctr
    ", fragment)))
'
cat("totalNWC_by_ven:\n")
totalNWC_by_ven = with.order(sqldf(sprintf("
    select venue, 
           sum(1) as codingsN, sum(words) as words, sum(chars) as chars,
           sum(icount) as icount, sum(ucount) as ucount
    from codings_by_sent C
    where %s and %s
    group by C.venue
    ", no.duplicates, primary.code)))

cat("totalNWC_by_art:\n")
totalNWC_by_art = with.order(sqldf(sprintf("
    select citekey, venue, volume, 
           sum(1) as codingsN, sum(words) as words, sum(chars) as chars,
           sum(icount) as icount, sum(ucount) as ucount,
           sum(code LIKE 'h-%%') as h_N,
           sum(code LIKE 'a-%%') as a_N,
           sum(code LIKE 'h-%%') > 0 as is_struc,
           sum(code LIKE '%%design') > 0 as has_design
    from codings_by_sent C
    where %s and %s
    group by citekey
    ", no.duplicates, primary.code)))

cat("totalNWC_by_code_ven_dsgn:\n")
totalNWC_by_code_ven_dsgn = with.order(sqldf(sprintf("
    select code, topic, C.venue, has_design,
           sum(1) as codingsN, sum(C.words) as words, sum(C.chars) as chars,
           sum(C.icount) as icount, sum(C.ucount) as ucount
    from codings_by_sent C, totalNWC_by_art A
    where C.citekey = A.citekey and %s and %s
    group by C.code, C.topic, C.venue, A.has_design
    ", no.duplicates, primary.code)))

cat("totalNWC_by_sent:\n")
totalNWC_by_sent = with.order(sqldf(sprintf("
    select citekey, venue, volume, sidx, 
           sum(1) as codingsN, sum(words) as words, sum(chars) as chars,
           sum(icount) as icount, sum(ucount) as ucount
    from codings_by_sent C
    where %s and %s
    group by citekey, sidx
    ", no.duplicates, primary.code)))

cat("pctNWC_by_code_ven_struc:\n")
pctNWC_by_code_ven_struc = with.order(sqldf(sprintf("
    select round(100 * sum(1) / T.codingsN, 1) as codingspct,
           round(100 * sum(C.words) / T.words, 1) as wordspct,
           round(100 * sum(C.chars) / T.chars, 1) as charspct,
           C.code, C.venue, is_struc, has_design
    from codings_by_sent C, totalNWC_by_art A, totalNWC_by_ven T
    where C.citekey == A.citekey and C.venue == T.venue and %s and %s
    group by C.code, C.venue, A.is_struc, A.has_design
    ", no.duplicates, primary.code)))  # TODO: include duplicates!
