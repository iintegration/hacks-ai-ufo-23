CREATE MIGRATION m1cdgbfiwwqzmpv3zxovnh72wfpdjirzk6hzc3mj4fdr5mfh5l5klq
    ONTO m1uqxatyydkxnb7vg3hied2kc4cgxkd475ztz7phtumpmjw3y2ww5q
{
  ALTER TYPE default::Subject {
      CREATE PROPERTY photo_url: std::str;
  };
};
