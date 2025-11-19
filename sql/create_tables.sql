-- ================================
-- TABLE 1: POPULAR MOVIES (Existing)
-- DO NOT MODIFY — matches your ETL
-- ================================

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

-- ================================
-- TABLE 2: MOVIE DETAILS (New)
-- ================================

CREATE TABLE IF NOT EXISTS movie_details (
    id BIGINT PRIMARY KEY,
    title TEXT,
    overview TEXT,
    release_date DATE,
    popularity DOUBLE PRECISION,
    vote_count BIGINT,
    vote_average DOUBLE PRECISION,
    poster_path TEXT,
    backdrop_path TEXT,
    original_language TEXT,
    genres JSONB,
    runtime INTEGER,
    budget BIGINT,
    revenue BIGINT,
    homepage TEXT,
    tagline TEXT,
    status TEXT,
    imdb_id TEXT,
    production_companies JSONB,
    production_countries JSONB,
    spoken_languages JSONB,
    last_updated TIMESTAMP DEFAULT now()
);

-- ================================
-- TABLE 3: MOVIE CREDITS (New)
-- ================================

CREATE TABLE IF NOT EXISTS movie_credits (
    movie_id BIGINT REFERENCES movie_details(id),
    cast JSONB,
    crew JSONB,
    last_updated TIMESTAMP DEFAULT now()
);
