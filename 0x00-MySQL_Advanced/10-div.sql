-- SQL script that creates a function for dividing two integers

DELIMITER $$

DROP FUNCTION IF EXISTS SafeDiv;
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
	RETURN(IF(b = 0, 0, a/b));
END $$

DELIMITER ;
