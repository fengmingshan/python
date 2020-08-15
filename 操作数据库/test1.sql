/*
Navicat MySQL Data Transfer

Source Server         : MySQL_local
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2020-08-13 10:19:52
*/
DROP DATABASE IF EXISTS test1;
CREATE DATABASE IF NOT EXISTS test1;
USE test1;

SELECT 'CREATING DATABASE STRUCTURE' as 'INFO';
SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `passwd` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('3', 'byj', 'a123456');
INSERT INTO `user` VALUES ('2', 'cx', 'passwd');
INSERT INTO `user` VALUES ('9', 'ggl', 'admin123');
INSERT INTO `user` VALUES ('8', 'wjz', 'test123');
INSERT INTO `user` VALUES ('1', 'xjj', 'admin');
