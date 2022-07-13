insert into users (id, login, pseudonym, is_active)
values (1, 'luke', 'Luke Skywalker', true),
       (2, 'anakin', 'Anakin Skywalker', true),
       (3, 'dartvaider', 'Dart Vaider', false);

insert into books (id, title, description, cover_image_url, price, user_id)
values (1, 'How I Met Yoda', 'The story on how I met Mr. Yoda', 'https://example.com/book1', 42, 1),
       (2, 'How I Became Evil', 'Nuff said', 'https://example.com/book2', 24, 2);