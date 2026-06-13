alter table INNODB_BUFFER_PAGE_LRU
    add POOL_ID bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE_LRU
    add LRU_POSITION bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE_LRU
    add SPACE bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE_LRU
    add PAGE_NUMBER bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE_LRU
    add PAGE_TYPE varchar(64) default '' null;

alter table INNODB_BUFFER_PAGE_LRU
    add FLUSH_TYPE bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE_LRU
    add FIX_COUNT bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE_LRU
    add IS_HASHED varchar(3) default '' null;

alter table INNODB_BUFFER_PAGE_LRU
    add NEWEST_MODIFICATION bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE_LRU
    add OLDEST_MODIFICATION bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE_LRU
    add ACCESS_TIME bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE_LRU
    add TABLE_NAME varchar(1024) default '' null;

alter table INNODB_BUFFER_PAGE_LRU
    add INDEX_NAME varchar(1024) default '' null;

alter table INNODB_BUFFER_PAGE_LRU
    add NUMBER_RECORDS bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE_LRU
    add DATA_SIZE bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE_LRU
    add COMPRESSED_SIZE bigint unsigned default '' not null;

alter table INNODB_BUFFER_PAGE_LRU
    add COMPRESSED varchar(3) default '' null;

alter table INNODB_BUFFER_PAGE_LRU
    add IO_FIX varchar(64) default '' null;

alter table INNODB_BUFFER_PAGE_LRU
    add IS_OLD varchar(3) default '' null;

alter table INNODB_BUFFER_PAGE_LRU
    add FREE_PAGE_CLOCK bigint unsigned default '' not null;

