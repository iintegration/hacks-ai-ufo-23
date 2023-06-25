insert Subject {
  obj_key := <str>$object_key,
  number := <int64>$number,
  type := <str>$type,
  subtype := <str>$subtype
} unless conflict on .obj_key
