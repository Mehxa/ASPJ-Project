CREATE DATABASE  IF NOT EXISTS `blogdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `blogdb`;
-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: blogdb
-- ------------------------------------------------------
-- Server version	8.0.20

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
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `CommentID` smallint NOT NULL AUTO_INCREMENT,
  `PostID` smallint NOT NULL,
  `UserID` tinyint NOT NULL,
  `DatetimePosted` datetime NOT NULL,
  `Content` mediumtext NOT NULL,
  `Upvotes` mediumint NOT NULL,
  `Downvotes` mediumint NOT NULL,
  PRIMARY KEY (`CommentID`),
  UNIQUE KEY `CommentID_UNIQUE` (`CommentID`),
  KEY `fk_comment_PostID_idx` (`PostID`),
  KEY `fk_comment_UserID_idx` (`UserID`),
  CONSTRAINT `fk_comment_PostID` FOREIGN KEY (`PostID`) REFERENCES `post` (`PostID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_comment_UserID` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment_votes`
--

DROP TABLE IF EXISTS `comment_votes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment_votes` (
  `UserID` tinyint NOT NULL,
  `CommentID` smallint NOT NULL,
  `Vote` tinyint NOT NULL,
  PRIMARY KEY (`UserID`,`CommentID`),
  KEY `fk_comment_votes_CommentID_idx` (`CommentID`),
  CONSTRAINT `fk_comment_votes_CommentID` FOREIGN KEY (`CommentID`) REFERENCES `comment` (`CommentID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_comment_votes_UserID` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment_votes`
--

LOCK TABLES `comment_votes` WRITE;
/*!40000 ALTER TABLE `comment_votes` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment_votes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `FeedbackID` tinyint NOT NULL AUTO_INCREMENT,
  `UserID` tinyint NOT NULL,
  `Reason` tinytext NOT NULL,
  `Content` mediumtext NOT NULL,
  `DatetimePosted` datetime NOT NULL,
  PRIMARY KEY (`FeedbackID`),
  UNIQUE KEY `FeedbackID_UNIQUE` (`FeedbackID`),
  UNIQUE KEY `DatetimePosted_UNIQUE` (`DatetimePosted`),
  KEY `fk_feedback_UserID_idx` (`UserID`),
  CONSTRAINT `fk_feedback_UserID` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post` (
  `PostID` smallint NOT NULL AUTO_INCREMENT,
  `TopicID` tinyint NOT NULL,
  `UserID` tinyint NOT NULL,
  `DatetimePosted` datetime NOT NULL,
  `Title` text NOT NULL,
  `Content` mediumtext NOT NULL,
  `Upvotes` mediumint NOT NULL,
  `Downvotes` mediumint NOT NULL,
  PRIMARY KEY (`PostID`),
  UNIQUE KEY `PostID_UNIQUE` (`PostID`),
  KEY `fk_post_TopicID_idx` (`TopicID`),
  KEY `fk_post_UserID_idx` (`UserID`),
  CONSTRAINT `fk_post_TopicID` FOREIGN KEY (`TopicID`) REFERENCES `topic` (`TopicID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_post_UserID` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
INSERT INTO `post` VALUES (2,1,7,'2020-06-22 15:45:06','What does if __name__ == “__main__”: do?','As stated in the title, what does if __name__ == “__main__”: do? From what I have observed so far, the usage of it is to simply separate the rest of the code from the main code that runs upon the start of the program.',0,0),(4,18,3,'2020-06-27 20:33:41','What is Bootstrap?','There are a lot of questions here related to Bootstrap. I see a lot of people using it. So I tried to research it, and I found the official Bootstrap site, but there was only a download section and a few words after that. Nothing that explains what is it for... I just understood that it is a front-end helper. I have tried to find something by Googling, but found nothing specific. Everything I found is related to the computer science definition.\r\n\r\nSo, my questions are:\r\n\r\nWhat is Bootstrap at all?\r\nWhat is it used for, and how does it help front-end development?\r\nI would also like some more details explaining it.',0,0),(5,1,7,'2020-06-27 20:40:26','Asking the user for input until they give a valid response','How can I reject values like -1, which is a valid int, but nonsensical in this context?',0,0);
/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_votes`
--

DROP TABLE IF EXISTS `post_votes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post_votes` (
  `UserID` tinyint NOT NULL,
  `PostID` smallint NOT NULL,
  `Vote` tinyint NOT NULL,
  PRIMARY KEY (`UserID`,`PostID`),
  KEY `fk_votes_PostID_idx` (`PostID`),
  CONSTRAINT `fk_post_votes_PostID` FOREIGN KEY (`PostID`) REFERENCES `post` (`PostID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_post_votes_UserID` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_votes`
--

LOCK TABLES `post_votes` WRITE;
/*!40000 ALTER TABLE `post_votes` DISABLE KEYS */;
/*!40000 ALTER TABLE `post_votes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reply`
--

DROP TABLE IF EXISTS `reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reply` (
  `ReplyID` smallint NOT NULL AUTO_INCREMENT,
  `CommentID` smallint NOT NULL,
  `UserID` tinyint NOT NULL,
  `Content` mediumtext NOT NULL,
  `DatetimePosted` datetime NOT NULL,
  PRIMARY KEY (`ReplyID`),
  KEY `fk_reply_CommentID_idx` (`CommentID`),
  KEY `fk_reply_UserID_idx` (`UserID`),
  CONSTRAINT `fk_reply_CommentID` FOREIGN KEY (`CommentID`) REFERENCES `comment` (`CommentID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_reply_UserID` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reply`
--

LOCK TABLES `reply` WRITE;
/*!40000 ALTER TABLE `reply` DISABLE KEYS */;
/*!40000 ALTER TABLE `reply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topic`
--

DROP TABLE IF EXISTS `topic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topic` (
  `TopicID` tinyint NOT NULL AUTO_INCREMENT,
  `UserID` tinyint NOT NULL,
  `Content` mediumtext NOT NULL,
  `DatetimePosted` datetime NOT NULL,
  PRIMARY KEY (`TopicID`),
  UNIQUE KEY `TopicID_UNIQUE` (`TopicID`),
  UNIQUE KEY `DatetimePosted_UNIQUE` (`DatetimePosted`),
  KEY `fk_topic_UserID_idx` (`UserID`),
  CONSTRAINT `fk_topic_UserID` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic`
--

LOCK TABLES `topic` WRITE;
/*!40000 ALTER TABLE `topic` DISABLE KEYS */;
INSERT INTO `topic` VALUES (1,1,'Python','2020-06-20 10:05:00'),(2,1,'Java','2020-06-20 10:05:10'),(3,1,'JavaScript','2020-06-20 10:05:21'),(4,1,'C','2020-06-20 10:05:30'),(5,1,'C#','2020-06-20 10:05:37'),(6,1,'C++','2020-06-20 10:05:54'),(7,1,'Objective-C','2020-06-20 10:06:06'),(8,1,'Ruby','2020-06-20 10:06:15'),(9,1,'PHP','2020-06-20 10:06:25'),(10,1,'SQL','2020-06-20 10:06:32'),(11,1,'HTML','2020-06-20 10:10:03'),(12,1,'CSS','2020-06-20 10:10:12'),(13,1,'jQuery','2020-06-20 10:10:20'),(14,1,'Perl','2020-06-20 10:10:30'),(15,1,'XML','2020-06-20 10:10:41'),(16,2,'Object-Oriented Programming','2020-06-20 12:48:20'),(17,4,'RegEx','2020-06-21 13:01:18'),(18,4,'Bootstrap','2020-06-21 13:01:30'),(19,9,'cybersecurity','2020-06-27 02:28:41');
/*!40000 ALTER TABLE `topic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `UserID` tinyint NOT NULL AUTO_INCREMENT,
  `Name` varchar(40) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Username` varchar(30) NOT NULL,
  `Password` varchar(50) NOT NULL,
  `Status` tinytext,
  `Birthday` date NOT NULL,
  `isAdmin` tinyint NOT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `UserID_UNIQUE` (`UserID`),
  UNIQUE KEY `Email_UNIQUE` (`Email`),
  UNIQUE KEY `Username_UNIQUE` (`Username`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Jams','jams@lorem-ipsum.com','NotABot','NotABot123',NULL,'0000-00-00',1),(2,'Siti Sarah','sitisarah@lorem-ipsum.com','CoffeeGirl','CoffeeGirl123',NULL,'2002-02-14',1),(3,'Muhammad','muhammad@lorem-ipsum.com','Mehxa','Mehxa123',NULL,'2002-03-15',1),(4,'Ko Jia Ling','kojialing@lorem-ipsum.com','Kobot','Kobot123',NULL,'2003-01-01',1),(6,'Coco Mak','coconutmak@gmail.com','theauthenticcoconut','nuts@coco',NULL,'2001-02-28',0),(7,'Johnathan Tay Wei Jun','john2004@gmail.com','johnnyjohnny','hohohomerrychristmas',NULL,'1997-10-03',0),(9,'Alexander Han','hansolo02@live.com','hanbaobao','burgerking02',NULL,'1998-01-30',0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-27 22:31:14
