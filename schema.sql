DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks(
    title TEXT NOT NULL,
    done INTEGER NOT NULL,
    author_ip TEXT NOT NULL,
    created_date TEXT NOT NULL
);
INSERT INTO tasks(title, done, author_ip, created_date) 
VALUES ("Task name 1", 0, "123.45.67.89", "2018-05-08 10:00:00");
INSERT INTO tasks(title, done, author_ip, created_date) 
VALUES ("Foobar", 0, "1.2.3.4", "2018-05-08 11:00:00");
INSERT INTO tasks(title, done, author_ip, created_date) 
VALUES ("Buy a PyCharm license", 0, "1.1.1.1", "2018-05-08 12:00:00");
INSERT INTO tasks(title, done, author_ip, created_date) 
VALUES ("Learn Python", 0, "127.10.01.10", "2018-05-08 13:00:00");