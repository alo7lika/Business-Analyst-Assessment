
-- C-Q1: Average booking amount by booking sequence
-- Only Completed bookings are considered.

WITH ranked_bookings AS (
    SELECT
        customer_id,
        booking_id,
        total_amount,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY checkin_date, booking_id
        ) AS booking_sequence
    FROM hotel_bookings
    WHERE booking_status = 'Completed'
),
categorized_bookings AS (
    SELECT
        CASE
            WHEN booking_sequence = 1 THEN 'First'
            WHEN booking_sequence = 2 THEN 'Second'
            ELSE 'Third or Later'
        END AS sequence_label,
        CASE
            WHEN booking_sequence = 1 THEN 1
            WHEN booking_sequence = 2 THEN 2
            ELSE 3
        END AS sequence_order,
        total_amount
    FROM ranked_bookings
)
SELECT
    sequence_label,
    ROUND(AVG(total_amount), 2) AS avg_total,
    COUNT(*) AS n
FROM categorized_bookings
GROUP BY sequence_label, sequence_order
ORDER BY sequence_order;


-- C-Q2: Top 5 properties by normalized average review rating
-- Corporate ratings are converted from a 1-10 scale to a 1-5 scale.
-- Reviews associated with Cancelled bookings are excluded.

SELECT
    property_name,
    property_city,
    COUNT(review_rating) AS num_reviews,
    ROUND(
        AVG(
            CASE
                WHEN customer_segment = 'Corporate'
                    THEN review_rating / 2.0
                ELSE review_rating
            END
        ), 2
    ) AS normalized_avg_rating
FROM hotel_bookings
WHERE review_rating IS NOT NULL
  AND booking_status <> 'Cancelled'
GROUP BY property_id, property_name, property_city
HAVING COUNT(review_rating) >= 20
ORDER BY normalized_avg_rating DESC, property_id
LIMIT 5;
