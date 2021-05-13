CREATE DATABASE Forum;
use Forum;

CREATE TABLE All_post (
  Post_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Which_subforum varchar(100) NOT NULL,
  PostDate datetime DEFAULT current_timestamp(),
  Author varchar(100) DEFAULT NULL,
  PRIMARY KEY (Post_ID)
);

CREATE TABLE Post_GPU (
  Post_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Post_title varchar(255)  NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Post_ID),
  CONSTRAINT Post_GPU_FK FOREIGN KEY (Post_ID) REFERENCES All_post (Post_ID)
);

CREATE TABLE Comment_GPU (
  Comment_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Comment_content mediumtext  NOT NULL,
  Post_ID bigint(20) unsigned NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Comment_ID),
  KEY Comment_GPU_FK (Post_ID),
  CONSTRAINT Comment_GPU_FK FOREIGN KEY (Post_ID) REFERENCES Post_GPU (Post_ID)
);

CREATE TABLE Reply_GPU (
  Reply_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Reply_content mediumtext  NOT NULL,
  Comment_ID bigint(20) unsigned DEFAULT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Reply_ID),
  KEY Reply_GPU_FK (Comment_ID),
  CONSTRAINT Reply_GPU_FK FOREIGN KEY (Comment_ID) REFERENCES Comment_GPU (Comment_ID)
);

CREATE TABLE Post_CPU (
  Post_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Post_title varchar(255)  NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Post_ID),
  CONSTRAINT Post_CPU_FK FOREIGN KEY (Post_ID) REFERENCES All_post (Post_ID)
);

CREATE TABLE Comment_CPU (
  Comment_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Comment_content mediumtext  NOT NULL,
  Post_ID bigint(20) unsigned NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Comment_ID),
  KEY Comment_CPU_FK (Post_ID),
  CONSTRAINT Comment_CPU_FK FOREIGN KEY (Post_ID) REFERENCES Post_CPU (Post_ID)
);

CREATE TABLE Reply_CPU (
  Reply_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Reply_content mediumtext  NOT NULL,
  Comment_ID bigint(20) unsigned DEFAULT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Reply_ID),
  KEY Reply_CPU_FK (Comment_ID),
  CONSTRAINT Reply_CPU_FK FOREIGN KEY (Comment_ID) REFERENCES Comment_CPU (Comment_ID)
);

CREATE TABLE Post_Laptop (
  Post_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Post_title varchar(255)  NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Post_ID),
  CONSTRAINT Post_Laptop_FK FOREIGN KEY (Post_ID) REFERENCES All_post (Post_ID)
);

CREATE TABLE Comment_Laptop (
  Comment_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Comment_content mediumtext  NOT NULL,
  Post_ID bigint(20) unsigned NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Comment_ID),
  KEY Comment_Laptop_FK (Post_ID),
  CONSTRAINT Comment_Laptop_FK FOREIGN KEY (Post_ID) REFERENCES Post_Laptop (Post_ID)
);

CREATE TABLE Reply_Laptop (
  Reply_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Reply_content mediumtext  NOT NULL,
  Comment_ID bigint(20) unsigned DEFAULT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Reply_ID),
  KEY Reply_Laptop_FK (Comment_ID),
  CONSTRAINT Reply_Laptop_FK FOREIGN KEY (Comment_ID) REFERENCES Comment_Laptop (Comment_ID)
);

CREATE TABLE Post_Memory (
  Post_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Post_title varchar(255)  NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Post_ID),
  CONSTRAINT Post_Memory_FK FOREIGN KEY (Post_ID) REFERENCES All_post (Post_ID)
);

CREATE TABLE Comment_Memory (
  Comment_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Comment_content mediumtext  NOT NULL,
  Post_ID bigint(20) unsigned NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Comment_ID),
  KEY Comment_Memory_FK (Post_ID),
  CONSTRAINT Comment_Memory_FK FOREIGN KEY (Post_ID) REFERENCES Post_Memory (Post_ID)
);

