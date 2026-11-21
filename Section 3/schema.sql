
-- SECTION 3: NORMALIZED DATABASE SCHEMA

-- 1. Customers
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_segment VARCHAR(20) NOT NULL
        CHECK (customer_segment IN ('Individual', 'Group', 'Corporate')),
    customer_signup_date DATE NOT NULL,
    customer_home_city VARCHAR(100),
    customer_loyalty_tier VARCHAR(20) NOT NULL
        CHECK (customer_loyalty_tier IN ('Gold', 'Platinum', 'Silver'))
);

-- 2. Properties
CREATE TABLE properties (
    property_id INTEGER PRIMARY KEY,
    property_name VARCHAR(150) NOT NULL,
    property_city VARCHAR(100) NOT NULL,
    property_star_rating DECIMAL(3,1),
    property_type VARCHAR(50),
    property_total_rooms INTEGER,
    CONSTRAINT uq_property_name_city
        UNIQUE (property_name, property_city)
);

-- 3. Bookings
CREATE TABLE bookings (
    booking_id BIGINT PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    property_id INTEGER NOT NULL REFERENCES properties(property_id),
    booking_date DATE NOT NULL,
    checkin_date DATE NOT NULL,
    checkout_date DATE NOT NULL,
    CONSTRAINT ck_valid_stay CHECK (checkout_date > checkin_date),
    room_type VARCHAR(50),
    num_rooms INTEGER NOT NULL,
    nights INTEGER NOT NULL,
    booking_channel VARCHAR(50),
    adr DECIMAL(12,2),
    discount_amount DECIMAL(12,2),
    coupon_code VARCHAR(50),
    total_amount DECIMAL(14,2),
    payment_method VARCHAR(50),
    booking_status VARCHAR(20) NOT NULL
);

-- 4. Reviews
CREATE TABLE reviews (
    booking_id BIGINT PRIMARY KEY REFERENCES bookings(booking_id),
    review_rating DECIMAL(4,2) NOT NULL
        CHECK (review_rating BETWEEN 1 AND 10),
    review_date DATE
);

-- This index improves customer booking sequence queries by supporting
-- customer-based filtering and chronological ordering of bookings.
CREATE INDEX idx_bookings_customer_checkin
    ON bookings (customer_id, checkin_date, booking_id);
