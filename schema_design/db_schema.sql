CREATE DATABASE movies_database;
\c movies_database
CREATE SCHEMA IF NOT EXISTS content;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    creation_date DATE,
    certificate TEXT,
    file_path VARCHAR(100),
    rating FLOAT8,
    type VARCHAR(20) not null,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE INDEX film_work_creation_date_idx ON content.film_work(creation_date);
CREATE INDEX film_work_rating_idx ON content.film_work(rating);


CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE UNIQUE INDEX genre_name_idx ON content.genre(name);


CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL,
    created_at timestamp with time zone
);

CREATE UNIQUE INDEX film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id);


CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    birth_date DATE,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE INDEX person_full_name_idx ON content.person(full_name);


CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at timestamp with time zone
);

CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work (film_work_id, person_id);
