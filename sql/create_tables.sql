-- Popular movies from TMDB API
CREATE TABLE IF NOT EXISTS popular_movies (
    id BIGINT PRIMARY KEY,
    title TEXT,
    vote_average DOUBLE PRECISION,
    vote_count BIGINT,
    popularity DOUBLE PRECISION,
    release_date TEXT,
    original_language TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Full movie details
CREATE TABLE IF NOT EXISTS movie_details (
    id BIGINT PRIMARY KEY,
    title TEXT,
    overview TEXT,
    release_date TEXT,
    popularity DOUBLE PRECISION,
    vote_count BIGINT,
    vote_average DOUBLE PRECISION,
    poster_path TEXT,
    backdrop_path TEXT,
    original_language TEXT,
    genres JSONB,
    runtime INT,
    budget BIGINT,
    revenue BIGINT,
    homepage TEXT,
    tagline TEXT,
    status TEXT,
    imdb_id TEXT,
    production_companies JSONB,
    production_countries JSONB,
    spoken_languages JSONB,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Movie cast and crew
CREATE TABLE IF NOT EXISTS movie_credits (
    movie_id BIGINT PRIMARY KEY,
    movie_cast JSONB,
    movie_crew JSONB,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
