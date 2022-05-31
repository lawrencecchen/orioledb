from .base_test import BaseTest
from testgres.exceptions import QueryException


class TriggerTest(BaseTest):

	def test_1(self):
		node = self.node
		node.start()
		node.safe_psql("""
			CREATE EXTENSION IF NOT EXISTS orioledb;
			CREATE TABLE o_test_1(
				val_1 int, 
				val_2 int
			)USING orioledb;
			
			INSERT INTO o_test_1 (val_1, val_2)
				(SELECT val_1, val_1 + 100 FROM generate_series (1, 50) val_1);
			
			CREATE OR REPLACE FUNCTION func_trig_o_test_1()
			RETURNS TRIGGER AS
			$$
			BEGIN						
			INSERT INTO o_test_1(val_1)
				VALUES (OLD.val_1);
			RETURN OLD;
			END;
			$$
			LANGUAGE 'plpgsql';
										
			CREATE TRIGGER trig_o_test_1 AFTER DELETE
			ON o_test_1 FOR EACH ROW
			EXECUTE PROCEDURE func_trig_o_test_1();
										
			DELETE FROM o_test_1 WHERE val_2 % 10 = 0;
		""")
		node.stop(['-m', 'immediate'])

		node.start()
		node.stop()

	def test_2(self):
		node = self.node
		node.start()
		node.safe_psql("""
			CREATE EXTENSION IF NOT EXISTS orioledb;
			CREATE TABLE o_test_1(
				val_1 int, 
				val_2 int
			)USING orioledb;
			CREATE TABLE o_test_2(
				val_3 int,
				val_4 int
			)USING orioledb;
	
			INSERT INTO o_test_1 (val_1, val_2)
				(SELECT val_1, val_1 + 100 FROM generate_series (1, 50) val_1);
			INSERT INTO o_test_2 (val_3, val_4)
				(SELECT val_3, val_3 + 100 FROM generate_series (1, 50) val_3);
			
			CREATE OR REPLACE FUNCTION func_trig_o_test_1()
			RETURNS TRIGGER AS
			$$
			BEGIN						
			INSERT INTO o_test_1(val_1)
				VALUES (OLD.val_1);
			
			RETURN OLD;
			END;
			$$
			LANGUAGE 'plpgsql';
										
			CREATE TRIGGER trig_o_test_12 AFTER DELETE
			ON o_test_1 FOR EACH ROW
			EXECUTE PROCEDURE func_trig_o_test_1();

			DELETE FROM o_test_1 WHERE val_1 = 2;			
		""")
		node.stop(['-m', 'immediate'])

		node.start()
		node.stop()

	def test_3(self):
		node = self.node
		node.start()
		node.safe_psql("""
			CREATE EXTENSION IF NOT EXISTS orioledb;
			CREATE TABLE o_test_1(
				val_1 int, 
				val_2 int,
				val_22 int
			)USING orioledb;
			CREATE TABLE o_test_2(
				val_3 int,
				val_4 int
			)USING orioledb;
			
			INSERT INTO o_test_1 (val_1, val_2, val_22)
				(SELECT val_1, val_1 + 100, val_1 + 20 FROM generate_series (1, 50) val_1);
			INSERT INTO o_test_2 (val_3, val_4)
				(SELECT val_3, val_3 + 100 FROM generate_series (1, 50) val_3);
			
			CREATE OR REPLACE FUNCTION func_trig_o_test_1()
			RETURNS TRIGGER AS
			$$
			BEGIN											
			INSERT INTO o_test_1(val_1)
				VALUES (OLD.val_1);
			RETURN OLD;
			END;
			$$
			LANGUAGE 'plpgsql';
							
			CREATE TRIGGER trig_o_test_1 BEFORE DELETE
			ON o_test_1 FOR EACH ROW
			EXECUTE PROCEDURE func_trig_o_test_1();

			UPDATE o_test_1 SET val_1 = val_1 + 100;				
			
			DELETE FROM o_test_1 WHERE val_22 % 10 = 0;
		""")
		node.stop(['-m', 'immediate'])

		node.start()
		node.stop()

	def test_4(self):
		node = self.node
		node.start()
		node.safe_psql("""
			CREATE EXTENSION IF NOT EXISTS orioledb;
			CREATE TABLE o_test_1(
				val_1 int, 
				val_2 int
			)USING orioledb;
			
			INSERT INTO o_test_1 (val_1, val_2)
				(SELECT val_1, val_1 + 100 FROM generate_series (1, 5) val_1);
            
			CREATE OR REPLACE FUNCTION func_trig_o_test_1()
			RETURNS TRIGGER AS
			$$
			BEGIN											
			INSERT INTO o_test_1(val_1)
				VALUES (OLD.val_1);
			RETURN OLD;
			END;
			$$
			LANGUAGE 'plpgsql';
							
			CREATE TRIGGER trig_o_test_1 AFTER DELETE
			ON o_test_1 FOR EACH STATEMENT
			EXECUTE PROCEDURE func_trig_o_test_1();
            
            DELETE FROM o_test_1 WHERE val_1 = 3;
		""")
		node.stop(['-m', 'immediate'])

		node.start()
		node.stop()

	def test_5(self):
		node = self.node
		node.start()
		node.safe_psql("""
			CREATE EXTENSION IF NOT EXISTS orioledb;
			CREATE TABLE o_test_1(
				val_1 int, 
				val_2 int
			)USING orioledb;

			INSERT INTO o_test_1 (val_1, val_2)
				(SELECT val_1, val_1 + 100 FROM generate_series (1, 5) val_1);

			CREATE OR REPLACE FUNCTION func_trig_o_test_1()
			RETURNS TRIGGER AS
			$$
			BEGIN
			INSERT INTO o_test_1(val_1)
				VALUES (OLD.val_1);
			RETURN OLD;
			END;
			$$
			LANGUAGE 'plpgsql';
											
			CREATE TRIGGER trig_o_test_1 AFTER UPDATE
			ON o_test_1 FOR EACH STATEMENT
			EXECUTE PROCEDURE func_trig_o_test_1();

			UPDATE o_test_1 SET val_1 = val_1 + 100;
		""")
		node.stop(['-m', 'immediate'])

		node.start()
		node.stop()	

	def test_6(self):
		node = self.node
		node.start()
		with self.assertRaises(QueryException) as e:
			node.safe_psql("""
				CREATE EXTENSION IF NOT EXISTS orioledb;
				
				CREATE TABLE o_test_1(
					val_1 int, 
					val_2 int
				)USING orioledb;
					
				INSERT INTO o_test_1 (val_1, val_2)
					(SELECT val_1, val_1 + 100 FROM generate_series (1, 2) val_1);

				CREATE OR REPLACE FUNCTION func_trig_o_test_1()
				RETURNS TRIGGER AS
				$$
				BEGIN										
				UPDATE o_test_1 SET val_2 = OLD.val_2;
				RETURN OLD;
				END;
				$$
				LANGUAGE 'plpgsql';

				CREATE TRIGGER trig_o_test_1 BEFORE DELETE
				ON o_test_1 FOR EACH ROW
				EXECUTE PROCEDURE func_trig_o_test_1();

				DELETE FROM o_test_1 WHERE val_2 % 1 = 0;
							
				ROLLBACK;
			""")
		self.assertEqual(e.exception.message,
						 "ERROR:  tuple to be deleted was already modified by an operation triggered by the current command\n" +
						 "HINT:  Consider using an AFTER trigger instead of a BEFORE trigger to propagate changes to other rows.\n")

		node.stop(['-m', 'immediate'])

		node.start()
		node.stop()












