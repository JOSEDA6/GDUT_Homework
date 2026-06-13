alter table INNODB_CMPMEM
    add page_size int not null;

alter table INNODB_CMPMEM
    add buffer_pool_instance int not null;

alter table INNODB_CMPMEM
    add pages_used int not null;

alter table INNODB_CMPMEM
    add pages_free int not null;

alter table INNODB_CMPMEM
    add relocation_ops bigint not null;

alter table INNODB_CMPMEM
    add relocation_time int not null;

