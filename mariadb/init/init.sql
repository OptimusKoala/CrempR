CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    role ENUM('user','admin') DEFAULT 'user'
);

INSERT INTO users (username, password, role)
VALUES ('admin', '$2b$12$YGCXO2KekLivRs1/LFz/A.kxq8pK2.EYENG6D9gvgXAtkVtVgITVq', 'admin');