alter table PLUGINS
    add PLUGIN_NAME varchar(64) default '' not null;

alter table PLUGINS
    add PLUGIN_VERSION varchar(20) default '' not null;

alter table PLUGINS
    add PLUGIN_STATUS varchar(10) default '' not null;

alter table PLUGINS
    add PLUGIN_TYPE varchar(80) default '' not null;

alter table PLUGINS
    add PLUGIN_TYPE_VERSION varchar(20) default '' not null;

alter table PLUGINS
    add PLUGIN_LIBRARY varchar(64) default '' null;

alter table PLUGINS
    add PLUGIN_LIBRARY_VERSION varchar(20) default '' null;

alter table PLUGINS
    add PLUGIN_AUTHOR varchar(64) default '' null;

alter table PLUGINS
    add PLUGIN_DESCRIPTION varchar(65535) default '' null;

alter table PLUGINS
    add PLUGIN_LICENSE varchar(80) default '' null;

alter table PLUGINS
    add LOAD_OPTION varchar(64) default '' not null;

