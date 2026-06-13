create table 物资管理.供应商
(
    供应商编号 int auto_increment
        primary key,
    供应商名称 varchar(255) not null,
    联系人     varchar(255) null,
    联系电话   varchar(20)  null,
    供应商地址 varchar(255) null,
    密码       varchar(255) null
);

create index idx_供应商名称
    on 物资管理.供应商 (供应商名称);

