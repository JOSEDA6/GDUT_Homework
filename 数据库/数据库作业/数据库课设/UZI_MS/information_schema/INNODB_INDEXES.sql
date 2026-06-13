alter table INNODB_INDEXES
    add INDEX_ID bigint unsigned default '' not null;

alter table INNODB_INDEXES
    add NAME varchar(193) default '' not null;

alter table INNODB_INDEXES
    add TABLE_ID bigint unsigned default '' not null;

alter table INNODB_INDEXES
    add TYPE int not null;

alter table INNODB_INDEXES
    add N_FIELDS int not null;

alter table INNODB_INDEXES
    add PAGE_NO int not null;

alter table INNODB_INDEXES
    add SPACE int not null;

alter table INNODB_INDEXES
    add MERGE_THRESHOLD int not null;

