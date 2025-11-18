CREATE TABLE IF NOT EXISTS popular_movies (
    id BIGINT PRIMARY KEY,
    title TEXT,
    vote_average DOUBLE PRECISION,
    vote_count BIGINT,
    popularity DOUBLE PRECISION,
    release_date DATE,
    original_language TEXT,
    last_updated TIMESTAMP DEFAULT now()
);
