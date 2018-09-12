DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS exercise;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    user_id TEXT UNIQUE NOT NULL,
    profile_id INTEGER,
    FOREIGN KEY (profile_id) REFERENCES profile(id)
);

CREATE TABLE exercise (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    details TEXT NOT NULL,
    duration INTEGER NOT NULL,
    date_of TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (user_id)
);

CREATE TABLE profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    username TEXT NOT NULL, 
    firstname TEXT,
    lastname TEXT,
    bio TEXT,
    twitter TEXT,
    github TEXT,
    FOREIGN KEY (user_id) REFERENCES user (user_id)
)

INSERT INTO user (username, user_id) VALUES ('test', '00000000'), ('test2', '0abc0023');

INSERT INTO exercise (user_id, details, duration, date_of) VALUES ('00000000', 'running', 32, '2018-09-02'), ('00000000', 'shadow-boxing', 15, '2018-06-15'), ('0abc0023', 'kicking ass', 15, '2000-01-01'), ('0abc0023', 'kicking ass', 15, '2000-01-02'), ('0abc0023', 'kicking ass', 15, '2000-01-03'), ('0abc0023', 'kicking ass', 15, '2000-02-04');