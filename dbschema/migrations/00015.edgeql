CREATE MIGRATION m1eg4wbnirnwkssnr6eygvd4ycgazqc3tcyqoxhl6abjwgpwom5z4a
    ONTO m1i5nplspdifprowabburxcojv3k4jzvazclkd2ebpipgnihyaaiga
{
  ALTER TYPE default::Task {
      ALTER PROPERTY predicted_end_date {
          SET TYPE std::str USING (<std::str>.predicted_end_date);
      };
  };
};
