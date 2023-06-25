CREATE MIGRATION m1i5nplspdifprowabburxcojv3k4jzvazclkd2ebpipgnihyaaiga
    ONTO m1n6wtteav5zjvnsmch7huqj5ta3kj5iuspwxpreisvh2xqsthvdma
{
  ALTER TYPE default::Subject {
      ALTER PROPERTY obj_key {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  ALTER TYPE default::Task {
      CREATE CONSTRAINT std::exclusive ON ((.subject, .code));
  };
};
