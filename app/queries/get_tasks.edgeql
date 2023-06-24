select Task {
  name,
  code,
  predicted_end_date,
  actual_end_date,
  reasons: {
    name,
    about
  }
}
filter .subject.id = <uuid>$subject_id