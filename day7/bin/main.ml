module Day7 = struct

open Aocutils

type tree = Empty | Node of string * tree | Leaf of string * int

type console_line = CD of string | LS | DIR of string | FILE of string * int

let parse = 
  let parse_line s = 
  if String.starts_with ~prefix:"$ cd" s then (CD (String.sub s 5 (String.length s - 5))) else 
  if String.starts_with ~prefix:"$ ls" s then (LS) else 
  let xs = String.split_on_char ' ' s in
    match xs with
    | "dir" :: xs -> DIR (List.hd xs)
    | x :: xs -> FILE (List.hd xs, int_of_string x)
    | _ -> invalid_arg s
   in
  List.map parse_line

(** [get_node a (Node (b, t))] finds the node designated by a in the tree t. *)
let get_node _ _ = Node ("", Leaf ("", 0))
let build_tree (xs : console_line list) : tree = 
  let top = Node ("/", Empty) in
  let rec aux xs (Node (n, t)) =
    match xs with
    | CD a :: xs -> if a = "/" then aux xs top else aux xs (get_node a t)
    | LS :: xs -> read_files xs (Node (n, t))
    | _ -> invalid_arg "error while building tree"
  and 
  read_files _xs (Node (n,t)) = 
    Node (n,t)
  in
  aux xs top
      
let solve _ = 0
let () = read |> parse |> build_tree |> solve |> print_int ;;

end