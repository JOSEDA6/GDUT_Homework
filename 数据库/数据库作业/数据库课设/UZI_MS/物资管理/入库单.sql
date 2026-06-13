create table 物资管理.入库单
(
    入库单编号   int auto_increment
        primary key,
    采购订单编号 int  null,
    入库日期     date null,
    数量         int  null,
    物资编号     int  null,
    constraint 入库单_ibfk_1
        foreign key (采购订单编号) references 物资管理.采购订单 (采购订单编号),
    constraint 入库单_ibfk_2
        foreign key (物资编号) references 物资管理.物资 (物资编号)
);

create index idx_入库单_物资编号
    on 物资管理.入库单 (物资编号);

create index idx_入库单_采购订单编号
    on 物资管理.入库单 (采购订单编号);

