#!/bin/bash
pyfile="$1"
[[ -z "$1" ]] && echo "provide pyfile" && exit
[[ ! -f "$1" ]] && echo "$1 is not a pyfile" && exit

(pypy "$pyfile" in/a_example.txt && echo 'a done') &
(pypy "$pyfile" in/b_lovely_landscapes.txt && echo 'b done') &
(pypy "$pyfile" in/c_memorable_moments.txt && echo 'c done') &
(pypy "$pyfile" in/d_pet_pictures.txt && echo 'd done') &
(pypy "$pyfile" in/e_shiny_selfies.txt && echo 'e done')
