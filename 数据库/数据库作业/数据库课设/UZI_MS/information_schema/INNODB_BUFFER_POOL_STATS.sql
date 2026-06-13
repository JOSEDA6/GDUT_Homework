alter table INNODB_BUFFER_POOL_STATS
    add POOL_ID bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add POOL_SIZE bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add FREE_BUFFERS bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add DATABASE_PAGES bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add OLD_DATABASE_PAGES bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add MODIFIED_DATABASE_PAGES bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add PENDING_DECOMPRESS bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add PENDING_READS bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add PENDING_FLUSH_LRU bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add PENDING_FLUSH_LIST bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add PAGES_MADE_YOUNG bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add PAGES_NOT_MADE_YOUNG bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add PAGES_MADE_YOUNG_RATE float(12, 0) not null;

alter table INNODB_BUFFER_POOL_STATS
    add PAGES_MADE_NOT_YOUNG_RATE float(12, 0) not null;

alter table INNODB_BUFFER_POOL_STATS
    add NUMBER_PAGES_READ bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add NUMBER_PAGES_CREATED bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add NUMBER_PAGES_WRITTEN bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add PAGES_READ_RATE float(12, 0) not null;

alter table INNODB_BUFFER_POOL_STATS
    add PAGES_CREATE_RATE float(12, 0) not null;

alter table INNODB_BUFFER_POOL_STATS
    add PAGES_WRITTEN_RATE float(12, 0) not null;

alter table INNODB_BUFFER_POOL_STATS
    add NUMBER_PAGES_GET bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add HIT_RATE bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add YOUNG_MAKE_PER_THOUSAND_GETS bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add NOT_YOUNG_MAKE_PER_THOUSAND_GETS bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add NUMBER_PAGES_READ_AHEAD bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add NUMBER_READ_AHEAD_EVICTED bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add READ_AHEAD_RATE float(12, 0) not null;

alter table INNODB_BUFFER_POOL_STATS
    add READ_AHEAD_EVICTED_RATE float(12, 0) not null;

alter table INNODB_BUFFER_POOL_STATS
    add LRU_IO_TOTAL bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add LRU_IO_CURRENT bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add UNCOMPRESS_TOTAL bigint unsigned default '' not null;

alter table INNODB_BUFFER_POOL_STATS
    add UNCOMPRESS_CURRENT bigint unsigned default '' not null;

