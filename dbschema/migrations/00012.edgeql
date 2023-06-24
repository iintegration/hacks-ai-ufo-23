CREATE MIGRATION m1zmlzzognudjjwh3yw2xyj7th3r3bilf5dpmqcqpiznm4vtri7d2q
    ONTO m125srcgr57cjhrlua4uztxiarh3j3ut7ysgfcv5j22t2igpzanojq
{
  ALTER TYPE default::Task {
      ALTER PROPERTY actual_end_date {
          SET TYPE cal::local_date USING (cal::to_local_date(.actual_end_date, 'UTC'));
      };
      ALTER PROPERTY predicted_end_date {
          SET TYPE cal::local_date USING (cal::to_local_date(.predicted_end_date, 'UTC'));
      };
  };
};
