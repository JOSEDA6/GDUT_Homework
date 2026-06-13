alter table INNODB_BUFFER_PAGE
    add POOL_ID bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE
    add BLOCK_ID bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE
    add SPACE bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE
    add PAGE_NUMBER bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE
    add PAGE_TYPE varchar(64) default '' null;

alter table INNODB_BUFFER_PAGE
    add FLUSH_TYPE bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE
    add FIX_COUNT bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE
    add IS_HASHED varchar(3) default '' null;

alter table INNODB_BUFFER_PAGE
    add NEWEST_MODIFICATION bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE
    add OLDEST_MODIFICATION bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE
    add ACCESS_TIME bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE
    add TABLE_NAME varchar(1024) default '' null;

alter table INNODB_BUFFER_PAGE
    add INDEX_NAME varchar(1024) default '' null;

alter table INNODB_BUFFER_PAGE
    add NUMBER_RECORDS bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE
    add DATA_SIZE bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE
    add COMPRESSED_SIZE bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE
    add PAGE_STATE varchar(64) default '' null;

alter table INNODB_BUFFER_PAGE
    add IO_FIX varchar(64) default '' null;

alter table INNODB_BUFFER_PAGE
    add IS_OLD varchar(3) default '' null;

alter table INNODB_BUFFER_PAGE
    add FREE_PAGE_CLOCK bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE
    add IS_STALE varchar(3) default '' null;

