DROP TABLE IF EXISTS username_staging.reviews;
CREATE TABLE username_staging.reviews(
    review                  BIGINT NOT NULL,
    product_id              BIGINT NOT NULL
);
    
INSERT INTO username_staging.reviews(
    review, product_id
)
VALUES(
    s, s
);