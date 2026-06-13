alter table INNODB_FT_INDEX_CACHE
    add WORD varchar(337) default '' not null;

alter table INNODB_FT_INDEX_CACHE
    add FIRST_DOC_ID bigint unsigned default '' not null;

alter table INNODB_FT_INDEX_CACHE
    add LAST_DOC_ID bigint unsigned default '' not null;

alter table INNODB_FT_INDEX_CACHE
    add DOC_COUNT bigint unsigned default '' not null;

alter table INNODB_FT_INDEX_CACHE
    add DOC_ID bigint unsigned default '' not null;

alter table INNODB_FT_INDEX_CACHE
    add POSITION bigint unsigned default '' not null;

