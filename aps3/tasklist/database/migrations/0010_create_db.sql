DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks (
    uuid BINARY(16) PRIMARY KEY,
    description NVARCHAR(1024),
    completed BOOLEAN,
    user_id BINARY(16),
    FOREIGN KEY (user_id) REFERENCES users(uuid)
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    uuid BINARY(16) PRIMARY KEY,
    username NVARCHAR(40),
    first_name NVARCHAR(40),
    last_name NVARCHAR(40)
);
