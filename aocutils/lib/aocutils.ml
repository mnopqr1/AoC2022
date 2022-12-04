let read =
  let next_line () = try Some (input_line stdin) with End_of_file -> None in
  let rec loop acc = 
    match next_line () with
     | None -> acc
     | Some l -> loop (l :: acc)
  in loop []

let mappair f (a, b) = (f a, f b)

let split2 c s = match String.split_on_char c s with
  | [a;b] -> (a,b) | _ -> raise (Invalid_argument ("parsing error on " ^ Char.escaped c))