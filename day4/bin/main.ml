module Day4 = struct
open Aocutils

let (>>) f g = fun x -> g (f x)

(** [parse_line] converts a line of the form "a1-b1,a2-b2" to a pair of pairs of ints *)
let parse_line = (split2 ',') >> mappair ((split2 '-') >> mappair int_of_string)

let parse = List.map parse_line

let contains (c,d) (a,b) = a >= c && b <= d
let cond1 ((a1,b1),(a2,b2)) = contains (a1,b1) (a2,b2) || contains (a2,b2) (a1,b1)
let disjoint (a,b) (c,d) = b < c || d < a
let cond2 ((a,b),(c,d)) = not (disjoint (a,b) (c,d))
let solve cond l = List.length (List.filter cond l)

let () = let lines = parse read in
  print_int (solve cond1 lines); print_newline ();
  print_int (solve cond2 lines); print_newline ();

end