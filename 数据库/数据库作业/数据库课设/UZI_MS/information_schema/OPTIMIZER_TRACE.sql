alter table OPTIMIZER_TRACE
    add QUERY varchar(65535) default '' not null;

alter table OPTIMIZER_TRACE
    add TRACE varchar(65535) default '' not null;

alter table OPTIMIZER_TRACE
    add MISSING_BYTES_BEYOND_MAX_MEM_SIZE int not null;

alter table OPTIMIZER_TRACE
    add INSUFFICIENT_PRIVILEGES tinyint(1) not null;

