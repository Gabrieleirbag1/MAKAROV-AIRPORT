-- MySQL dump 10.13  Distrib 5.7.44, for Linux (x86_64)
--
-- Host: 172.21.0.5    Database: makarov_airport
-- ------------------------------------------------------
-- Server version	11.4.2-MariaDB-ubu2404

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add banque',7,'add_banque'),(26,'Can change banque',7,'change_banque'),(27,'Can delete banque',7,'delete_banque'),(28,'Can view banque',7,'view_banque'),(29,'Can add user profile',8,'add_userprofile'),(30,'Can change user profile',8,'change_userprofile'),(31,'Can delete user profile',8,'delete_userprofile'),(32,'Can view user profile',8,'view_userprofile'),(33,'Can add reservations',9,'add_reservations'),(34,'Can change reservations',9,'change_reservations'),(35,'Can delete reservations',9,'delete_reservations'),(36,'Can view reservations',9,'view_reservations'),(37,'Can add aeroports',10,'add_aeroports'),(38,'Can change aeroports',10,'change_aeroports'),(39,'Can delete aeroports',10,'delete_aeroports'),(40,'Can view aeroports',10,'view_aeroports'),(41,'Can add avions',11,'add_avions'),(42,'Can change avions',11,'change_avions'),(43,'Can delete avions',11,'delete_avions'),(44,'Can view avions',11,'view_avions'),(45,'Can add staff',12,'add_staff'),(46,'Can change staff',12,'change_staff'),(47,'Can delete staff',12,'delete_staff'),(48,'Can view staff',12,'view_staff'),(49,'Can add vol',13,'add_vol'),(50,'Can change vol',13,'change_vol'),(51,'Can delete vol',13,'delete_vol'),(52,'Can view vol',13,'view_vol');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(9,'reservations','reservations'),(6,'sessions','session'),(10,'structure','aeroports'),(11,'structure','avions'),(12,'structure','staff'),(7,'users','banque'),(8,'users','userprofile'),(13,'vols','vol');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-06-24 11:09:28.301369'),(2,'auth','0001_initial','2024-06-24 11:09:28.514294'),(3,'admin','0001_initial','2024-06-24 11:09:28.560108'),(4,'admin','0002_logentry_remove_auto_add','2024-06-24 11:09:28.567804'),(5,'admin','0003_logentry_add_action_flag_choices','2024-06-24 11:09:28.572214'),(6,'contenttypes','0002_remove_content_type_name','2024-06-24 11:09:28.606247'),(7,'auth','0002_alter_permission_name_max_length','2024-06-24 11:09:28.629246'),(8,'auth','0003_alter_user_email_max_length','2024-06-24 11:09:28.642638'),(9,'auth','0004_alter_user_username_opts','2024-06-24 11:09:28.651460'),(10,'auth','0005_alter_user_last_login_null','2024-06-24 11:09:28.669646'),(11,'auth','0006_require_contenttypes_0002','2024-06-24 11:09:28.671247'),(12,'auth','0007_alter_validators_add_error_messages','2024-06-24 11:09:28.678895'),(13,'auth','0008_alter_user_username_max_length','2024-06-24 11:09:28.691083'),(14,'auth','0009_alter_user_last_name_max_length','2024-06-24 11:09:28.706871'),(15,'auth','0010_alter_group_name_max_length','2024-06-24 11:09:28.726412'),(16,'auth','0011_update_proxy_permissions','2024-06-24 11:09:28.736838'),(17,'auth','0012_alter_user_first_name_max_length','2024-06-24 11:09:28.753116'),(18,'sessions','0001_initial','2024-06-24 11:09:28.772401'),(19,'users','0001_initial','2024-06-24 11:09:28.787964'),(20,'users','0002_userprofile_first_name_userprofile_last_name','2024-06-24 11:09:28.817816'),(21,'users','0003_rename_code_banque_rib','2024-06-24 11:09:28.827445'),(22,'reservations','0001_initial','2024-06-24 16:06:48.753285'),(23,'reservations','0002_alter_reservations_user_ref','2024-06-24 16:06:48.781650'),(24,'structure','0001_initial','2024-06-24 16:06:48.781020'),(25,'structure','0002_alter_avions_image','2024-06-24 16:06:48.796440'),(26,'reservations','0003_alter_reservations_user_ref','2024-06-24 16:06:48.800504'),(27,'structure','0003_alter_staff_level_alter_staff_user_ref','2024-06-24 16:06:48.827973'),(28,'structure','0004_alter_staff_user_ref','2024-06-24 16:06:48.844789'),(29,'vols','0001_initial','2024-06-24 16:06:48.903681'),(30,'vols','0002_remove_vol_aeroport_depart_and_more','2024-06-24 16:06:49.120766'),(31,'vols','0003_vol_numero_vol','2024-06-24 16:06:49.133299'),(32,'vols','0004_rename_numero_vol_vol_numvol','2024-06-24 16:06:49.139583'),(33,'vols','0005_vol_avion_ref','2024-06-24 16:06:49.157099');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservations_reservations`
--

DROP TABLE IF EXISTS `reservations_reservations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reservations_reservations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `vol_ref` int(11) NOT NULL,
  `user_ref` varchar(100) NOT NULL,
  `demande` tinyint(1) NOT NULL,
  `annulation` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservations_reservations`
--

LOCK TABLES `reservations_reservations` WRITE;
/*!40000 ALTER TABLE `reservations_reservations` DISABLE KEYS */;
INSERT INTO `reservations_reservations` VALUES (1,2847271,'gab',0,0),(2,2847271,'gab',0,0),(3,8383936,'dae',0,0);
/*!40000 ALTER TABLE `reservations_reservations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `structure_aeroports`
--

