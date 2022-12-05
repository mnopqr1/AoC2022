let read =
  let next_line () = try Some (input_line stdin) with End_of_file -> None in
  let rec loop acc = 
    match next_line () with
     | None -> acc
     | Some l -> loop (l :: acc)
  in List.rev (loop [])

let mappair f (a, b) = (f a, f b)

let split2 c s = match String.split_on_char c s with
  | [a;b] -> (a,b) | _ -> raise (Invalid_argument ("parsing error on " ^ Char.escaped c))

let (>>) f g = fun x -> g (f x)

(* let test_ints () = OUnit2.assert_equal (ints 5) ([0;1;2;3;4]);; *)
let ints n =
  let rec aux n acc = 
    if n = 0 then (acc) else aux (n-1) ((n-1) :: acc) in
  aux n []

(* let test_split_on () = OUnit2.assert_equal (split_on (fun x -> x = 0) [1;2;0;3;4]) [[1;2];[3;4]] *)
let split_on (f : 'a -> bool) (xs : 'a list) : 'a list list = 
  let rec aux xs cur acc = 
  match xs with
    | [] -> List.rev (List.rev cur :: acc)
    | x :: xs -> if f x then aux xs [] (List.rev cur :: acc) else aux xs (x :: cur) acc
  in aux xs [] []