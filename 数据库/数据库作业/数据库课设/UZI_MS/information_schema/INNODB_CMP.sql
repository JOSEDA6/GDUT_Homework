alter table INNODB_CMP
    add page_size int not null;

alter table INNODB_CMP
    add compress_ops int not null;

alter table INNODB_CMP
    add compress_ops_ok int not null;

alter table INNODB_CMP
    add compress_time int not null;

alter table INNODB_CMP
    add uncompress_ops int not null;

alter table INNODB_CMP
    add uncompress_time int not null;

