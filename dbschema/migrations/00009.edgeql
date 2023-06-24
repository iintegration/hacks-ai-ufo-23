CREATE MIGRATION m1pfftzzdlnhg3pmzppb5xjvkpz4mjt3vwfcppy6ivtn6qxgt6yk2a
    ONTO m1yizw2ecozektnwsiqsz7jobygs5tuk563bmogeugv3u6q2nualxa
{
  ALTER TYPE default::File {
      CREATE PROPERTY origin_filename: std::str;
  };
};
