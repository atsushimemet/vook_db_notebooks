CREATE TABLE IF NOT EXISTS products (
    id bigint PRIMARY KEY AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    url varchar(255) NOT NULL UNIQUE,
    price int NOT NULL,
    knowledge_id bigint NOT NULL,
    platform_id bigint NOT NULL,
    size_id bigint NOT NULL,
    created_at datetime(6) NOT NULL,
    updated_at datetime(6) NOT NULL
)
