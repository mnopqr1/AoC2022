let read =
  let next_line () = try Some (input_line stdin) with End_of_file -> None in
  let rec loop acc = 
    match next_line () with
     | None -> acc
     | Some l -> loop (l :: acc)
  in loop []