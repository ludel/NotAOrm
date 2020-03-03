CREATE_TABLES = """
    create table site(id integer constraint site_pk primary key autoincrement, visitor integer DEFAULT 0, url TEXT not null); 
    create table user(id INTEGER constraint user_pk primary key  autoincrement  NOT NULL , name VARCHAR(255) , site site INTEGER, FOREIGN KEY(site) REFERENCES site(ROWID) );
    create table webmaster(id INTEGER constraint webmaster_pk primary key  autoincrement  NOT NULL , email VARCHAR(255) , user user INTEGER, FOREIGN KEY(user) REFERENCES user(ROWID) );
"""

GENERATE_DATA = """
    DELETE FROM site; delete from sqlite_sequence where name='site';
    DELETE FROM webmaster; delete from sqlite_sequence where name='webmaster';
    DELETE FROM user; delete from sqlite_sequence where name='user';
    insert into site ('url', 'visitor') values ('test.com', 10);
    insert into site ('url', 'visitor') values ('google.com', 1000);
    insert into site ('url', 'visitor') values ('google2.com', 100);
    insert into site ('url', 'visitor') values ('aaa.com', 15);
    insert into site ('url', 'visitor') values ('aaa.com', 5);
    insert into site ('url', 'visitor') values ('bbb.com', 5);
    INSERT INTO user ('name', 'site') VALUES ('Marc Dupons',1);
    INSERT INTO user ('name', 'site') VALUES ('Benoit Dubois',2);
    INSERT INTO user ('name', 'site') VALUES ('Sylain Dupain',2);
    INSERT INTO webmaster (user,email) VALUES (1, 'marc.dubois@test.com');
    INSERT INTO webmaster (user,email) VALUES (2, 'ben.dubois@test.com');
    INSERT INTO webmaster (user) VALUES (3);
"""
