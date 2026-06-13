alter table INNODB_SESSION_TEMP_TABLESPACES
    add ID int unsigned default '' not null;

alter table INNODB_SESSION_TEMP_TABLESPACES
    add SPACE int unsigned default '' not null;

alter table INNODB_SESSION_TEMP_TABLESPACES
    add PATH varchar(4001) default '' not null;

alter table INNODB_SESSION_TEMP_TABLESPACES
    add SIZE bigint unsigned default '' not null;

alter table INNODB_SESSION_TEMP_TABLESPACES
    add STATE varchar(192) default '' not null;

alter table INNODB_SESSION_TEMP_TABLESPACES
    add PURPOSE varchar(192) default '' not null;

