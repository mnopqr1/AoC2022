(** [read] reads a file from the stdin as a list of strings, splitting at newline characters.*)
val read : string list

(** [mappair] is a map function on a pair: [mappair f (a,b)] returns [(f a, f b)]*)
val mappair : ('a -> 'b) -> ('a * 'a) -> ('b * 'b)

(** [split2 c s] splits the string [s] into two parts on the character [c].
    Precondition: c occurs exactly once in s.*)
val split2 : char -> string -> string * string

val (>>) : ('a -> 'b) -> ('b -> 'c) -> 'a -> 'c

(** [ints n] returns the list [0;1;...;n-1], where n is a non-negative integer *)
val ints : int -> int list

(** [split_on f xs] returns a list of lists [xs0;xs1;...;xsn], where all elements [x] for which [f x] is true are removed. *)
val split_on : ('a -> bool) -> ('a list) -> 'a list list