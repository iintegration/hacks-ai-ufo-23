CREATE MIGRATION m1i73cnoccc3o2xlt7jimvgbruuwtbm6r6h4tbrp7rrg6h5b37kqma
    ONTO m13aoadx6v3rwoat7f5iqbmhbipshw3kfzavij5mzq5fvkme4uhrha
{
  ALTER TYPE default::User {
      CREATE MULTI LINK tokens := (.<owner[IS default::Token]);
  };
};
