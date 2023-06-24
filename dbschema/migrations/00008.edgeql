CREATE MIGRATION m1yizw2ecozektnwsiqsz7jobygs5tuk563bmogeugv3u6q2nualxa
    ONTO m1cdgbfiwwqzmpv3zxovnh72wfpdjirzk6hzc3mj4fdr5mfh5l5klq
{
  CREATE TYPE default::Reason EXTENDING meta::Created, meta::Modified {
      CREATE REQUIRED LINK task: default::Task;
      CREATE REQUIRED PROPERTY about: std::str;
      CREATE REQUIRED PROPERTY name: std::str;
  };
  ALTER TYPE default::Task {
      CREATE MULTI LINK reasons := (.<task[IS default::Reason]);
  };
  ALTER TYPE default::Subject {
      DROP PROPERTY photo_url;
  };
};
