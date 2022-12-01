let sum_list = List.fold_left (+) 0

let max_list = List.fold_left (max) 0

let solve1 xss = max_list @@ List.map sum_list xss

let solve2 xss = 
  let xs = List.rev @@ List.sort compare (List.map sum_list xss) in
  (List.nth xs 0) + (List.nth xs 1) + (List.nth xs 2)

let read ic =
  let next_line () = try Some (input_line ic) with End_of_file -> None in
  let rec loop acc = 
    match next_line () with
     | None -> acc
     | Some l -> loop (l :: acc)
  in loop []

let parse ls = 
  let rec loop rem xs xss =
    match rem with
      | [] -> xs :: xss
      | l :: ls -> if String.length l > 0 then loop ls (int_of_string l :: xs) xss 
                  else loop ls [] (xs :: xss)
    in loop ls [] []

let () = 
  let xss = parse @@ read stdin in
  print_int (solve1 xss); 
  print_newline (); 
  print_int (solve2 xss);
  print_newline ();
