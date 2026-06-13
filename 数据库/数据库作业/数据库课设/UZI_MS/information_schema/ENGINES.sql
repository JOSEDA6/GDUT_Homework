alter table ENGINES
    add ENGINE varchar(64) default '' not null;

alter table ENGINES
    add SUPPORT varchar(8) default '' not null;

alter table ENGINES
    add COMMENT varchar(80) default '' not null;

alter table ENGINES
    add TRANSACTIONS varchar(3) default '' null;

alter table ENGINES
    add XA varchar(3) default '' null;

alter table ENGINES
    add SAVEPOINTS varchar(3) default '' null;

