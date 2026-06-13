alter table INNODB_TEMP_TABLE_INFO
    add TABLE_ID bigint unsigned default '' not null;

alter table INNODB_TEMP_TABLE_INFO
    add NAME varchar(64) default '' null;

alter table INNODB_TEMP_TABLE_INFO
    add N_COLS int unsigned default '' not null;

alter table INNODB_TEMP_TABLE_INFO
    add SPACE int unsigned default '' not null;

