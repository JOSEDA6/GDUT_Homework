alter table INNODB_FT_INDEX_TABLE
    add WORD varchar(337) default '' not null;

alter table INNODB_FT_INDEX_TABLE
    add FIRST_DOC_ID bigint unsigned default '' not null;

alter table INNODB_FT_INDEX_TABLE
    add LAST_DOC_ID bigint unsigned default '' not null;

alter table INNODB_FT_INDEX_TABLE
    add DOC_COUNT bigint unsigned default '' not null;

alter table INNODB_FT_INDEX_TABLE
    add DOC_ID bigint unsigned default '' not null;

alter table INNODB_FT_INDEX_TABLE
    add POSITION bigint unsigned default '' not null;

