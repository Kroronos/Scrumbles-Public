CREATE DATABASE `Scrumbles` /*!40100 DEFAULT CHARACTER SET latin1 */;
Use `Scrumbles`;
CREATE TABLE `CardTable` (
  `CardID` bigint(20) NOT NULL,
  `CardType` varchar(45) DEFAULT NULL,
  `CardPriority` int(10) unsigned DEFAULT '1',
  `CardTitle` varchar(45) DEFAULT NULL,
  `CardDescription` longtext,
  `CardCreatedDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CardDueDate` datetime DEFAULT NULL,
  `CardCodeLink` mediumtext,
  `SprintID` bigint(20) unsigned DEFAULT NULL,
  `UserID` bigint(20) DEFAULT NULL,
  `Status` bigint(20) NOT NULL,
  `CardPoints` int(11) DEFAULT '0',
  PRIMARY KEY (`CardID`),
  KEY `UserID_idx` (`UserID`),
  KEY `SprintID_idx` (`SprintID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Table Stores Task Data';
CREATE TABLE `CardTagTable` (
  `TagID` bigint(20) DEFAULT NULL,
  `CardID` bigint(20) DEFAULT NULL,
  KEY `CardID_idx` (`CardID`),
  KEY `TagID_idx` (`TagID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Table to create the multi relationship between tags and cards';
CREATE TABLE `CardTimeLine` (
  `CardID` bigint(20) NOT NULL,
  `AssignedToSprint` datetime DEFAULT NULL,
  `AssignedToUser` datetime DEFAULT NULL,
  `WorkStarted` datetime DEFAULT NULL,
  `Submitted` datetime DEFAULT NULL,
  `Completed` datetime DEFAULT NULL,
  PRIMARY KEY (`CardID`),
  UNIQUE KEY `CardID_UNIQUE` (`CardID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Table Tracks Card Timelines';
CREATE TABLE `CommentTable` (
  `CommentID` bigint(20) NOT NULL,
  `CommentTimeStamp` datetime NOT NULL,
  `CommentContent` longtext,
  `CardID` bigint(20) DEFAULT NULL,
  `UserID` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`CommentID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `EpicTable` (
  `EpicID` bigint(20) DEFAULT NULL,
  `SubitemID` bigint(20) NOT NULL,
  PRIMARY KEY (`SubitemID`),
  UNIQUE KEY `SubitemID_UNIQUE` (`SubitemID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Epic table is an item to item relationship.  EpicID column is a CardID, SubItem is a CardID';
CREATE TABLE `ProjectItemTable` (
  `ProjectID` bigint(20) NOT NULL,
  `ItemID` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `ProjectsTable` (
  `ProjectID` bigint(20) NOT NULL,
  `ProjectName` varchar(45) NOT NULL,
  PRIMARY KEY (`ProjectID`),
  UNIQUE KEY `ProjectID_UNIQUE` (`ProjectID`),
  UNIQUE KEY `ProjectName_UNIQUE` (`ProjectName`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Scrumbles Projects';
CREATE TABLE `ProjectUserTable` (
  `UserID` bigint(20) NOT NULL,
  `ProjectID` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Many to Many Projects to Users';
CREATE TABLE `SprintTable` (
  `SprintID` bigint(20) NOT NULL,
  `StartDate` datetime DEFAULT NULL,
  `DueDate` datetime DEFAULT NULL,
  `SprintName` varchar(45) DEFAULT NULL,
  `ProjectID` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`SprintID`),
  UNIQUE KEY `SprintName_UNIQUE` (`SprintName`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `TagTable` (
  `TagID` bigint(20) NOT NULL,
  `TagName` varchar(45) NOT NULL,
  PRIMARY KEY (`TagID`),
  UNIQUE KEY `idTagTable_UNIQUE` (`TagID`),
  UNIQUE KEY `TagName_UNIQUE` (`TagName`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='A table of Scrumbles Tags';
CREATE TABLE `UserTable` (
  `UserID` bigint(20) NOT NULL,
  `UserName` varchar(45) DEFAULT NULL,
  `UserEmailAddress` varchar(45) DEFAULT NULL,
  `UserPassword` varchar(64) DEFAULT NULL,
  `UserRole` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `UserName_UNIQUE` (`UserName`),
  UNIQUE KEY `UserEmailAddress_UNIQUE` (`UserEmailAddress`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Testingthe creation of a table';

INSERT INTO `ProjectsTable` (`ProjectID`,`ProjectName`) VALUES (0,'New Project');
INSERT INTO `UserTable`
(`UserID`,
`UserName`,
`UserEmailAddress`,
`UserPassword`,
`UserRole`)
VALUES
('0', 'Admin', '', 
'ce1e29c43cf4721dcc39f077631e09e9d8d3b19ba8c8743a3fc18e8eca2a0f73', 'Admin');





