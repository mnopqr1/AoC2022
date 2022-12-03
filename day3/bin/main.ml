module Day3 = struct
let read ic =
  let next_line () = try Some (input_line ic) with End_of_file -> None in
  let rec loop acc = 
    match next_line () with
     | None -> acc
     | Some l -> loop (l :: acc)
  in loop []

(** [parse] converts each line to a string sequence *)
let parse = List.map String.to_seq

let sum_list = List.fold_left (+) 0

(** [mid_split] splits a sequence in half, assuming the sequence has even length. *)
let mid_split s = 
  let m = Seq.length s / 2 in (Seq.take m s, Seq.drop m s)

(** [has c] tests if a sequence of characters contains [c] *)
let has c = Seq.exists (Char.equal c)

let value c = let x = Char.code c in if x < 97 then x - 38 else x - 96

(** [find_common2 (a,b)] finds a character that occurs in both a and b, 
    and raises [Not_found] if there is no such character *)
let find_common2 (a,b) = 
  match Seq.find (fun c -> has c b) a with
    | Some x -> x
    | None -> raise Not_found

(** [find_common3 (a1,a2,a3)] finds a character that occurs in a1, a2 and a3, 
    and raises [Not_found] if there is no such character *)
let find_common3 (a1,a2,a3) = 
  match Seq.find (fun c -> has c a2 && has c a3) a1 with
    | Some x -> x
    | None -> raise Not_found

(** [map3 f xs] applies [f] to triples taken from [xs], that is,
    [map3 f [x1;x2;x3;x4;x5;x6;...]] returns [[f(x1,x2,x3);f(x4,x5,x6);...]].
    Precondition: the length of [xs] is divisible by 3.*)
let map3 f xs = 
  let rec aux xs acc =
    match xs with
    | [] -> acc
    | x1 :: x2 :: x3 :: xs -> aux xs (f (x1,x2,x3) :: acc)
    | _ -> raise (Invalid_argument "number of strings not divisible by 3")
  in
  aux xs []

let solve1 ins = 
  let rs = List.map mid_split ins in
  List.map (fun x -> value @@ find_common2 x) rs 
  |> sum_list

let solve2 ins = 
  List.map value (map3 find_common3 ins) |> sum_list

let () = let lines = parse @@ read stdin in
  print_int (solve1 lines); print_newline ();
  print_int (solve2 lines); print_newline ();

end