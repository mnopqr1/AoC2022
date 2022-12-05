module Day5 = struct
  open Aocutils

(** the type [instruction] has three fields: [k] the number of items, [f] from which stack, [t] to which stack. *)
type instruction = {k: int; f: int; t: int}

(* debugging *)
let verbose = false
let debug msg = if verbose then print_string msg
let print_stack s = 
  Seq.iter (fun x -> print_char x) (Stack.to_seq s); print_newline ();;
let print_stacks = Array.iter (print_stack)
let debug_s stacks = if verbose then print_stacks stacks
let string_of_instruction i = 
  "move " ^ string_of_int i.k ^ " from " ^ string_of_int i.f ^ " to " ^ string_of_int i.t

(* parsing *)  
let init_stacks (a : string list) = 
  let n = (String.length (List.hd a) + 1) / 4 in
  let stacks = Array.init n (fun _ -> Stack.create ()) in
  let parse_line l = 
    let xs = List.map (fun i -> l.[4 * i + 1]) (ints n) in
    List.iteri (fun i x -> if not (x = ' ') then Stack.push x stacks.(i)) xs
  in
  let _ = List.iter parse_line @@ List.rev a in 
  stacks

let parse_instructions = List.map
  (fun i -> 
  let xs = String.split_on_char ' ' i in
  let get j = int_of_string (List.nth xs j) in
  {k = get 1; f = get 3; t = get 5})
let parse lines = 
  match split_on (fun x -> String.length x > 1 && x.[1] = '1') lines with
  | [a;b] -> (init_stacks a, parse_instructions (List.tl b))
  | xs -> raise (Invalid_argument ("invalid input: split into " ^ string_of_int (List.length xs)))

(* part 1 *)
let _exec1 stacks i = 
  debug ("\nInstruction: " ^ string_of_instruction i ^ "\n");
  for _ = 1 to i.k do
    let e = Stack.pop stacks.(i.f - 1) in
    Stack.push e stacks.(i.t - 1)
  done;
  debug_s stacks;;

(* part 2 *)
let popn (n: int) (s : 'a Stack.t) : 'a List.t =
  let rec aux n acc = if n = 0 then acc else aux (n-1) (Stack.pop s :: acc) in 
  aux n []
let pushl (xs : 'a List.t) (s: 'a Stack.t) = 
  List.iter (fun x -> Stack.push x s) xs
let exec2 stacks i = 
  debug ("\nInstruction: " ^ string_of_instruction i ^ "\n");
  let xs = popn i.k stacks.(i.f-1) in
  pushl xs stacks.(i.t-1);
  debug_s stacks;;

let () =
  let (stacks, instructions) = parse read in 
  debug "\nInitial stacks:\n";
  debug_s stacks;
  List.iter (exec2 stacks) instructions;
  Array.iter (fun s -> print_char (Stack.pop s)) stacks;
end