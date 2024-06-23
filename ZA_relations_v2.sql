-- relations



-- CREATE TABLE Successful (
--     numReviews INT PRIMARY KEY,
--     bAvgRating FLOAT
-- );

-- CREATE TABLE Popular (
--     numCheckIns INT PRIMARY KEY,
--     numReviews INT,
--     stars FLOAT,
        
-- );

CREATE TABLE zipcodeData (
    zipcode INT PRIMARY KEY,
    avgIncome INT NOT NULL,
    numOfBusinesses INT NOT NULL,
    totalPopulation INT NOT NULL
);

CREATE TABLE Business (
    business_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    state CHAR(2) NOT NULL,
    city VARCHAR(100) NOT NULL,
    zipcode INT NOT NULL,
    numCheckIns INT,
    reviewRating FLOAT,
    reviewCount INT,
    CONSTRAINT fk_Business
        FOREIGN KEY (zipcode) REFERENCES zipcodeData(zipcode)
);

CREATE TABLE Categories (
    business_id VARCHAR(50),
    category VARCHAR(100),
    PRIMARY KEY(business_id, category),
    CONSTRAINT fk_categories
        FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

CREATE TABLE Location(
    business_id VARCHAR(50),
    zipcode INT,
    state VARCHAR(2) NOT NULL,
    city VARCHAR(100) NOT NULL,
    PRIMARY KEY (business_id, zipcode),
    CONSTRAINT fk_Location
        FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

CREATE TABLE Reviews (
    review_id VARCHAR(50) PRIMARY KEY,
    business_id VARCHAR(50),
    numReviews INT,
    bRating FLOAT,
    bAvgRating FLOAT,
    CONSTRAINT fk_Reviews
    FOREIGN KEY (business_id) REFERENCES business(business_id)
);

CREATE TABLE CheckIn (
    business_id VARCHAR(50),
    day VARCHAR(30) NOT NULL,
    hour TIME NOT NULL,
    dailyNumCheckIns INT,
    PRIMARY KEY (business_id,day,hour),
    CONSTRAINT fk_Checkin
        FOREIGN KEY (business_id) REFERENCES business(business_id)
);


-- relationships

CREATE TABLE recievesReview(
    business_id VARCHAR(50),
    review_id VARCHAR(50),
    PRIMARY KEY (review_id),
    CONSTRAINT fk_Recieves
        FOREIGN KEY (business_id) REFERENCES Business(business_id),
        FOREIGN KEY (review_id) REFERENCES Reviews(review_id)
);

CREATE TABLE recievesCheckIn(
    business_id VARCHAR(50),
    day VARCHAR(30) NOT NULL,
    hour TIME NOT NULL,
    PRIMARY KEY (business_id,day,hour),
    CONSTRAINT fk_Recieves
        FOREIGN KEY (business_id) REFERENCES Business(business_id),
        FOREIGN KEY (business_id,day,hour) REFERENCES Checkin(business_id,day,hour)
);

CREATE TABLE type(
    business_id VARCHAR(50),
    category VARCHAR(100),
    PRIMARY KEY(business_id, category),
    CONSTRAINT fk_Type
        FOREIGN KEY (business_id,category) REFERENCES Categories(business_id,category)
);

CREATE TABLE resides_in(
    business_id VARCHAR(50),
    zipcode INT,
    PRIMARY KEY (business_id,zipcode),
    CONSTRAINT fk_ResidesIn
        FOREIGN KEY (zipcode) REFERENCES zipcodeData(zipcode),
        FOREIGN KEY (business_id,zipcode) REFERENCES Location(business_id,zipcode)
);

CREATE TABLE business_is(

    numReviews INT,
    numCheckIns INT,

    PRIMARY KEY(numReviews, numCheckIns)

);
