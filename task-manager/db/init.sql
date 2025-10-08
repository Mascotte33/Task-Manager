CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    deadline DATE,
    done BOOLEAN DEFAULT FALSE
);
