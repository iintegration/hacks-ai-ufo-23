insert File {
  owner := (
    select User
    filter .id = <uuid>$user_id
  ),
  origin_filename := <str>$origin_filename
}
