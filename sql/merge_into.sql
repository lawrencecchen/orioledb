CREATE EXTENSION orioledb;

BEGIN;

CREATE TABLE o_test_1(
	val_1 int UNIQUE, 
	val_2 int
)USING orioledb;

INSERT INTO o_test_1 
	VALUES (10, 2200);
INSERT INTO o_test_1 
	VALUES (20, 1900);

CREATE TABLE o_test_2(
    val_3 int, 
    val_4 int
)USING orioledb;

INSERT INTO o_test_2 
    VALUES (10, 2200);
INSERT INTO o_test_2 
    VALUES (20, 1000);

EXPLAIN VERBOSE
MERGE INTO o_test_1 
    USING o_test_2 
    ON o_test_1.val_1 = o_test_2.val_3
WHEN MATCHED THEN 
    UPDATE SET val_2 = (SELECT COUNT(*) FROM generate_series(1,1));

DROP TABLE o_test_1;
DROP TABLE o_test_2;
COMMIT;

BEGIN;

CREATE TABLE o_test_1 (
  val_1 int,
  val_2 int,
  val_3 int
)USING orioledb;

CREATE UNIQUE INDEX o_test_1_val_1 ON o_test_1 (val_1) INCLUDE (val_2, val_3);

DROP TABLE o_test_1;
COMMIT;

BEGIN;

CREATE TABLE  o_test_circles(
    c circle,
    EXCLUDE USING gist (c WITH &&)
)USING orioledb;

DROP TABLE o_test_circles;
COMMIT;

BEGIN;

CREATE TABLE  o_test_as_values(val_1, val_2)USING orioledb
    AS (VALUES (1, 2));

DROP TABLE o_test_as_values;
COMMIT;

BEGIN;

CREATE TABLE o_test_4(
  val_7 int,
  val_8 int
)USING orioledb;

INSERT INTO o_test_4 
  values(10, 1000);
INSERT INTO o_test_4 
  values(30, 300);
CREATE TABLE o_test_5(
  val_9 int UNIQUE
)USING orioledb;

CREATE TABLE o_test_6(
        val_10 int
    )INHERITS (o_test_5)USING orioledb;

ALTER TABLE o_test_5 ADD COLUMN val_val int;

INSERT INTO o_test_5
    VALUES (10, 2200);
INSERT INTO o_test_5
    VALUES (20, 1900);
INSERT INTO o_test_6 
    VALUES (30, 0, 700);

MERGE INTO o_test_5 USING o_test_4 ON o_test_5.val_9 = o_test_4.val_7
 WHEN MATCHED THEN UPDATE SET val_val = val_val + o_test_4.val_7;

DROP TABLE o_test_4;
DROP TABLE o_test_5;
DROP TABLE o_test_6;
COMMIT;

