insert Token {
  owner := (
    select User
    filter .id = <uuid>$user_id
  ),
  value := <str>$token
}