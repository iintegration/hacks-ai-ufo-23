insert Task {
  subject := (
    select Subject
    filter .obj_key = <str>$obj_key
  ),
  name := <str>$name,
  code := <str>$code,
  predicted_end_date := <optional cal::local_date>$predicted_end_date,
  actual_end_date := <optional cal::local_date>$actual_end_date
} unless conflict on ((.subject, .code)) else (
  update Task set {
    predicted_end_date := <optional cal::local_date>$predicted_end_date,
    actual_end_date := <optional cal::local_date>$actual_end_date
  }
)