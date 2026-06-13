create table 物资管理.采购订单
(
    采购订单编号 int auto_increment
        primary key,
    供应商编号   int  null,
    采购日期     date null,
    交货日期     date null,
    数量         int  null,
    物资编号     int  null,
    constraint 采购订单_ibfk_1
        foreign key (供应商编号) references 物资管理.供应商 (供应商编号),
    constraint 采购订单_ibfk_2
        foreign key (物资编号) references 物资管理.物资 (物资编号)
);

create index idx_采购订单_供应商编号
    on 物资管理.采购订单 (供应商编号);

create index idx_采购订单_物资编号
    on 物资管理.采购订单 (物资编号);

