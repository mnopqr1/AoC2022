# Advent of Code 2022

## Day 1

* Trying to do this in OCaml this year just to learn and see the difference
* Installing OCaml on a new (Linux) installation was fairly smooth, following the instructions here:
https://dev.realworldocaml.org/install.html
* Writing the actual code for the puzzle was easy
* Writing the code for parsing the input was a bit of a struggle and involved
  a bit of internet searching
* I don't really understand the dune tool. I succeeded in writing a Makefile
  but I didn't commit enough files to be able to do `dune build`. The workflow
isn't very clear to me yet.
* Error messages in OCaml often refer to later lines. The VSCode extension
  makes me nervous because it is yelling at me while I'm not even done writing
the function yet!
* Got into some github cleaning trouble and ended up refreshing the entire
  repo...

## Day 2
* I like sum types.
* There is some redundancy in what I did for question 2 because I'm re-calculating the result of the round even if that was given from the start.
* There's probably a fancier way to write `beat` and `let_win` (they're each other's inverse) but don't know how.
* I used Scanf "in the wild"!
* I'd like to learn how to export some common functions (read, sum_list, etc) to a little utility library so that I don't have to copy/paste them into main every time.
