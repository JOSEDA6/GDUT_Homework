alter table INNODB_CMPMEM_RESET
    add page_size int not null;

alter table INNODB_CMPMEM_RESET
    add buffer_pool_instance int not null;

alter table INNODB_CMPMEM_RESET
    add pages_used int not null;

alter table INNODB_CMPMEM_RESET
    add pages_free int not null;

alter table INNODB_CMPMEM_RESET
    add relocation_ops bigint not null;

alter table INNODB_CMPMEM_RESET
    add relocation_time int not null;

