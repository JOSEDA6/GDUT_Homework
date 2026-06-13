alter table INNODB_CACHED_INDEXES
    add SPACE_ID int unsigned default '' not null;

alter table INNODB_CACHED_INDEXES
    add INDEX_ID bigint unsigned default '' not null;

alter table INNODB_CACHED_INDEXES
    add N_CACHED_PAGES bigint unsigned default '' not null;

