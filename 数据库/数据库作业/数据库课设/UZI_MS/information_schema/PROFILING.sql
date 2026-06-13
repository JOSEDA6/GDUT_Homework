alter table PROFILING
    add QUERY_ID int not null;

alter table PROFILING
    add SEQ int not null;

alter table PROFILING
    add STATE varchar(30) default '' not null;

alter table PROFILING
    add DURATION decimal(905) not null;

alter table PROFILING
    add CPU_USER decimal(905) null;

alter table PROFILING
    add CPU_SYSTEM decimal(905) null;

alter table PROFILING
    add CONTEXT_VOLUNTARY int null;

alter table PROFILING
    add CONTEXT_INVOLUNTARY int null;

alter table PROFILING
    add BLOCK_OPS_IN int null;

alter table PROFILING
    add BLOCK_OPS_OUT int null;

alter table PROFILING
    add MESSAGES_SENT int null;

alter table PROFILING
    add MESSAGES_RECEIVED int null;

alter table PROFILING
    add PAGE_FAULTS_MAJOR int null;

alter table PROFILING
    add PAGE_FAULTS_MINOR int null;

alter table PROFILING
    add SWAPS int null;

alter table PROFILING
    add SOURCE_FUNCTION varchar(30) default '' null;

alter table PROFILING
    add SOURCE_FILE varchar(20) default '' null;

alter table PROFILING
    add SOURCE_LINE int null;

