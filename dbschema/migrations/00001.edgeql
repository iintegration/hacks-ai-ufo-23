CREATE MIGRATION m1ml4dirrdqxjy46talriq7puftnbazzmb5h6ouwaik5gorb6wkpbq
    ONTO initial
{
  CREATE MODULE meta IF NOT EXISTS;
  CREATE ABSTRACT TYPE meta::Created {
      CREATE PROPERTY created: std::datetime {
          CREATE REWRITE
              INSERT 
              USING (std::datetime_of_statement());
      };
  };
  CREATE ABSTRACT TYPE meta::Modified {
      CREATE PROPERTY modified: std::datetime {
          CREATE REWRITE
              UPDATE 
              USING (std::datetime_of_statement());
      };
  };
  CREATE TYPE default::Subject EXTENDING meta::Created, meta::Modified {
      CREATE REQUIRED PROPERTY obj_key: std::str;
      CREATE PROPERTY state: std::str;
  };
  CREATE TYPE default::User EXTENDING meta::Created, meta::Modified {
      CREATE REQUIRED PROPERTY login: std::str;
      CREATE REQUIRED PROPERTY password_hash: std::str;
  };
  CREATE TYPE default::Token EXTENDING meta::Created, meta::Modified {
      CREATE REQUIRED LINK owner: default::User;
      CREATE REQUIRED PROPERTY value: std::str;
  };
};
