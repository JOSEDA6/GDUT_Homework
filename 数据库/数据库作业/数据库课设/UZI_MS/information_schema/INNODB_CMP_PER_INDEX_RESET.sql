alter table INNODB_CMP_PER_INDEX_RESET
    add database_name varchar(192) default '' not null;

alter table INNODB_CMP_PER_INDEX_RESET
    add table_name varchar(192) default '' not null;

alter table INNODB_CMP_PER_INDEX_RESET
    add index_name varchar(192) default '' not null;

alter table INNODB_CMP_PER_INDEX_RESET
    add compress_ops int not null;

alter table INNODB_CMP_PER_INDEX_RESET
    add compress_ops_ok int not null;

alter table INNODB_CMP_PER_INDEX_RESET
    add compress_time int not null;

alter table INNODB_CMP_PER_INDEX_RESET
    add uncompress_ops int not null;

alter table INNODB_CMP_PER_INDEX_RESET
    add uncompress_time int not null;

