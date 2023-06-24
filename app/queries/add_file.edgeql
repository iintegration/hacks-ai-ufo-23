insert File {
  owner := (
    select User
    filter .id = <uuid>$user_id
  )
}
