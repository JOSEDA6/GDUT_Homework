alter table INNODB_TABLESPACES
    add SPACE int unsigned default '' not null;

alter table INNODB_TABLESPACES
    add NAME varchar(655) default '' not null;

alter table INNODB_TABLESPACES
    add FLAG int unsigned default '' not null;

alter table INNODB_TABLESPACES
    add ROW_FORMAT varchar(22) default '' null;

alter table INNODB_TABLESPACES
    add PAGE_SIZE int unsigned default '' not null;

alter table INNODB_TABLESPACES
    add ZIP_PAGE_SIZE int unsigned default '' not null;

alter table INNODB_TABLESPACES
    add SPACE_TYPE varchar(10) default '' null;

alter table INNODB_TABLESPACES
    add FS_BLOCK_SIZE int unsigned default '' not null;

alter table INNODB_TABLESPACES
    add FILE_SIZE bigint unsigned default '' not null;

alter table INNODB_TABLESPACES
    add ALLOCATED_SIZE bigint unsigned default '' not null;

alter table INNODB_TABLESPACES
    add AUTOEXTEND_SIZE bigint unsigned default '' not null;

alter table INNODB_TABLESPACES
    add SERVER_VERSION varchar(10) default '' null;

alter table INNODB_TABLESPACES
    add SPACE_VERSION int unsigned default '' not null;

alter table INNODB_TABLESPACES
    add ENCRYPTION varchar(1) default '' null;

alter table INNODB_TABLESPACES
    add STATE varchar(10) default '' null;

