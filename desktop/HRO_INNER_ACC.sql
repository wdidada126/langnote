/*
 Navicat Premium Data Transfer

 Source Server         : 5%Edidadas-ucloud_root
 Source Server Type    : MySQL
 Source Server Version : 50733
 Source Host           : 106.75.209.6:3306
 Source Schema         : convertdata

 Target Server Type    : MySQL
 Target Server Version : 50733
 File Encoding         : 65001

 Date: 13/11/2023 15:43:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for HRO_INNER_ACC
-- ----------------------------
DROP TABLE IF EXISTS `HRO_INNER_ACC`;
CREATE TABLE `HRO_INNER_ACC` (
  `ID` varchar(36) COLLATE utf8mb4_bin NOT NULL COMMENT '主键id',
  `ETP_ID` varchar(36) COLLATE utf8mb4_bin NOT NULL COMMENT '公司id',
  `BALANCE` decimal(11,2) DEFAULT NULL COMMENT '余额',
  `INIT_BALANCE` decimal(11,2) DEFAULT NULL COMMENT '初始余额',
  `INPUT` decimal(11,2) DEFAULT NULL COMMENT '流入金额',
  `OUTPUT` decimal(11,2) DEFAULT NULL COMMENT '流出金额',
  `CREATE_TIME` char(26) COLLATE utf8mb4_bin NOT NULL COMMENT '创建时间YYYY-MM-DD HH24:MI:SS.FFFFFF',
  `LAST_MODI_TIME` char(26) COLLATE utf8mb4_bin NOT NULL COMMENT '最后一次更新时间YYYY-MM-DD HH24:MI:SS.FFFFFF',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='内部账户主表';

SET FOREIGN_KEY_CHECKS = 1;
