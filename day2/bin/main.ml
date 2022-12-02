let read ic =
  let next_line () = try Some (input_line ic) with End_of_file -> None in
  let rec loop acc = 
    match next_line () with
     | None -> acc
     | Some l -> loop (l :: acc)
  in loop []

let sum_list = List.fold_left (+) 0

type play = Rock | Paper | Scissors
type result = Win | Lose | Draw

let beat p = match p with
 | Rock -> Paper
 | Paper -> Scissors
 | Scissors -> Rock

let let_win p = match p with
 | Rock -> Scissors
 | Paper -> Rock
 | Scissors -> Paper

let beats a b = beat b = a
let value p = match p with | Rock -> 1 | Paper -> 2 | Scissors -> 3

let what_to_play p r = match r with
  | Draw -> p
  | Win -> beat p
  | Lose -> let_win p

let convert1 x = match x with | "A" | "X" -> Rock | "B" | "Y" -> Paper | "C" | "Z" -> Scissors
  | _ -> raise (Invalid_argument x)

let convert2 x = match x with | "X" -> Lose | "Y" -> Draw | "Z" -> Win 
  | _ -> raise (Invalid_argument x)

let round_of_strings a b = (convert1 a, convert1 b)

let score_round (a,b) = 
  let result = if a = b then 3 else if beats b a then 6 else 0
  in value b + result

let parse_line f = fun l -> Scanf.sscanf l "%s %s" f

let parse1 = List.map (parse_line round_of_strings)

let score_round2 p r =
  let p1 = convert1 p in
  let r = convert2 r in
  let p2 = what_to_play p1 r in
  score_round (p1, p2)

let q1 lines = sum_list @@ List.map score_round (parse1 lines)
let q2 lines = sum_list @@ List.map (parse_line score_round2) lines

let () = 
let lines = read Stdlib.stdin in
  print_int (q1 lines); print_newline (); print_int (q2 lines); print_newline ();