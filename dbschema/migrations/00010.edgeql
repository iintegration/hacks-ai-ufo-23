CREATE MIGRATION m1eoqjdmbfd3ppfwdzrthf5h6anlas72pu6enad2asfegwpg2vsejq
    ONTO m1pfftzzdlnhg3pmzppb5xjvkpz4mjt3vwfcppy6ivtn6qxgt6yk2a
{
  ALTER TYPE default::File {
      CREATE REQUIRED PROPERTY obj_key: std::str {
          SET REQUIRED USING (<std::str>{});
      };
      ALTER PROPERTY origin_filename {
          SET REQUIRED USING (<std::str>{});
      };
  };
};
