CREATE DATABASE  IF NOT EXISTS `db_nganhang` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `db_nganhang`;
-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: db_nganhang
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activity_log`
--

DROP TABLE IF EXISTS `activity_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int NOT NULL,
  `activity_time` datetime NOT NULL,
  `activity` varchar(50) NOT NULL,
  `description` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `employee_id` (`employee_id`),
  CONSTRAINT `activity_log_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=280 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_log`
--

LOCK TABLES `activity_log` WRITE;
/*!40000 ALTER TABLE `activity_log` DISABLE KEYS */;
INSERT INTO `activity_log` VALUES (224,2,'2020-09-06 14:50:37','Đăng nhập',''),(225,2,'2020-09-06 14:50:39','Đăng xuất',''),(226,2,'2020-09-06 14:54:02','Đăng nhập',''),(227,2,'2020-09-06 14:54:04','Đăng xuất',''),(228,2,'2020-09-08 14:57:08','Đăng nhập',''),(229,2,'2020-09-08 16:11:46','Đăng nhập',''),(230,2,'2020-09-08 16:13:04','Đăng nhập',''),(231,2,'2020-09-08 17:45:53','Đăng xuất',''),(232,2,'2020-09-08 17:45:55','Đăng nhập',''),(233,2,'2020-09-08 17:50:41','Đăng xuất',''),(234,2,'2020-09-08 17:50:43','Đăng nhập',''),(235,2,'2020-09-09 15:28:56','Đăng nhập',''),(236,2,'2020-09-09 22:00:15','Đăng nhập',''),(237,2,'2020-09-09 22:01:22','Đăng xuất',''),(238,2,'2020-09-09 22:01:45','Đăng nhập',''),(239,2,'2020-09-09 22:12:14','Đăng xuất tự động','Nhân viên không có hoạt động'),(240,1,'2020-09-09 22:12:30','Đăng nhập',''),(241,1,'2020-09-09 22:13:34','Đăng xuất',''),(242,2,'2020-09-09 22:13:37','Đăng nhập',''),(243,2,'2020-09-09 22:25:26','Sửa thông tin tài khoản','Cập nhật thông tin tài khoản thành công'),(244,2,'2020-09-09 22:29:56','Đăng xuất',''),(245,2,'2020-09-09 22:29:57','Đăng nhập',''),(246,2,'2020-09-09 22:37:31','Đăng xuất',''),(247,1,'2020-09-09 22:37:38','Đăng nhập',''),(248,1,'2020-09-09 22:38:10','Đăng xuất',''),(249,4,'2020-09-09 22:38:17','Đăng nhập',''),(250,4,'2020-09-09 22:39:00','Đăng xuất',''),(251,1,'2020-09-09 22:39:08','Đăng nhập',''),(252,1,'2020-09-09 22:39:42','Đăng xuất',''),(253,4,'2020-09-09 22:39:48','Đăng nhập',''),(254,4,'2020-09-09 22:40:41','Sửa thông tin tài khoản','Mật khẩu không chính xác'),(255,4,'2020-09-09 22:40:52','Sửa thông tin tài khoản','Cập nhật thông tin tài khoản thành công'),(256,4,'2020-09-09 22:41:06','Đăng xuất',''),(257,2,'2020-09-09 22:41:12','Đăng nhập',''),(258,2,'2020-09-10 07:18:32','Đăng xuất',''),(259,1,'2020-09-10 07:18:38','Đăng nhập',''),(260,1,'2020-09-10 07:20:58','Đăng xuất',''),(261,1,'2020-09-10 07:21:02','Đăng nhập',''),(262,1,'2020-09-10 07:21:09','Đăng xuất',''),(263,2,'2020-09-10 07:21:51','Đăng nhập',''),(264,2,'2020-09-10 21:18:10','Đăng nhập',''),(265,2,'2020-09-10 22:33:09','Đăng nhập',''),(266,2,'2020-09-11 22:06:39','Đăng xuất',''),(267,4,'2020-09-11 22:06:39','Đăng nhập',''),(268,4,'2020-09-11 22:06:39','Đăng xuất',''),(269,1,'2020-09-11 22:06:39','Đăng nhập',''),(270,1,'2020-09-11 22:06:39','Đăng xuất tự động','Nhân viên truy cập vào trang không được phân quyền'),(271,4,'2020-09-11 22:06:39','Đăng nhập',''),(272,4,'2020-09-11 22:11:03','Đăng xuất tự động','Nhân viên truy cập vào trang không được phân quyền'),(273,2,'2020-09-11 22:11:03','Đăng nhập',''),(274,2,'2020-09-11 22:11:03','Đăng xuất',''),(275,4,'2020-09-11 22:11:03','Đăng nhập',''),(276,4,'2020-09-11 22:11:03','Đăng xuất tự động','Nhân viên truy cập vào trang không được phân quyền'),(277,2,'2020-09-11 22:11:03','Đăng nhập',''),(278,2,'2020-09-11 22:35:23','Đăng xuất',''),(279,2,'2020-09-11 22:35:23','Đăng nhập','');
/*!40000 ALTER TABLE `activity_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `identity_card_number` int NOT NULL,
  `phone` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (18,'23432',2324,NULL),(20,'Bá Đạt',134,'0938622780'),(21,'ádsad',23232,''),(22,'Tường Vân',21154,'0938622780'),(23,'cxv3',121,'0938622780'),(24,'dvvfyh',12124124,'09386223'),(25,'r4',147,''),(26,'12dddxxx',232,NULL),(27,'dsf324',3434,NULL),(28,'bnjhjyj',2133131,NULL),(29,'bnm675',41772,NULL);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(50) NOT NULL,
  `gender` enum('MALE','FEMALE','OTHER') DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `employee_role` enum('ADMIN','EMPLOYEE') DEFAULT NULL,
  `start_work_date` date DEFAULT NULL,
  `position_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `position_id` (`position_id`),
  CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`position_id`) REFERENCES `position` (`id`),
  CONSTRAINT `employee_chk_1` CHECK ((`active` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'admin1','58b5444cf1b6253a4317fe12daff411a78bda0a95279b1d5768ebf5ca60829e78da944e8a9160a0b6d428cb213e813525a72650dac67b88879394ff624da482f','Quản trị viên - 1','MALE',NULL,'',NULL,1,'ADMIN',NULL,NULL),(2,'nbdat22','89ad306e53aad8fdad00390569f5afad21714bad263de72e9f6b70788f6f45a7579debdb2a9c6dc0d05070eccb50b4f48740e54eb228d2eddca237fb0d00ccf9','Bá Đạt','MALE','1999-07-31','0938622780',NULL,1,'EMPLOYEE','2020-08-28',1),(4,'nxhung54','4dff4ea340f0a823f15d3f4f01ab62eae0e5da579ccb851f8db9dfe84c58b2b37b89903a740e1ee172da793a6e79d560e5f7f9bd058a12a280433ed6fa46510a','Xuân Hưng','MALE','1998-09-14','',NULL,1,'EMPLOYEE','2020-09-09',2);
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `passbook`
--

DROP TABLE IF EXISTS `passbook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passbook` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `passbook_type_id` int NOT NULL,
  `open_date` datetime NOT NULL,
  `balance_amount` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_id` (`customer_id`),
  KEY `passbook_type_id` (`passbook_type_id`),
  CONSTRAINT `passbook_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
  CONSTRAINT `passbook_ibfk_2` FOREIGN KEY (`passbook_type_id`) REFERENCES `passbook_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passbook`
--

LOCK TABLES `passbook` WRITE;
/*!40000 ALTER TABLE `passbook` DISABLE KEYS */;
INSERT INTO `passbook` VALUES (1,20,2,'2020-09-11 21:34:12',1250000),(2,20,2,'2020-09-10 22:43:47',10000000),(3,20,2,'2020-07-09 00:00:00',60000000),(4,22,2,'2020-09-11 21:35:59',300000),(5,22,2,'2020-09-09 00:00:00',69000000),(6,23,1,'2020-01-09 00:00:00',100900000),(7,25,2,'2020-09-10 00:00:00',12300000),(8,22,3,'2020-09-10 00:00:00',45000000),(9,18,1,'2020-09-10 00:00:00',12121200),(10,21,1,'2020-09-10 00:00:00',21000000),(11,22,2,'2020-09-10 00:00:00',15000000),(12,21,1,'2020-09-10 00:00:00',12321300000),(13,25,2,'2020-09-10 00:00:00',25000000),(14,18,1,'2020-09-10 00:00:00',12444400),(15,20,2,'2020-01-10 00:00:00',0),(16,21,1,'2020-09-10 00:00:00',2011000),(17,20,1,'2020-09-10 00:00:00',5500000),(18,22,1,'2020-02-10 00:00:00',25000000),(19,25,1,'2020-09-10 00:00:00',5000000),(20,20,3,'2020-09-10 00:00:00',15000000),(21,20,3,'2020-09-10 00:00:00',150000000),(22,20,1,'2020-09-10 00:00:00',100000),(23,20,1,'2020-01-10 00:00:00',15997600),(24,20,1,'2020-09-10 00:00:00',36222000),(25,22,2,'2020-09-10 00:00:00',12234000000),(26,21,1,'2020-09-10 00:00:00',3500000),(27,21,1,'2020-09-10 22:38:51',3000000),(28,26,2,'2020-09-10 22:38:51',1500000),(29,18,1,'2020-09-11 21:14:01',1500000);
/*!40000 ALTER TABLE `passbook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `passbook_type`
--

DROP TABLE IF EXISTS `passbook_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passbook_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `passbook_type_name` varchar(50) NOT NULL,
  `minimum_deposit` float NOT NULL,
  `minimum_deposit_date` int NOT NULL,
  `interest_rate` float NOT NULL,
  `apply_date` datetime NOT NULL,
  `term` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passbook_type`
--

LOCK TABLES `passbook_type` WRITE;
/*!40000 ALTER TABLE `passbook_type` DISABLE KEYS */;
INSERT INTO `passbook_type` VALUES (1,'Sổ không kỳ hạn',100000,15,0.0015,'2020-09-03 00:00:00',0),(2,'Sổ có kỳ hạn 3',100000,15,0.005,'2020-09-03 00:00:00',3),(3,'Sổ có kỳ hạn 6',100000,15,0.0055,'2020-09-03 00:00:00',6);
/*!40000 ALTER TABLE `passbook_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `position`
--

DROP TABLE IF EXISTS `position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `position` (
  `id` int NOT NULL AUTO_INCREMENT,
  `position_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `position`
--

LOCK TABLES `position` WRITE;
/*!40000 ALTER TABLE `position` DISABLE KEYS */;
INSERT INTO `position` VALUES (1,'Nhân viên quản lý'),(2,'Nhân viên giao dịch');
/*!40000 ALTER TABLE `position` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction_slip`
--

DROP TABLE IF EXISTS `transaction_slip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction_slip` (
  `id` int NOT NULL AUTO_INCREMENT,
  `passbook_id` int NOT NULL,
  `customer_id` int NOT NULL,
  `employee_id` int NOT NULL,
  `transaction_date` datetime NOT NULL,
  `transaction_type` enum('WITHDRAW','MATURITY','OPEN_PASSBOOK','DEPOSIT') NOT NULL,
  `transaction_amount` float NOT NULL,
  `interest_amount` float DEFAULT NULL,
  `content` varchar(300) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `passbook_id` (`passbook_id`),
  KEY `customer_id` (`customer_id`),
  KEY `employee_id` (`employee_id`),
  CONSTRAINT `transaction_slip_ibfk_1` FOREIGN KEY (`passbook_id`) REFERENCES `passbook` (`id`),
  CONSTRAINT `transaction_slip_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
  CONSTRAINT `transaction_slip_ibfk_3` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_slip`
--

LOCK TABLES `transaction_slip` WRITE;
/*!40000 ALTER TABLE `transaction_slip` DISABLE KEYS */;
INSERT INTO `transaction_slip` VALUES (3,4,22,2,'2020-09-11 18:20:29','DEPOSIT',2000000,288000,'Gửi tiền'),(4,4,22,2,'2020-09-11 18:24:23','DEPOSIT',1000000,0,'Gửi tiền'),(5,4,22,2,'2020-09-11 18:27:18','DEPOSIT',5000000,0,'Rút tiền'),(6,4,22,2,'2020-09-11 18:27:18','DEPOSIT',5000000,0,'Rút tiền'),(7,4,22,2,'2020-09-11 18:36:47','DEPOSIT',100000000,0,'Rút tiền'),(8,4,22,2,'2020-09-11 18:36:47','DEPOSIT',26152000,0,'Rút tiền'),(10,6,23,2,'2020-03-11 18:36:47','DEPOSIT',3824000,0,'Rút tiền'),(11,6,23,2,'2020-09-11 18:36:47','DEPOSIT',2000000,900000,'Gửi tiền'),(12,6,23,2,'2020-09-11 18:45:26','DEPOSIT',100000000,0,'Gửi tiền'),(13,6,23,2,'2020-09-11 18:45:26','DEPOSIT',2000000,0,'Rút tiền'),(14,1,20,2,'2020-02-11 18:45:26','MATURITY',0,NULL,'Đáo hạn'),(15,1,20,2,'2020-09-11 18:45:26','DEPOSIT',12334400,814070,'Rút tiền'),(16,23,20,2,'2020-02-11 18:45:26','DEPOSIT',500000,12000,'Gửi tiền'),(17,23,20,2,'2020-09-11 18:45:26','DEPOSIT',512000,0,'Rút tiền'),(18,23,20,2,'2020-09-11 20:27:22','DEPOSIT',2350,0,'Rút tiền'),(19,23,20,2,'2020-09-11 20:27:22','DEPOSIT',15000000,0,'Gửi tiền'),(20,18,22,2,'2020-09-11 21:14:01','DEPOSIT',700000,0,'Gửi tiền'),(21,18,22,2,'2020-09-11 21:14:01','DEPOSIT',200000,136500,'Rút tiền'),(22,18,22,2,'2020-09-11 21:14:01','DEPOSIT',7174500,0,'Gửi tiền'),(23,18,22,2,'2020-09-11 21:14:01','DEPOSIT',1999000,0,'Gửi tiền'),(24,18,22,2,'2020-09-11 21:14:01','DEPOSIT',2890000,0,'Gửi tiền'),(25,1,20,2,'2020-09-11 21:14:01','OPEN_PASSBOOK',1250000,NULL,'Mở sổ tiết kiệm cũ'),(26,29,18,2,'2020-09-11 21:14:01','OPEN_PASSBOOK',1500000,NULL,'Tạo sổ tiết kiệm mới'),(27,4,22,2,'2020-09-11 21:14:01','OPEN_PASSBOOK',300000,NULL,'Mở sổ tiết kiệm cũ');
/*!40000 ALTER TABLE `transaction_slip` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-09-12  0:37:10
