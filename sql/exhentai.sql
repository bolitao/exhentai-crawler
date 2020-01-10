create table favorites
(
    id    int(255) auto_increment
        primary key,
    title varchar(1500) null,
    link  varchar(500)  null,
    tags  varchar(3000) null
);

create table toplist
(
    id    int auto_increment
        primary key,
    title varchar(1500) null,
    link  varchar(500)  null,
    tags  varchar(3000) null,
    date  datetime      null,
    type  varchar(30)   null
);

