CREATE MIGRATION m125srcgr57cjhrlua4uztxiarh3j3ut7ysgfcv5j22t2igpzanojq
    ONTO m1eoqjdmbfd3ppfwdzrthf5h6anlas72pu6enad2asfegwpg2vsejq
{
  ALTER TYPE default::File {
      ALTER PROPERTY obj_key {
          RESET OPTIONALITY;
      };
  };
};
