alter table INNODB_TABLESTATS
    add TABLE_ID bigint unsigned default '' not null;

alter table INNODB_TABLESTATS
    add NAME varchar(193) default '' not null;

alter table INNODB_TABLESTATS
    add STATS_INITIALIZED varchar(193) default '' not null;

alter table INNODB_TABLESTATS
    add NUM_ROWS bigint unsigned default '' not null;

alter table INNODB_TABLESTATS
    add CLUST_INDEX_SIZE bigint unsigned default '' not null;

alter table INNODB_TABLESTATS
    add OTHER_INDEX_SIZE bigint unsigned default '' not null;

alter table INNODB_TABLESTATS
    add MODIFIED_COUNTER bigint unsigned default '' not null;

alter table INNODB_TABLESTATS
    add AUTOINC bigint unsigned default '' not null;

alter table INNODB_TABLESTATS
    add REF_COUNT int not null;

