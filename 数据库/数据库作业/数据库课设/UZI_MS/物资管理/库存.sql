create table 物资管理.库存
(
    库存编号 int auto_increment
        primary key,
    物资编号 int null,
    库存数量 int null,
    constraint 库存_ibfk_1
        foreign key (物资编号) references 物资管理.物资 (物资编号)
);

create index 物资编号
    on 物资管理.库存 (物资编号);

