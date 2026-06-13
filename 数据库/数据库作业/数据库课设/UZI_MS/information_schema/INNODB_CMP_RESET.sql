alter table INNODB_CMP_RESET
    add page_size int not null;

alter table INNODB_CMP_RESET
    add compress_ops int not null;

alter table INNODB_CMP_RESET
    add compress_ops_ok int not null;

alter table INNODB_CMP_RESET
    add compress_time int not null;

alter table INNODB_CMP_RESET
    add uncompress_ops int not null;

alter table INNODB_CMP_RESET
    add uncompress_time int not null;

