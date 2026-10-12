#!/bin/bash
# cited papers (corpusId:citekey) then seeded-but-unextracted
CITED="84499623:kimball1997 60878010:eccel2012 195922148:forster2016 250155510:althoff2022 \
17774932:chabotcouture2014 219686759:he2020 234365737:wang2021 278327193:gallusser2025 \
128411698:kilibarda2014 284273775:serranonotivoli2019 281622763:mu2025 283024444:hierro2025 \
272607389:huang2024 31512633:wright2017 8407239:li2004 34314121:fu2004 1666227:yin2014 \
4673735:marengo2017 124196310:zhang2016 52308154:hwang2019"
OTHER="16432275 54465149 55302471 129526222 133791555 197823247 219486154 225390613 \
247301991 256437472 256572165 267609509 268122880 289361597 290466870 290659217"
for pair in $CITED; do
  id="${pair%%:*}"; key="${pair##*:}"
  asta papers get "CorpusId:$id" --fields title,year,externalIds,openAccessPdf 2>/dev/null \
   | jq -r --arg k "$key" '"CITED\t\($k)\t\(.year // "?")\t\(.openAccessPdf.status // "CLOSED")\t\((.externalIds.DOI // .externalIds.ArXiv // "-"))\t\(.title)"'
done
for id in $OTHER; do
  asta papers get "CorpusId:$id" --fields title,year,externalIds,openAccessPdf 2>/dev/null \
   | jq -r '"SEEDED\t-\t\(.year // "?")\t\(.openAccessPdf.status // "CLOSED")\t\((.externalIds.DOI // .externalIds.ArXiv // "-"))\t\(.title)"'
done
