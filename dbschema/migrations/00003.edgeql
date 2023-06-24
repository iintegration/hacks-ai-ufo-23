CREATE MIGRATION m13aoadx6v3rwoat7f5iqbmhbipshw3kfzavij5mzq5fvkme4uhrha
    ONTO m1micmlvkj43v4y7y5qzp7i63ydcmiuzksgido6jukbvm7lbkxbheq
{
  ALTER TYPE default::User {
      ALTER PROPERTY login {
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