DROP TABLE IF EXISTS `structure_aeroports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `structure_aeroports` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `code_pays` varchar(3) NOT NULL,
  `fuseau` varchar(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `structure_aeroports`
--

LOCK TABLES `structure_aeroports` WRITE;
/*!40000 ALTER TABLE `structure_aeroports` DISABLE KEYS */;
INSERT INTO `structure_aeroports` VALUES (1,'Roissy','FR','UTC+2'),(2,'Barcelona','ES','UTC+2'),(3,'Heathrow','GB','UTC+1'),(4,'JFK','US','UTC-4'),(5,'Haneda','JP','UTC+9'),(6,'Dubai','AE','UTC+4'),(7,'Changi','SG','UTC+8'),(8,'Sheremetyevo','RU','UTC+3'),(9,'Sydney','AU','UTC+10'),(10,'São Paulo-Guarulhos','BR','UTC-3');
/*!40000 ALTER TABLE `structure_aeroports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `structure_avions`
--

DROP TABLE IF EXISTS `structure_avions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `structure_avions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `marque` varchar(100) NOT NULL,
  `modele` varchar(100) NOT NULL,
  `places` int(11) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `structure_avions`
--

LOCK TABLES `structure_avions` WRITE;
/*!40000 ALTER TABLE `structure_avions` DISABLE KEYS */;
INSERT INTO `structure_avions` VALUES (1,'Boeing','777-300ER',365,NULL),(2,'Ilyushin','II-96',300,NULL),(3,'Sukhoi','SSJ100',87,NULL),(4,'BOEING','737-800',162,NULL),(5,'AIRBUS','A220-300',130,NULL),(6,'AIRBUS','A380',500,NULL),(7,'Boeing','747-8 Intercontinental',467,NULL),(8,'Airbus','A320',150,NULL),(9,'Airbus','A350-900',325,NULL),(10,'Boeing','787-9 Dreamliner',296,NULL),(11,'Ilyushin','II-86',350,NULL),(12,'Boeing','747-400',416,NULL);
/*!40000 ALTER TABLE `structure_avions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `structure_staff`
--

DROP TABLE IF EXISTS `structure_staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `structure_staff` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_ref` varchar(100) NOT NULL,
  `level` int(11) NOT NULL,
  `aeroport_ref_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `structure_staff_user_ref_2969b9c5_uniq` (`user_ref`),
  KEY `structure_staff_aeroport_ref_id_f54f0ad4_fk_structure` (`aeroport_ref_id`),
  CONSTRAINT `structure_staff_aeroport_ref_id_f54f0ad4_fk_structure` FOREIGN KEY (`aeroport_ref_id`) REFERENCES `structure_aeroports` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `structure_staff`
--

LOCK TABLES `structure_staff` WRITE;
/*!40000 ALTER TABLE `structure_staff` DISABLE KEYS */;
INSERT INTO `structure_staff` VALUES (1,'darkowen',1,1);
/*!40000 ALTER TABLE `structure_staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_banque`
--

DROP TABLE IF EXISTS `users_banque`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_banque` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `argent` int(11) NOT NULL,
  `rib` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_banque`
--

LOCK TABLES `users_banque` WRITE;
/*!40000 ALTER TABLE `users_banque` DISABLE KEYS */;
INSERT INTO `users_banque` VALUES (1,'gab',853,'11932449'),(2,'dae',2649,'98537539'),(3,'darkowen',1815,'40366100');
/*!40000 ALTER TABLE `users_banque` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_userprofile`
--

DROP TABLE IF EXISTS `users_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_userprofile` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_userprofile`
--

LOCK TABLES `users_userprofile` WRITE;
/*!40000 ALTER TABLE `users_userprofile` DISABLE KEYS */;
INSERT INTO `users_userprofile` VALUES (2,'gab','toto','gabrielgarrone670@gmail.com',0,'Gabriel','Garrone'),(3,'dae','toto','gabrielgarrone670@gmail.com',0,'Gabriel','Garrone'),(4,'darkowen','toto','owen@mail.com',1,'owen','pichot');
/*!40000 ALTER TABLE `users_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vols_vol`
--

DROP TABLE IF EXISTS `vols_vol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vols_vol` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `date_depart` date NOT NULL,
  `date_arrivee` date NOT NULL,
  `heure_depart` time(6) NOT NULL,
  `heure_arrivee` time(6) NOT NULL,
  `prix` int(11) NOT NULL,
  `type` varchar(100) NOT NULL,
  `aeroport_arrivee_ref` int(11) NOT NULL,
  `aeroport_depart_ref` int(11) NOT NULL,
  `numvol` int(11) NOT NULL,
  `avion_ref` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vols_vol`
--

LOCK TABLES `vols_vol` WRITE;
/*!40000 ALTER TABLE `vols_vol` DISABLE KEYS */;
INSERT INTO `vols_vol` VALUES (1,'2024-06-25','2024-06-25','12:51:00.000000','14:57:00.000000',450,'F',2,1,2847271,'A320'),(2,'2024-06-26','2024-06-26','09:59:00.000000','15:05:00.000000',150,'B',5,4,8383936,'737-800');
/*!40000 ALTER TABLE `vols_vol` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-25  8:27:50