CREATE TABLE Reply_Memory (
  Reply_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Reply_content mediumtext  NOT NULL,
  Comment_ID bigint(20) unsigned DEFAULT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Reply_ID),
  KEY Reply_Memory_FK (Comment_ID),
  CONSTRAINT Reply_Memory_FK FOREIGN KEY (Comment_ID) REFERENCES Comment_Memory (Comment_ID)
);

CREATE TABLE Post_Monitor (
  Post_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Post_title varchar(255)  NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Post_ID),
  CONSTRAINT Post_Monitor_FK FOREIGN KEY (Post_ID) REFERENCES All_post (Post_ID)
);

CREATE TABLE Comment_Monitor (
  Comment_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Comment_content mediumtext  NOT NULL,
  Post_ID bigint(20) unsigned NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Comment_ID),
  KEY Comment_Monitor_FK (Post_ID),
  CONSTRAINT Comment_Monitor_FK FOREIGN KEY (Post_ID) REFERENCES Post_Monitor (Post_ID)
);

CREATE TABLE Reply_Monitor (
  Reply_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Reply_content mediumtext  NOT NULL,
  Comment_ID bigint(20) unsigned DEFAULT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Reply_ID),
  KEY Reply_Monitor_FK (Comment_ID),
  CONSTRAINT Reply_Monitor_FK FOREIGN KEY (Comment_ID) REFERENCES Comment_Monitor (Comment_ID)
);

CREATE TABLE Post_Motherboard (
  Post_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Post_title varchar(255)  NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Post_ID),
  CONSTRAINT Post_Motherboard_FK FOREIGN KEY (Post_ID) REFERENCES All_post (Post_ID)
);

CREATE TABLE Comment_Motherboard (
  Comment_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Comment_content mediumtext  NOT NULL,
  Post_ID bigint(20) unsigned NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Comment_ID),
  KEY Comment_Motherboard_FK (Post_ID),
  CONSTRAINT Comment_Motherboard_FK FOREIGN KEY (Post_ID) REFERENCES Post_Motherboard (Post_ID)
);

CREATE TABLE Reply_Motherboard (
  Reply_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Reply_content mediumtext  NOT NULL,
  Comment_ID bigint(20) unsigned DEFAULT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Reply_ID),
  KEY Reply_Motherboard_FK (Comment_ID),
  CONSTRAINT Reply_Motherboard_FK FOREIGN KEY (Comment_ID) REFERENCES Comment_Motherboard (Comment_ID)
);

CREATE TABLE Post_PCCases (
  Post_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Post_title varchar(255)  NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Post_ID),
  CONSTRAINT Post_PCCases_FK FOREIGN KEY (Post_ID) REFERENCES All_post (Post_ID)
);

CREATE TABLE Comment_PCCases (
  Comment_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Comment_content mediumtext  NOT NULL,
  Post_ID bigint(20) unsigned NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Comment_ID),
  KEY Comment_PCCases_FK (Post_ID),
  CONSTRAINT Comment_PCCases_FK FOREIGN KEY (Post_ID) REFERENCES Post_PCCases (Post_ID)
);

CREATE TABLE Reply_PCCases (
  Reply_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Reply_content mediumtext  NOT NULL,
  Comment_ID bigint(20) unsigned DEFAULT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Reply_ID),
  KEY Reply_PCCases_FK (Comment_ID),
  CONSTRAINT Reply_PCCases_FK FOREIGN KEY (Comment_ID) REFERENCES Comment_PCCases (Comment_ID)
);

CREATE TABLE Post_PSU (
  Post_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Post_title varchar(255)  NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Post_ID),
  CONSTRAINT Post_PSU_FK FOREIGN KEY (Post_ID) REFERENCES All_post (Post_ID)
);

CREATE TABLE Comment_PSU (
  Comment_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Comment_content mediumtext  NOT NULL,
  Post_ID bigint(20) unsigned NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Comment_ID),
  KEY Comment_PSU_FK (Post_ID),
  CONSTRAINT Comment_PSU_FK FOREIGN KEY (Post_ID) REFERENCES Post_PSU (Post_ID)
);

