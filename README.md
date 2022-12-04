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

## Day 3

* Learned how to use the `Seq` type. Its methods `find` and `exists` make it easy to check duplicates.
* For the second part, I wrote an ad hoc `map3` function that takes three elements of a list at a time. There's probably a better way.
* Still figuring out how to use a Module to make a separate class of utilities to avoid copying code from one day to the next.
* Practiced a bit with documenting my code.

## Day 4

* Had to tinker for a while to get the parsing in a nice shape, but happy with how clean `parse_line` looks in the end.
* A technical question came up that I still need to think about how I'm going to formulate it well.
* Part 2 was almost immediate after having done part 1 in a modular way. Today's puzzle felt particularly smooth for a functional language.
* I figured out (with some pain, I did not find clear OCaml/Dune documentation on this point) a way to put the utilities in a separate library: 
    1. I ran `dune init proj --kind=lib aocutils`.
    2. I define the utility functions there, including a `.mli` compilation unit file. 
    3. I created a symbolic link in day4/vendor: `mkdir vendor && cd vendor && ln -s ../../aocutils/ aocutils`. 
  I'm not sure if this is how one is supposed to do it but it allows me to call `read` from the day4 `main` file, once I put `open Aocutils` at the top. What took me the longest was to figure out how to get `read` into the namespace, so as to avoid having to write `Aocutils.read`. This requires defining the signature, that's what the `.mli` file in the `aocutils` directory is for!
=======