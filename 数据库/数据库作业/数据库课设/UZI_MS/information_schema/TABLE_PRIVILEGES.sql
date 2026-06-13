alter table TABLE_PRIVILEGES
    add GRANTEE varchar(292) default '' not null;

alter table TABLE_PRIVILEGES
    add TABLE_CATALOG varchar(512) default '' not null;

alter table TABLE_PRIVILEGES
    add TABLE_SCHEMA varchar(64) default '' not null;

alter table TABLE_PRIVILEGES
    add TABLE_NAME varchar(64) default '' not null;

alter table TABLE_PRIVILEGES
    add PRIVILEGE_TYPE varchar(64) default '' not null;

alter table TABLE_PRIVILEGES
    add IS_GRANTABLE varchar(3) default '' not null;

