CREATE MIGRATION m1uqxatyydkxnb7vg3hied2kc4cgxkd475ztz7phtumpmjw3y2ww5q
    ONTO m1hdtbbyvc5fq7ofilotks34ulkejnf2hp2qqz7lvfq2hecgamzo3a
{
  CREATE TYPE default::File EXTENDING meta::Created, meta::Modified {
      CREATE REQUIRED LINK owner: default::User;
  };
  ALTER TYPE default::Task {
      ALTER LINK subject {
          SET REQUIRED USING (<default::Subject>{});
      };
      CREATE PROPERTY actual_end_date: std::datetime;
      CREATE REQUIRED PROPERTY code: std::str {
          SET REQUIRED USING (<std::str>{});
      };
      CREATE REQUIRED PROPERTY name: std::str {
          SET REQUIRED USING (<std::str>{});
      };
      CREATE PROPERTY predicted_end_date: std::datetime;
  };
};
