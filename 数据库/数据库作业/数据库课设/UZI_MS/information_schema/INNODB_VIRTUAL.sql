alter table INNODB_VIRTUAL
    add TABLE_ID bigint unsigned default '' not null;

alter table INNODB_VIRTUAL
    add POS int unsigned default '' not null;

alter table INNODB_VIRTUAL
    add BASE_POS int unsigned default '' not null;

