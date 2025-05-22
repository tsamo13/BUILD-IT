DROP DATABASE IF EXISTS databases_project;
CREATE DATABASE databases_project;
USE databases_project;

CREATE TABLE User (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100),
    phone_number VARCHAR(20),
    address TEXT
);

CREATE TABLE Citizen (
    user_id INT PRIMARY KEY REFERENCES User(id)
);

CREATE TABLE Construction (
    user_id INT PRIMARY KEY REFERENCES User(id),
    description TEXT,
    location VARCHAR(100),
    available BOOLEAN
);

CREATE TABLE Workshop (
    user_id INT PRIMARY KEY REFERENCES User(id),
    workshop_type VARCHAR(50),
    description TEXT,
    location VARCHAR(100),
    available BOOLEAN
);

CREATE TABLE Project (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    information TEXT,
    construction_type VARCHAR(50),
    start_date DATE,
    location VARCHAR(100),
    status VARCHAR(20) CHECK (status IN ('Pending', 'Active', 'Completed')),
    citizen_id INT REFERENCES Citizen(user_id),
    construction_id INT REFERENCES Construction(user_id),
    workshop_id INT REFERENCES Workshop(user_id)
);

CREATE TABLE License (
    id SERIAL PRIMARY KEY,
    project_id INT REFERENCES Project(id),
    license_type VARCHAR(50),
    license_description TEXT,
    start_date DATE
);

CREATE TABLE Issue (
    id SERIAL PRIMARY KEY,
    project_id INT REFERENCES Project(id),
    construction_id INT REFERENCES Construction(user_id),
    issue_type VARCHAR(50),
    issue_description TEXT,
    new_finish_date DATE
);

CREATE TABLE Review (
    id SERIAL PRIMARY KEY,
    reviewer_id INT REFERENCES User(id),
    reviewee_id INT REFERENCES User(id),
    project_id INT REFERENCES Project(id),
    stars INT CHECK (stars BETWEEN 1 AND 5),
    date DATE,
    comments TEXT
);

CREATE TABLE Request (
    id SERIAL PRIMARY KEY,
    construction_id INT REFERENCES Construction(user_id),
    project_title VARCHAR(100),
    email VARCHAR(100),
    text TEXT
);

CREATE TABLE Appointment (
    id SERIAL PRIMARY KEY,
    construction_id INT REFERENCES Construction(user_id),
    citizen_id INT REFERENCES Citizen(user_id),
    estimated_cost DECIMAL(10, 2)
);

CREATE TABLE ProgressUpdate (
    id SERIAL PRIMARY KEY,
    workshop_id INT REFERENCES Workshop(user_id),
    project_id INT REFERENCES Project(id),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Notification (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES User(id),
    type VARCHAR(50),
    title VARCHAR(100),
    date DATE
);

CREATE TABLE WorkshopRequest (
    id SERIAL PRIMARY KEY,
    construction_id INT REFERENCES Construction(user_id),
    workshop_id INT REFERENCES Workshop(user_id),
    project_id INT REFERENCES Project(id),
    status VARCHAR(20) CHECK (status IN ('Pending', 'Accepted', 'Rejected')),
    message TEXT
);




INSERT INTO user (id, name, email, password, phone_number, address) VALUES
(1, 'Brandon Russell', 'grayanna@christian-moore.com', 'hashed_pw1', '+1-532-061-9610', '01220 Pruitt Ports Suite 470, Matthewfort, PA 84224'),
(2, 'Rhonda Stewart', 'ocohen@hotmail.com', 'hashed_pw2', '+1-786-580-2174x255', '769 Smith Radial, Port Courtneytown, MI 30533'),
(3, 'Jonathan Holloway', 'victoria38@hooper-hernandez.net', 'hashed_pw3', '670.027.3045x466', '511 Merritt Underpass, Jonesfurt, MD 34912'),
(4, 'Amanda Hoffman', 'andrew26@gmail.com', 'hashed_pw4', '001-253-108-6842x465', '129 Reynolds Streets Apt. 705, Pittsmouth, NE 04204'),
(5, 'Frederick Black', 'vincent85@barry.com', 'hashed_pw5', '833-546-0813x830', '95158 Sarah Valleys, Port Rachel, VA 52714'),
(6, 'Dawn Wall', 'randy38@gmail.com', 'hashed_pw6', '+1-099-759-1057x565', '3260 Bennett Greens Apt. 865, West Davidview, PA 42736'),
(7, 'James Willis', 'owenskathy@hotmail.com', 'hashed_pw7', '374-799-5378x94502', '727 Thomas Plains Apt. 553, South Williamport, OR 02327'),
(8, 'James Watts', 'justin65@williams-smith.com', 'hashed_pw8', '048.283.4773', '79884 Abigail Cliff, Russellmouth, AR 75213'),
(9, 'Matthew Holmes', 'ntaylor@compton.com', 'hashed_pw9', '600-658-0036', '1453 Kaitlyn Turnpike, South Jeffrey, NY 87325'),
(10, 'Jeanette Lopez', 'soneill@alvarez.com', 'hashed_pw10', '(175)890-7854', '18195 Kimberly Ford Suite 262, Taylortown, WY 11813');


INSERT INTO Citizen (user_id) VALUES
(1),
(2),
(3);

INSERT INTO Construction (user_id, description, location, available) VALUES
(4, 'Boy receive care American.', 'Lake Albertmouth', TRUE),
(5, 'Particular know bit others.', 'South Anthony', TRUE),
(6, 'Share too public.', 'West Brianview', FALSE),
(7, 'Indeed drive above.', 'Calvintown', TRUE);

INSERT INTO Workshop (user_id, workshop_type, description, location, available) VALUES
(8, 'Electricians', 'Social hour nothing point.', 'Justinborough', TRUE),
(9, 'Plumbers', 'Near today artist.', 'North Scott', TRUE),
(10, 'Painters', 'Study something third.', 'Port Janice', FALSE);

INSERT INTO Project (name, information, construction_type, start_date, location, status, citizen_id, construction_id, workshop_id) VALUES
('Dream House', 'Yard understand three page.', 'Construction', '2025-06-01', 'Lake Lauren', 'Pending', 1, 4, 8),
('Office Reno', 'Look he space let possible exist Mrs.', 'Renovation', '2025-05-20', 'Karenburgh', 'Active', 2, 5, 9);

INSERT INTO License (project_id, license_type, license_description, start_date) VALUES
(1, 'Building', 'General permit for foundation', '2025-05-01'),
(2, 'Renovation', 'Office internal redesign', '2025-05-10');

INSERT INTO Issue (project_id, construction_id, issue_type, issue_description, new_finish_date) VALUES
(1, 4, 'Καθυστέρηση', 'Supply chain delay', '2025-06-30'),
(2, 5, 'Υλικά', 'Wrong material delivered', '2025-06-25');

INSERT INTO Review (reviewer_id, reviewee_id, project_id, stars, comments, date) VALUES
(1, 4, 1, 5, 'Excellent collaboration', '2025-05-15'),
(2, 5, 1, 4, 'Very responsive', '2025-05-16'),
(4, 8, 1, 5, 'Great quality work', '2025-05-17');




select * from user;