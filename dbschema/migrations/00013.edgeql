CREATE MIGRATION m1n6wtteav5zjvnsmch7huqj5ta3kj5iuspwxpreisvh2xqsthvdma
    ONTO m1zmlzzognudjjwh3yw2xyj7th3r3bilf5dpmqcqpiznm4vtri7d2q
{
  ALTER TYPE default::Subject {
      CREATE PROPERTY number: std::int64;
  };
};
