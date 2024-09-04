create table  profile (id serial ,
job varchar(150),
company varchar(150),
ssn varchar(150),
residence varchar(150),
current_location jsonb,   
blood_group varchar(150) );

CREATE TABLE reservation (
    ID SERIAL PRIMARY KEY,
    checkin_date DATE NOT NULL,
    checkout_date DATE NOT NULL,
    idprofile INT NOT NULL,
	FOREIGN KEY (idprofile) REFERENCES profile(id)
);