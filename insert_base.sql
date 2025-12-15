---------------------------------------------------------
-- 1. USER TYPES
---------------------------------------------------------
INSERT INTO user_types (type) VALUES
('Kund'),
('Mäklare'),
('Admin');

---------------------------------------------------------
-- 2. MUNICIPALS
---------------------------------------------------------
INSERT INTO municipals (municipal) VALUES
('Stockholm'),
('Göteborg'),
('Malmö');

---------------------------------------------------------
-- 3. ADRESSES
---------------------------------------------------------
INSERT INTO adresses (street, street_no, postal_code, postal_area, municipal) VALUES
('Drottninggatan', '12', '11151', 'Stockholm', 1),
('Avenyn', '33B', '41234', 'Göteborg', 2),
('Södra Förstadsgatan', '7A', '21143', 'Malmö', 3);

---------------------------------------------------------
-- 4. BROKER AGENCIES
---------------------------------------------------------
INSERT INTO broker_agencies (name, email, adress) VALUES
('Fastighetsbyrån Stockholm', 'kontakt@fastighetsbyran.se', 1),
('Svensk Fastighetsförmedling Göteborg', 'info@svenskfast.se', 2),
('Länsförsäkringar Malmö', 'malmo@lansfast.se', 3);

---------------------------------------------------------
-- 5. USERS 
---------------------------------------------------------
INSERT INTO users (type, user_name, user_psw, name, email) VALUES
-- Customers (type=1)
(1, 'anna_k', 'pw1', 'Anna Karlsson', 'anna@example.com'),
(1, 'johan_p', 'pw2', 'Johan Pettersson', 'johan@example.com'),
(1, 'elin_s', 'pw3', 'Elin Svensson', 'elin@example.com'),

-- Realtors (type=2)
(2, 'mikael_a', 'pw4', 'Mikael Andersson', 'mikael@maklare.se'),
(2, 'sara_b', 'pw5', 'Sara Bergström', 'sara@maklare.se'),
(2, 'per_n',  'pw6', 'Per Nilsson', 'per@maklare.se'),

-- Admins (type=3)
(3, 'admin1', 'pw7', 'Admin Ett', 'admin1@system.se'),
(3, 'admin2', 'pw8', 'Admin Två', 'admin2@system.se'),
(3, 'admin3', 'pw9', 'Admin Tre', 'admin3@system.se');

---------------------------------------------------------
-- 6. REALTOR PROFILE (users 4,5,6)
---------------------------------------------------------
INSERT INTO realtor_profile (id, agency) VALUES
(4, 1),
(5, 2),
(6, 3);

---------------------------------------------------------
-- 7. CUSTOMER PROFILE (users 1,2,3)
---------------------------------------------------------
INSERT INTO customer_profile (id, adress) VALUES
(1, 1),
(2, 2),
(3, 3);

---------------------------------------------------------
-- 8. REAL ESTATE TYPES
---------------------------------------------------------
INSERT INTO real_estate_types (type) VALUES
('Villa'),
('Bostadsrätt'),
('Radhus');

---------------------------------------------------------
-- 9. REAL ESTATES
---------------------------------------------------------
INSERT INTO real_estates (real_estate_type, municipal, adress, size, no_of_rooms) VALUES
(1, 1, 1, 150, 6),
(1, 2, 2, 300, 8),
(1, 3, 3, 110, 4),
(2, 1, 1, 45, 2),
(2, 2, 2, 78, 3),
(2, 3, 3, 110, 4);
---------------------------------------------------------
-- 10. REAL ESTATE IMAGES
---------------------------------------------------------
INSERT INTO real_estate_images (real_estate, picture_link) VALUES
(1, 'villa_stockholm_1.jpg'),
(5, 'brf_goteborg_1.jpg'),
(2, 'radhus_malmo_1.jpg');

---------------------------------------------------------
-- 11. HOUSE PROFILE (apply to properties 1 & 3)
---------------------------------------------------------
INSERT INTO house_profile (id, building_plot) VALUES
(1, 780),
(2, 250),
(3, 3000); 

---------------------------------------------------------
-- 12. APARTMENT PROFILE (apply to property 2)
---------------------------------------------------------
INSERT INTO apartment_profile (id, apartment_id, floor) VALUES
(4, 'BRF-203', 2),
(5, 'BRF-203-B', 2),
(6, 'BRF-203-C', 3); 

---------------------------------------------------------
-- 13. ADS
---------------------------------------------------------
INSERT INTO ads (agreement, customer, publish_date, end_date, realtor, description,status, price) VALUES
('Förmedlingsavtal', 1, NOW(), NOW() + INTERVAL '40 days', 4, 'Charmig villa i centrala Stockholm.', 'for sale', 10000000),
('Säljuppdrag',        2, NOW(), NOW() + INTERVAL '20 days', 5, 'Modern bostadsrätt i hjärtat av Göteborg.', 'for sale', 5000000),
('Förmedlingsavtal',  3, NOW(), NOW() + INTERVAL '10 days', 6, 'Mysigt radhus nära parker i Malmö.', 'coming', 6000000);

---------------------------------------------------------
-- 14. ADS-REAL ESTATES
---------------------------------------------------------
INSERT INTO ads_real_estates (ad, real_estate) VALUES
(1, 1),
(2, 2),
(3, 3);

---------------------------------------------------------
-- 15. AD IMAGES
---------------------------------------------------------
INSERT INTO ad_images (ad, picture) VALUES
(1, 1),
(2, 2),
(3, 3);

---------------------------------------------------------
-- 16. USER FAVORITES
---------------------------------------------------------
INSERT INTO user_favorites (usr, ad) VALUES
(1, 2),
(2, 1),
(3, 3);

---------------------------------------------------------
-- 17. REALTOR REVIEWS
---------------------------------------------------------
INSERT INTO realtor_reviews (originator, realtor, score, comment) VALUES
(1, 4, 5, 'Mycket professionell och trevlig.'),
(2, 5, 4, 'Bra kommunikation och tydlig process.'),
(3, 6, 3, 'Helt okej bemötande, men kunde varit snabbare.');
