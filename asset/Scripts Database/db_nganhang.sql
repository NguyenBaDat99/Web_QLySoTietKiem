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
) ENGINE=InnoDB AUTO_INCREMENT=321 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_log`
--

LOCK TABLES `activity_log` WRITE;
/*!40000 ALTER TABLE `activity_log` DISABLE KEYS */;
INSERT INTO `activity_log` VALUES (318,1,'2020-09-13 23:39:19','Đăng nhập',''),(319,1,'2020-09-13 23:39:19','Sửa thông tin tài khoản','Đổi mật khẩu thành công'),(320,1,'2020-09-13 23:39:19','Đăng xuất','');
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
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
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
INSERT INTO `employee` VALUES (1,'admin1','c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec','Quản trị viên - 1','MALE',NULL,'',NULL,1,'ADMIN',NULL,NULL),(2,'nbdat22','89ad306e53aad8fdad00390569f5afad21714bad263de72e9f6b70788f6f45a7579debdb2a9c6dc0d05070eccb50b4f48740e54eb228d2eddca237fb0d00ccf9','Bá Đạt','MALE','1999-07-31','0938622780',NULL,1,'EMPLOYEE','2020-08-28',1),(4,'nxhung54','cefcfa71cafe58e8427df2604dcf892ee99793195e606990748f92c9da9cdc48cbc547f913cbdc205513e9a5318c84014584fd77a046fce28c5ef8cee3ed927e','Xuân Hưng','MALE','1998-09-14','',NULL,1,'EMPLOYEE','2020-09-09',2);
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
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passbook`
--

LOCK TABLES `passbook` WRITE;
/*!40000 ALTER TABLE `passbook` DISABLE KEYS */;
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
  `collect_amount` float DEFAULT '0',
  `spend_amount` float DEFAULT '0',
  `interest_amount` float DEFAULT '0',
  `content` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `passbook_id` (`passbook_id`),
  KEY `customer_id` (`customer_id`),
  KEY `employee_id` (`employee_id`),
  CONSTRAINT `transaction_slip_ibfk_1` FOREIGN KEY (`passbook_id`) REFERENCES `passbook` (`id`),
  CONSTRAINT `transaction_slip_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
  CONSTRAINT `transaction_slip_ibfk_3` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_slip`
--

LOCK TABLES `transaction_slip` WRITE;
/*!40000 ALTER TABLE `transaction_slip` DISABLE KEYS */;
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

-- Dump completed on 2020-09-13 23:41:55
