CREATE MIGRATION m1hdtbbyvc5fq7ofilotks34ulkejnf2hp2qqz7lvfq2hecgamzo3a
    ONTO m1i73cnoccc3o2xlt7jimvgbruuwtbm6r6h4tbrp7rrg6h5b37kqma
{
  CREATE TYPE default::Task EXTENDING meta::Created, meta::Modified {
      CREATE LINK subject: default::Subject;
  };
  ALTER TYPE default::Subject {
      CREATE MULTI LINK tasks := (.<subject[IS default::Task]);
      CREATE PROPERTY general_contractor: std::str;
      CREATE PROPERTY general_designer_key: std::str;
      CREATE PROPERTY number_of_workers: std::int64;
      CREATE PROPERTY square: std::str;
      CREATE PROPERTY subtype: std::str;
      CREATE PROPERTY type: std::str;
  };
};