CREATE TABLE Reply_PSU (
  Reply_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Reply_content mediumtext  NOT NULL,
  Comment_ID bigint(20) unsigned DEFAULT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Reply_ID),
  KEY Reply_PSU_FK (Comment_ID),
  CONSTRAINT Reply_PSU_FK FOREIGN KEY (Comment_ID) REFERENCES Comment_PSU (Comment_ID)
);

CREATE TABLE Post_Prebuild (
  Post_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Post_title varchar(255)  NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Post_ID),
  CONSTRAINT Post_Prebuild_FK FOREIGN KEY (Post_ID) REFERENCES All_post (Post_ID)
);

CREATE TABLE Comment_Prebuild (
  Comment_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Comment_content mediumtext  NOT NULL,
  Post_ID bigint(20) unsigned NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Comment_ID),
  KEY Comment_Prebuild_FK (Post_ID),
  CONSTRAINT Comment_Prebuild_FK FOREIGN KEY (Post_ID) REFERENCES Post_Prebuild (Post_ID)
);

CREATE TABLE Reply_Prebuild (
  Reply_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Reply_content mediumtext  NOT NULL,
  Comment_ID bigint(20) unsigned DEFAULT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Reply_ID),
  KEY Reply_Prebuild_FK (Comment_ID),
  CONSTRAINT Reply_Prebuild_FK FOREIGN KEY (Comment_ID) REFERENCES Comment_Prebuild (Comment_ID)
);

CREATE TABLE Post_Software (
  Post_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Post_title varchar(255)  NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Post_ID),
  CONSTRAINT Post_Software_FK FOREIGN KEY (Post_ID) REFERENCES All_post (Post_ID)
);

CREATE TABLE Comment_Software (
  Comment_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Comment_content mediumtext  NOT NULL,
  Post_ID bigint(20) unsigned NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Comment_ID),
  KEY Comment_Software_FK (Post_ID),
  CONSTRAINT Comment_Software_FK FOREIGN KEY (Post_ID) REFERENCES Post_Software (Post_ID)
);

CREATE TABLE Reply_Software (
  Reply_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Reply_content mediumtext  NOT NULL,
  Comment_ID bigint(20) unsigned DEFAULT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Reply_ID),
  KEY Reply_Software_FK (Comment_ID),
  CONSTRAINT Reply_Software_FK FOREIGN KEY (Comment_ID) REFERENCES Comment_Software (Comment_ID)
);

CREATE TABLE Post_Storage (
  Post_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Post_title varchar(255)  NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Post_ID),
  CONSTRAINT Post_Storage_FK FOREIGN KEY (Post_ID) REFERENCES All_post (Post_ID)
);

CREATE TABLE Comment_Storage (
  Comment_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Comment_content mediumtext  NOT NULL,
  Post_ID bigint(20) unsigned NOT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Comment_ID),
  KEY Comment_Storage_FK (Post_ID),
  CONSTRAINT Comment_Storage_FK FOREIGN KEY (Post_ID) REFERENCES Post_Storage (Post_ID)
);

CREATE TABLE Reply_Storage (
  Reply_ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  Reply_content mediumtext  NOT NULL,
  Comment_ID bigint(20) unsigned DEFAULT NULL,
  PostDate datetime NOT NULL DEFAULT current_timestamp(),
  Author varchar(100)  DEFAULT NULL,
  PRIMARY KEY (Reply_ID),
  KEY Reply_Storage_FK (Comment_ID),
  CONSTRAINT Reply_Storage_FK FOREIGN KEY (Comment_ID) REFERENCES Comment_Storage (Comment_ID)
);

CREATE TABLE Taboo (
  Word varchar(100) NOT NULL,
  PRIMARY KEY (`Word`)
);

INSERT INTO Taboo(Word)
VALUES('test'),
	  ('badword'),
	  ('badword2'),
      ('test3'),
      ('test4'),
      ('badword'),
	  ('TestBadWord'),
	  ('Snortz')	