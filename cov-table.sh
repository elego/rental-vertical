#!/bin/bash

addcol () 
{ 
    if [ -n "${AWKFS}" ]; then
        MAWK="/usr/bin/awk -F '${AWKFS}'";
    else
        MAWK=/usr/bin/awk;
    fi;
    ${MAWK} '
  BEGIN {
    sum[0] = 0
    maxcol = 0
    n = 0
  }

  {
    for (i = 1; i <= NF; i++) {
      if (NF > maxcol) {
        maxcol = NF
      }
      sum[i] += $i
    }
    n = n + 1
  }

  END {
    printf("%d lines\n", n)
    printf("sums: ")
    for (i = 1; i <= maxcol; i++) {
      printf("%d ", sum[i])
    }
    printf("\naverages: ")
    for (i = 1; i <= maxcol; i++) {
      printf("%.2d  ", sum[i]/n)
    }
    printf("\n")
  }
' "$@"
}

printf "| %-64s | %4s | %4s | %4s |\n" "*module*" "*lines*" "*misses*" "*percent*"

suma=
sumb=
for f in rental_* sale_* stock_*; do 
  if [[ -s $f/__manifest__.py ]]; then 
    s=$(grep "rental-vertical/${f}/" ${@:- ${HOME}/Downloads/coverage-report.txt} | addcol | grep 'sums:')
    a=$( echo $s | awk '{print $3}')
    b=$( echo $s | awk '{print $4}')
    if [[ -n "$a"  && -n "$b" ]]; then
      suma=$(( ${suma} + ${a} ))
      sumb=$(( ${sumb} + ${b} ))
      p=$(( ( $a - $b ) * 100 / $a ))
    else
      p=0
    fi
    printf "| %-64s |>. %4d |>. %4d |>. %4d |\n" "$f" "$a" "$b" "$p"
  fi
done
p=$(( ( ${suma} - ${sumb} ) * 100 / ${suma} ))

printf "| %-64s |>. %4d |>. %4d |>. %4d |\n" "*total*" "${suma}" "${sumb}" "$p"


