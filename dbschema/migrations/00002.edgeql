CREATE MIGRATION m1micmlvkj43v4y7y5qzp7i63ydcmiuzksgido6jukbvm7lbkxbheq
    ONTO m1ml4dirrdqxjy46talriq7puftnbazzmb5h6ouwaik5gorb6wkpbq
{
  ALTER TYPE default::Token {
      ALTER PROPERTY value {
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
