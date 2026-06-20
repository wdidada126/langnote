# MySQL表五要素

 			`ID` bigint unsigned NOT NULL AUTO_INCREMENT  COMMENT '主键',
             `CREATED_BY` varchar(32) NOT NULL   DEFAULT '' COMMENT '创建人',
             `CREATED_AT` datetime NOT NULL  DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
             `UPDATED_BY` varchar(32) NOT NULL   DEFAULT '' COMMENT '更新人',
             `UPDATED_AT` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',