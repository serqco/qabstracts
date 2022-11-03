# Read data and create helper data
# to be read with source()

library(sqldf)  # needs install before

#----- read input data:
datafile = "results/prestudy2-results.tsv"
codings = read.delim(datafile)

#----- declare SQL fragments:
no.duplicates = "C.codername='Lutz'"  # coder 'A' should always exist
primary.code = "C.words is not null"
core.codes = "('background', 'objective', 'method', 'design', 'result', 'conclusion')"

#----- R constants:
codeorder = c('h-background', 'background',
              'h-objective', 'objective',
              'h-design', 'design',
              'h-method', 'method',
              'h-result', 'result',
              'h-conclusion', 'conclusion'
             )

#----- derived tables:
'
tbl = sqldf(sprintf("
    select x, y, z 
    from codings C
    where %s and %s
    group by fctr
    ", fragment))
'
cat("totals:\n")
totals = sqldf(sprintf("
    select venue, sum(words) as words, sum(chars) as chars 
    from codings C
    where %s and %s
    group by C.venue
    ", no.duplicates, primary.code))

cat("code totals:\n")
code_totals = sqldf(sprintf("
    select code, 
           sum(words) as words, sum(chars) as chars 
    from codings C
    where %s and %s
    group by code, venue
    ", no.duplicates, primary.code))

cat("abstracts:\n")
abstracts = sqldf(sprintf("
    select citekey, venue, volume, 
           sum(words) as words, sum(chars) as chars,
           sum(code LIKE '%s') as num_h
    from codings C
    where %s and %s
    group by citekey
    ", 'h-%', no.duplicates, primary.code))
abstracts = sqldf(sprintf("
    select *, 
           (num_h > 0) as is_struc
    from abstracts A
    "))

cat("sentences:\n")
sentences = sqldf(sprintf("
    select citekey, venue, volume, sidx, sum(words), sum(chars)
    from codings C
    where %s and %s
    group by citekey, sidx
    ", no.duplicates, primary.code))

cat("space.for.basics:\n")
space.for.basics = sqldf(sprintf("
    select round(100 * sum(C.words) / T.words, 1) as wordspct,
           round(100 * sum(C.chars) / T.chars, 1) as charspct,
           C.code, C.venue, A.is_struc
    from codings C, abstracts A, totals T
    where C.citekey == A.citekey and C.venue == T.venue and %s and %s
    group by C.code, C.venue, A.is_struc
    ", no.duplicates, primary.code))  # TODO: include duplicates!
space.for.basics$code = ordered(space.for.basics$code, levels=rev(codeorder))          
