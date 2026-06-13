create table 物资管理.出库单
(
    出库单编号 int auto_increment
        primary key,
    客户编号   int  null,
    出库日期   date null,
    数量       int  null,
    物资编号   int  null,
    constraint 出库单_ibfk_1
        foreign key (客户编号) references 物资管理.客户 (客户编号),
    constraint 出库单_ibfk_2
        foreign key (物资编号) references 物资管理.物资 (物资编号)
);

create index idx_出库单_客户编号
    on 物资管理.出库单 (客户编号);

create index idx_出库单_物资编号
    on 物资管理.出库单 (物资编号);

