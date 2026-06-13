alter table INNODB_METRICS
    add NAME varchar(193) default '' not null;

alter table INNODB_METRICS
    add SUBSYSTEM varchar(193) default '' not null;

alter table INNODB_METRICS
    add COUNT bigint not null;

alter table INNODB_METRICS
    add MAX_COUNT bigint null;

alter table INNODB_METRICS
    add MIN_COUNT bigint null;

alter table INNODB_METRICS
    add AVG_COUNT float(12, 0) null;

alter table INNODB_METRICS
    add COUNT_RESET bigint not null;

alter table INNODB_METRICS
    add MAX_COUNT_RESET bigint null;

alter table INNODB_METRICS
    add MIN_COUNT_RESET bigint null;

alter table INNODB_METRICS
    add AVG_COUNT_RESET float(12, 0) null;

alter table INNODB_METRICS
    add TIME_ENABLED datetime default '' null;

alter table INNODB_METRICS
    add TIME_DISABLED datetime default '' null;

alter table INNODB_METRICS
    add TIME_ELAPSED bigint null;

alter table INNODB_METRICS
    add TIME_RESET datetime default '' null;

alter table INNODB_METRICS
    add STATUS varchar(193) default '' not null;

alter table INNODB_METRICS
    add TYPE varchar(193) default '' not null;

alter table INNODB_METRICS
    add COMMENT varchar(193) default '' not null;

