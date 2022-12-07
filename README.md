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
* In writing `parse_line`, a technical question came up about applying functions to arguments, I still need to think about how I'm going to formulate it well.
* Part 2 was almost immediate after having done part 1 in a modular way. Today's puzzle felt particularly smooth for a functional language.
* I figured out (with some pain, I did not find clear OCaml/Dune documentation on this point) a way to put the utilities in a separate library: 
    1. I ran `dune init proj --kind=lib aocutils`.
    2. I define the utility functions there, including a `.mli` compilation unit file. 
    3. I created a symbolic link in day4/vendor: `mkdir vendor && cd vendor && ln -s ../../aocutils/ aocutils`. 
  
  I'm not sure *at all* if this is how one is supposed to do it but it allows me to call `read` from the day4 `main` file, once I put `open Aocutils` at the top. What took me the longest was to figure out how to get `read` into the namespace, so as to avoid having to write `Aocutils.read`. This requires defining the signature, that's what the `.mli` file in the `aocutils` directory is for!

## Day 5

* The parsing functions took me a loooong time to get right. I knew what I wanted to do: split the input at the line containing the labels, and then parse the stacks and the instructions individually. But the splitting function took me a while to get right and the stack parsing is a bit ugly (I directly calculate the indices of the columns containing characters).
* I tried to automate testing but failed in battles with dune.
* I found OCaml to be frustratingly uncooperative today and would have been way faster if I did it in Python. The documentation isn't super helpful either. Is there really no easier way to build the list of the first `n` integers than to write the recursion by hand??
* If I want to be able to use it more effectively, I'd need to learn how to pretty print intermediate results.
* I learned how to (temporarily) get rid of warnings in dune: create a file `dune` in the project top-level directory and put
```
(env
  (dev
    (flags (:standard -w -32))))
```

## Day 6

* My solution to part 1 was ugly because it was early and I didn't think about how to do it properly.
* I managed to hack part 2 in OCaml but the runtime was horrible (over a minute).
* Just as a sanity check, after solving both stars in OCaml, I wrote a Python version using a `Counter`, which I was able to do much faster and which gave the answer instantly.
* There probably also exists a thing like `Counter` in OCaml... Or I guess I could just use a list as a map...

## Day 7

* This seemed a big jump in difficulty from the previous days...
* I gave up on OCaml after trying for half an hour and getting frustrated. I then tried a version in "vanilla Python" but it was buggy, so I wrote it a third time (!) in Python with a few classes and objects and it worked fine.
* Being able to do print debugging was very helpful here...
* I did not notice until after solving the puzzle that the input has a special property: we always `ls` before we do `cd`. This makes it easier than I thought it would be, for example, in the puzzle input, the only`cd /`is at the first line -- I abandoned my OCaml solution because I thought it was a possibility that I might have to go to the top of the tree at some point. Also, we always see a directory in an `ls` before doing `cd` into it. Thanks to this last point, [some of my code](https://github.com/mnopqr1/AoC2022/blob/1f14e599970639f64506ecc13aa3dce51cad7404/day7/day7.py#L21) miraculously works and never return `None`...
* If there's any OCaml influence on my Python code it's that I used a lambda to unify my solutions to parts 1 and 2!
