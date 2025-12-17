DROP TABLE IF EXISTS realtor_reviews CASCADE;
DROP TABLE IF EXISTS customer_favorites CASCADE;
DROP TABLE IF EXISTS ad_images CASCADE;
DROP TABLE IF EXISTS ads_real_estates CASCADE;
DROP TABLE IF EXISTS ads CASCADE;
DROP TABLE IF EXISTS apartment_profiles CASCADE;
DROP TABLE IF EXISTS house_profiles CASCADE;
DROP TABLE IF EXISTS real_estate_images CASCADE;
DROP TABLE IF EXISTS real_estates CASCADE;
DROP TABLE IF EXISTS real_estate_types CASCADE;
DROP TABLE IF EXISTS customer_profiles CASCADE;
DROP TABLE IF EXISTS realtor_profiles CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS broker_agencies CASCADE;
DROP TABLE IF EXISTS adresses CASCADE;
DROP TABLE IF EXISTS municipals CASCADE;
DROP TABLE IF EXISTS user_types CASCADE;

CREATE TABLE user_types (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE municipals (
    id SERIAL PRIMARY KEY,
    municipal VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE adresses (
    id SERIAL PRIMARY KEY,
    street VARCHAR(100),
    street_no VARCHAR(20),
    postal_code VARCHAR(20),
    postal_area VARCHAR(100),
    municipal INT REFERENCES municipals(id),
	UNIQUE (street,street_no,municipal)
);

CREATE TABLE broker_agencies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    email  VARCHAR(100) UNIQUE,
    adress INT REFERENCES adresses(id)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    type INT NOT NULL REFERENCES user_types(id),
    user_name VARCHAR(100) UNIQUE NOT NULL,
    user_psw VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE realtor_profiles (
    id INT PRIMARY KEY REFERENCES users(id),
    agency INT REFERENCES broker_agencies(id)
);

CREATE TABLE customer_profiles (
    id INT PRIMARY KEY REFERENCES users(id),
    adress INT REFERENCES adresses(id)
);

CREATE TABLE real_estate_types (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE real_estates (
    id SERIAL PRIMARY KEY,
    real_estate_type INT REFERENCES real_estate_types(id),
    municipal INT REFERENCES municipals(id),
    adress INT REFERENCES adresses(id),
    living_space INT,
    no_of_rooms INT
);

CREATE TABLE real_estate_images (
    id SERIAL PRIMARY KEY,
    real_estate INT REFERENCES real_estates(id) ON DELETE CASCADE,
    picture_link VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE house_profiles (
    id INT PRIMARY KEY REFERENCES real_estates(id) ON DELETE CASCADE,
    building_plot FLOAT
);

CREATE TABLE apartment_profiles (
    id INT PRIMARY KEY REFERENCES real_estates(id) ON DELETE CASCADE,
    apartment_id VARCHAR(50),
    floor INT
);

CREATE TABLE ads (
    id SERIAL PRIMARY KEY,
    agreement VARCHAR(255),
    customer INT REFERENCES customer_profiles(id) ON DELETE SET NULL,
    publish_date TIMESTAMPTZ,
	end_date TIMESTAMPTZ,
    realtor INT REFERENCES realtor_profiles(id) ON DELETE SET NULL,
    description TEXT,
	price FLOAT,
	sold_price FLOAT,
	status VARCHAR(50)
);

CREATE TABLE ads_real_estates (
    ad INT REFERENCES ads(id) ON DELETE CASCADE,
    real_estate INT REFERENCES real_estates(id) ON DELETE CASCADE,
    PRIMARY KEY (ad, real_estate)
);

CREATE TABLE ad_images (
    ad INT REFERENCES ads(id) ON DELETE CASCADE,
    picture INT REFERENCES real_estate_images(id) ON DELETE CASCADE,
    PRIMARY KEY (ad, picture)
);

CREATE TABLE customer_favorites (
    customer INT REFERENCES users(id),
    ad INT REFERENCES ads(id) ON DELETE CASCADE,
    PRIMARY KEY (customer, ad)
);

CREATE TABLE realtor_reviews (
    id SERIAL PRIMARY KEY,
    originator INT REFERENCES users(id) ON DELETE SET NULL,
    realtor INT REFERENCES realtor_profiles(id) ON DELETE SET NULL,
    score INT,
    comment TEXT,
	UNIQUE (originator, realtor)
);
