alter table INNODB_TRX
    add trx_id bigint unsigned default '' not null;

alter table INNODB_TRX
    add trx_state varchar(13) default '' not null;

alter table INNODB_TRX
    add trx_started datetime default '' not null;

alter table INNODB_TRX
    add trx_requested_lock_id varchar(105) default '' null;

alter table INNODB_TRX
    add trx_wait_started datetime default '' null;

alter table INNODB_TRX
    add trx_weight bigint unsigned default '' not null;

alter table INNODB_TRX
    add trx_mysql_thread_id bigint unsigned default '' not null;

alter table INNODB_TRX
    add trx_query varchar(1024) default '' null;

alter table INNODB_TRX
    add trx_operation_state varchar(64) default '' null;

alter table INNODB_TRX
    add trx_tables_in_use bigint unsigned default '' not null;

alter table INNODB_TRX
    add trx_tables_locked bigint unsigned default '' not null;

alter table INNODB_TRX
    add trx_lock_structs bigint unsigned default '' not null;

alter table INNODB_TRX
    add trx_lock_memory_bytes bigint unsigned default '' not null;

alter table INNODB_TRX
    add trx_rows_locked bigint unsigned default '' not null;

alter table INNODB_TRX
    add trx_rows_modified bigint unsigned default '' not null;

alter table INNODB_TRX
    add trx_concurrency_tickets bigint unsigned default '' not null;

alter table INNODB_TRX
    add trx_isolation_level varchar(16) default '' not null;

alter table INNODB_TRX
    add trx_unique_checks int not null;

alter table INNODB_TRX
    add trx_foreign_key_checks int not null;

alter table INNODB_TRX
    add trx_last_foreign_key_error varchar(256) default '' null;

alter table INNODB_TRX
    add trx_adaptive_hash_latched int not null;

alter table INNODB_TRX
    add trx_adaptive_hash_timeout bigint unsigned default '' not null;

alter table INNODB_TRX
    add trx_is_read_only int not null;

alter table INNODB_TRX
    add trx_autocommit_non_locking int not null;

alter table INNODB_TRX
    add trx_schedule_weight bigint unsigned default '' null;

