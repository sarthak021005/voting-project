
CREATE DATABASE IF NOT EXISTS evm;
USE evm;

CREATE TABLE voter(
voter_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50),
email VARCHAR(50),
password VARCHAR(200),
age INT,
address VARCHAR(100),
voted INT DEFAULT 0
);

CREATE TABLE admin(
admin_id INT AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(30),
password VARCHAR(100)
);

INSERT INTO admin(username,password) VALUES('admin','admin');

CREATE TABLE candidate(
candidate_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50),
party VARCHAR(50),
election_id INT
);

CREATE TABLE vote(
vote_id INT AUTO_INCREMENT PRIMARY KEY,
voter_id INT,
candidate_id INT,
election_id INT
);
