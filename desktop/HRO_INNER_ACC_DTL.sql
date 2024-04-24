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

 Date: 13/11/2023 15:43:45
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for HRO_INNER_ACC_DTL
-- ----------------------------
DROP TABLE IF EXISTS `HRO_INNER_ACC_DTL`;
CREATE TABLE `HRO_INNER_ACC_DTL` (
  `ID` varchar(36) COLLATE utf8mb4_bin NOT NULL COMMENT '主键id',
  `P_ID` varchar(36) COLLATE utf8mb4_bin NOT NULL COMMENT '父表id',
  `ACC_UNIT` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '开户单位',
  `NAME` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '账户名称',
  `ACC_NUMBER` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '账户账号',
  `BANK` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '开户行',
  `INIT_BALANCE` decimal(11,2) DEFAULT NULL COMMENT '初始余额',
  `CURRENCY` tinyint(4) DEFAULT NULL COMMENT '币种',
  `SUBJ_NAME` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '科目名称',
  `ACC_TYPE` tinyint(4) DEFAULT NULL COMMENT '账户类型',
  `ACC_NATURE` tinyint(4) DEFAULT NULL COMMENT '账户性质',
  `ACC_ATTRIBUTE` tinyint(4) DEFAULT NULL COMMENT '账户属性',
  `CREATE_TIME` char(26) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建时间YYYY-MM-DD HH24:MI:SS.FFFFFF',
  `LAST_MODI_TIME` char(26) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '最后一次更新时间YYYY-MM-DD HH24:MI:SS.FFFFFF',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='内部账户明细表';

SET FOREIGN_KEY_CHECKS = 1;
