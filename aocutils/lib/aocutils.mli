(** [read] reads a file from the stdin as a list of strings, splitting at newline characters.*)
val read : string list

(** [mappair] is a map function on a pair: [mappair f (a,b)] returns [(f a, f b)]*)
val mappair : ('a -> 'b) -> ('a * 'a) -> ('b * 'b)

(** [split2 c s] splits the string [s] into two parts on the character [c].
    Precondition: c occurs exactly once in s.*)
val split2 : char -> string -> string * string