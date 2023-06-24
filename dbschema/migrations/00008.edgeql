CREATE MIGRATION m1xjdryulj35bsf7n7l3xqbg4pz3z3nuu5zvcfwh4qld5k73kf54vq
    ONTO m1cdgbfiwwqzmpv3zxovnh72wfpdjirzk6hzc3mj4fdr5mfh5l5klq
{
  ALTER TYPE default::Subject {
      ALTER PROPERTY photo_url {
          SET REQUIRED USING (<std::str>{});
      };
  };
};
