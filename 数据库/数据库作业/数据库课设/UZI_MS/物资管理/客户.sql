create table 物资管理.客户
(
    客户编号 int auto_increment
        primary key,
    客户名称 varchar(255) not null,
    联系人   varchar(255) null,
    联系电话 varchar(20)  null,
    客户地址 varchar(255) null,
    密码     varchar(255) null
);

create index idx_客户名称
    on 物资管理.客户 (客户名称);

