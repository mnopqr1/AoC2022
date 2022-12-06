module Day6 = struct
open Aocutils

let parse l = String.to_seq @@ List.hd l

let nodup l = List.length @@ List.sort_uniq compare l = List.length l
let has_dup (x,y,z,w) = x = y || x = z || x = w || y = z || y = w || z = w
let _solve1 s = 
  let s1, s2, s3 = Seq.drop 1 s, Seq.drop 2 s, Seq.drop 3 s in
  let s4 = Seq.map2 (fun (x,y,z) w -> (x,y,z,w)) (Seq.map2 (fun (x,y) z -> (x,y,z)) (Seq.zip s s1) s2) s3 in
  (Seq.length @@ Seq.take_while has_dup s4) + 4

let n = 14
let solve2 s =
  let rec aux rem buf i =
    if nodup (List.of_seq buf) then i else
    let buf = Seq.append (Seq.drop 1 buf) (Seq.take 1 rem) in
    let rem = Seq.drop 1 rem in
    aux rem buf (i+1)
  in aux (Seq.drop n s) (Seq.take n s) n
let () = 
  print_int @@ 
  solve2    @@ 
  parse read; 
  print_newline ()

end
