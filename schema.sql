CREATE TABLE IF NOT EXISTS products (
	product_id VARCHAR NOT NULL,
   	score FLOAT NOT NULL,
	time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS product_stat(
	product_id VARCHAR PRIMARY KEY,
   	count INT NOT NULL,
	total_score FLOAT NOT NULL
);

CREATE TRIGGER IF NOT EXISTS update_logging
   AFTER UPDATE
   ON product_stat
BEGIN
 INSERT INTO products(product_id, score) VALUES(NEW.product_id, NEW.total_score - OLD.total_score);
END;

CREATE TRIGGER IF NOT EXISTS insert_logging
   AFTER INSERT
   ON product_stat
BEGIN
 INSERT INTO products(product_id, score) VALUES(NEW.product_id, NEW.total_score);
END;
