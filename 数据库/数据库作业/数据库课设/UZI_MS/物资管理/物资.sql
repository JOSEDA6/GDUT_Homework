create table 物资管理.物资
(
    物资编号 int auto_increment
        primary key,
    物资名称 varchar(255) not null,
    库存数量 int          null,
    单位     varchar(50)  null
);

create index idx_物资名称
    on 物资管理.物资 (物资名称);

