CREATE TABLE politician(
    politician_id INT GENERATED ALWAYS AS IDENTITY,
    full_name TEXT NOT NULL,
	house_or_senate VARCHAR(10) NOT NULL,
	state VARCHAR ( 100 ) NOT NULL,
	district INT, NOT NULL,
	party VARCHAR(255),
	website TEXT,
    PRIMARY KEY(politician_id)
);

CREATE TABLE transportation(
   transportation_id INT GENERATED ALWAYS AS IDENTITY,
   politician_id INT,
   info_or_not VARCHAR(50) NOT NULL, 
   quotes TEXT,
   website_found TEXT,
   PRIMARY KEY(transportation_id),
   CONSTRAINT fk_politician
      FOREIGN KEY(politician_id) 
	  REFERENCES politician(politician_id)
	  ON DELETE CASCADE
);
