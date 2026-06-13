alter table INNODB_TABLES
    add TABLE_ID bigint unsigned default '' not null;

alter table INNODB_TABLES
    add NAME varchar(655) default '' not null;

alter table INNODB_TABLES
    add FLAG int not null;

alter table INNODB_TABLES
    add N_COLS int not null;

alter table INNODB_TABLES
    add SPACE bigint not null;

alter table INNODB_TABLES
    add ROW_FORMAT varchar(12) default '' null;

alter table INNODB_TABLES
    add ZIP_PAGE_SIZE int unsigned default '' not null;

alter table INNODB_TABLES
    add SPACE_TYPE varchar(10) default '' null;

alter table INNODB_TABLES
    add INSTANT_COLS int not null;

alter table INNODB_TABLES
    add TOTAL_ROW_VERSIONS int not null;

