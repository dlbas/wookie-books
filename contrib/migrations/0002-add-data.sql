insert into users (login, pseudonym, is_active)
values ('luke', 'Luke Skywalker', true),
       ('anakin', 'Anakin Skywalker', true),
       ('dartvaider', 'Dart Vaider', false);

insert into books (title, description, cover_image_url, price, user_id)
values ('How I Met Yoda', 'The story on how I met Mr. Yoda', 'https://example.com/book1', 42, 1),
       ('How I Became Evil', 'Nuff said', 'https://example.com/book2', 24, 2);