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

 Date: 13/11/2023 21:13:46
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for HRO_LEDGER_DTL
-- ----------------------------
DROP TABLE IF EXISTS `HRO_LEDGER_DTL`;
CREATE TABLE `HRO_LEDGER_DTL` (
  `ID` varchar(36) COLLATE utf8mb4_bin NOT NULL COMMENT '主键id',
  `ACC_ID` varchar(36) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '内部账户ID',
  `ETP_ID` char(36) COLLATE utf8mb4_bin NOT NULL COMMENT '企业编号',
  `INCOME` decimal(11,2) DEFAULT NULL COMMENT '收入',
  `TRAD_DATE` varchar(26) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '交易时间',
  `TRAD_FLOW_NO` varchar(36) COLLATE utf8mb4_bin NOT NULL COMMENT '交易流水号',
  `OUTCOME` decimal(11,2) DEFAULT NULL COMMENT '支出',
  `BALANCE` decimal(11,2) DEFAULT NULL COMMENT '余额',
  `CARD_CODE` varchar(36) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '对方账号',
  `ACC_NAME` varchar(36) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '对方户名',
  `OPEN_BANK` varchar(36) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '对方开户行',
  `TRADE_AIM` varchar(36) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '交易用途',
  `ABSTR` varchar(36) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '摘要',
  `WRITEOFF_STAT` tinyint(4) DEFAULT NULL COMMENT '核销状态 0未核销 1部分核销 2 全部核销',
  `CREATE_TIME` char(26) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建时间YYYY-MM-DD HH24:MI:SS.FFFFFF',
  `LAST_MODI_TIME` char(26) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '最后一次更新时间YYYY-MM-DD HH24:MI:SS.FFFFFF',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='台账明细';

SET FOREIGN_KEY_CHECKS = 1;
