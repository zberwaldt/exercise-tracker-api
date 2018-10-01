DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS exercise;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    bio TEXT,
    twitter TEXT,
    facebook TEXT,
    instagram TEXT
);

CREATE TABLE exercise (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid TEXT NOT NULL,
    details TEXT NOT NULL,
    duration INTEGER NOT NULL,
    date_of TEXT NOT NULL,
    FOREIGN KEY (userid) REFERENCES user (userid)
);

INSERT INTO user (username, userid, password) VALUES ('test', '00000000', '123'), ('test2', '0abc0023', 'password1');

INSERT INTO exercise (userid, details, duration, date_of) VALUES ('00000000', 'running', 32, '2018-09-02'), ('00000000', 'shadow-boxing', 15, '2018-06-15'), ('0abc0023', 'kicking ass', 15, '2000-01-01'), ('0abc0023', 'kicking ass', 15, '2000-01-02'), ('0abc0023', 'kicking ass', 15, '2000-01-03'), ('0abc0023', 'kicking ass', 15, '2000-02-04');