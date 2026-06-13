alter table INNODB_COLUMNS
    add TABLE_ID bigint unsigned default '' not null;

alter table INNODB_COLUMNS
    add NAME varchar(193) default '' not null;

alter table INNODB_COLUMNS
    add POS bigint unsigned default '' not null;

alter table INNODB_COLUMNS
    add MTYPE int not null;

alter table INNODB_COLUMNS
    add PRTYPE int not null;

alter table INNODB_COLUMNS
    add LEN int not null;

alter table INNODB_COLUMNS
    add HAS_DEFAULT int not null;

alter table INNODB_COLUMNS
    add DEFAULT_VALUE text default '' null;

