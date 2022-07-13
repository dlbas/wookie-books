create table users
(
    id        integer primary key,
    login     varchar not null,
    password  varchar null,
    pseudonym varchar not null,
    is_active boolean not null
);


create table books
(
    id              integer primary key,
    title           varchar                  not null,
    description     varchar                  not null,
    cover_image_url varchar                  not null,
    price           decimal                  not null,
    unpublished_at  timestamp with time zone null,
    user_id         integer references users (id)
);