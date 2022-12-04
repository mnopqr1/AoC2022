module Day4 = struct
open Aocutils

(** [map2] is a map function on a pair: [map2 f (a,b)] returns [(f a, f b)]*)
let map2 f (a, b) = (f a, f b)

(** [split2 c s] splits the string [s] into two parts on the character [c].
    Precondition: c occurs exactly once in s.*)
let split2 c s = match String.split_on_char c s with
  | [a;b] -> (a,b) | _ -> raise (Invalid_argument ("parsing error on " ^ Char.escaped c))

(** [parse_line] converts a line of the form "a1-b1,a2-b2" to a pair of pairs of ints *)
let parse_line l = map2 (fun x -> map2 int_of_string (split2 '-' x)) (split2 ',' l)
let parse = List.map parse_line

let contains (a,b) (c,d) = a >= c && b <= d
let cond1 ((a,b),(c,d)) = contains (a,b) (c,d) || contains (c,d) (a,b)
let disjoint (a,b) (c,d) = b < c || d < a
let cond2 ((a,b),(c,d)) = not (disjoint (a,b) (c,d))
let solve cond l = List.length (List.filter cond l)

let () = let lines = parse @@ read in
  print_int (solve cond1 lines); print_newline ();
  print_int (solve cond2 lines); print_newline ();

end