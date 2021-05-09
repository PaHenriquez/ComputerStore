DROP DATABASE IF EXISTS SpoiledEgg;
CREATE DATABASE SpoiledEgg;
USE SpoiledEgg;

------------------------------------------------ USER TABLES -----------------------------------------------
CREATE TABLE Spoiled_Users(
	ID BIGINT(255) PRIMARY KEY,
	Username VARCHAR(255) NOT NULL UNIQUE,
	Email VARCHAR(512) NOT NULL UNIQUE,
	Password VARCHAR(255) NOT NULL,
	Phone_Number VARCHAR(13),
	User_Type VARCHAR(255) NOT NULL
);
------------------- CUSTOMER TABLES -------------------------
CREATE TABLE Spoiled_Customer(
	ID BIGINT(255) PRIMARY KEY,
	Address VARCHAR(255),
	Store_Credit INTEGER NOT NULL,
	FOREIGN KEY(ID) REFERENCES Spoiled_Users(ID)
);

CREATE TABLE Spoiled_Payment(
	ID BIGINT(255) PRIMARY KEY,
	Payment_Card VARCHAR(16),
	Name_On_Card VARCHAR(255),
	Billing_Address VARCHAR (512),
	FOREIGN KEY(ID) REFERENCES Spoiled_Customer(ID)
);
-------------------------------------------------------------

CREATE TABLE Spoiled_Employee(
	ID BIGINT(255) PRIMARY KEY,
	Employee_Type VARCHAR(255) NOT NULL,
	FOREIGN KEY(ID) REFERENCES Spoiled_Users(ID)
);

------------------------------------------ BUSINESS TABLES -------------------------------------------------
CREATE TABLE Spoiled_Business_Partner(
	ID BIGINT(255) PRIMARY KEY,
	Company_Name VARCHAR(255) NOT NULL UNIQUE,
	Partner_Type VARCHAR(255) NOT NULL,
	FOREIGN KEY(ID) REFERENCES Spoiled_Users(ID)
);

-------------------------------------------------------------------------------------------------------------

------------------------------------------------- Inventory Tables ------------------------------------------
 CREATE TABLE Spoiled_Item(
	Item_ID INTEGER PRIMARY KEY,
	Type_of_Part VARCHAR(255),
	Shipper_ID BIGINT(255),
	Desciption VARCHAR(512),
	Quantity INTEGER,
	Price REAL,
	Rating REAL,
	FOREIGN KEY(Shipper_ID) REFERENCES Spoiled_Business_Partner(ID)
 ); 
 
 CREATE TABLE Spoiled_Monitor(
	Item_ID INTEGER PRIMARY KEY,
	Name VARCHAR(255) NOT NULL,
	Dimensions INTEGER,
	Refresh_Rate INTEGER,
	Resolution VARCHAR(255),
	FOREIGN KEY(Item_ID) REFERENCES Spoiled_Item(Item_ID)
 );
 
 CREATE TABLE Spoiled_GPU(
	Item_ID INTEGER PRIMARY KEY,
	Name VARCHAR(255) NOT NULL,
	Architecture VARCHAR(255),
	FOREIGN KEY(Item_ID) REFERENCES Spoiled_Item(Item_ID)
 );
 
 CREATE TABLE Spoiled_CPU(
	Item_ID INTEGER PRIMARY KEY,
	Name VARCHAR(255) NOT NULL,
	Architecture VARCHAR(255),
	FOREIGN KEY(Item_ID) REFERENCES Spoiled_Item(Item_ID)
 );
 
 CREATE TABLE Spoiled_PC_Cases(
	Item_ID INTEGER PRIMARY KEY,
	Name VARCHAR(255) NOT NULL,
	Material VARCHAR(255),
	FOREIGN KEY(Item_ID) REFERENCES Spoiled_Item(Item_ID)
 );
 
 CREATE TABLE Spoiled_Motherboard(
	Item_ID INTEGER PRIMARY KEY,
	Name VARCHAR(255) NOT NULL,
	Architecture_Compatibility VARCHAR(255),
	FOREIGN KEY(Item_ID) REFERENCES Spoiled_Item(Item_ID)
 );
 
 CREATE TABLE Spoiled_PSU(
	Item_ID INTEGER PRIMARY KEY,
	Name VARCHAR(255) NOT NULL,
	Wattage INTEGER,
	FOREIGN KEY(Item_ID) REFERENCES Spoiled_Item(Item_ID)
 );
 
 CREATE TABLE Spoiled_Memory(
	Item_ID INTEGER PRIMARY KEY,
	Name VARCHAR(255) NOT NULL,
	Total_Memory INTEGER, 
	Speed INTEGER,
	FOREIGN KEY(Item_ID) REFERENCES Spoiled_Item(Item_ID)
 );
 
 CREATE TABLE Spoiled_Storage(
	Item_ID INTEGER PRIMARY KEY,
	Name VARCHAR(255) NOT NULL,
	Total_Memory INTEGER,
	Type_Of_Storage VARCHAR(255),
	FOREIGN KEY(Item_ID) REFERENCES Spoiled_Item(Item_ID)
 );
 
 CREATE TABLE Spoiled_Laptops_and_PreBuilds(
	Item_ID INTEGER PRIMARY KEY,
	Name VARCHAR(255) NOT NULL UNIQUE,
	Memory VARCHAR(255),
	Storage VARCHAR(255),
	GPU VARCHAR(255),
	CPU VARCHAR(255),
	PSU VARCHAR(255),
	Motherboard VARCHAR(255),
	PC_Case VARCHAR(255),
	Laptop_or_Prebuild INTEGER, -- 1 laptop, 2 prebuild 
	FOREIGN KEY(Item_ID) REFERENCES Spoiled_Item(Item_ID)
 );
 
 CREATE TABLE Spoiled_Software(
	Item_ID INTEGER PRIMARY KEY,
	Name VARCHAR(255) NOT NULL,
	OS_choice VARCHAR(255),
	FOREIGN KEY(Item_ID) REFERENCES Spoiled_Item(Item_ID)
 ); 
 
 
 --------------------------- Bidding System --------------------------------------
 CREATE TABLE Spoiled_Bids(
	Bid_ID INTEGER PRIMARY KEY,
	Item_ID INTEGER NOT NULL,
	Company_Name VARCHAR(255) NOT NULL,
	Bid INTEGER,
	Time_of_bid DATE,
	FOREIGN KEY(Item_ID) REFERENCES Spoiled_Item(Item_ID),
	FOREIGN KEY(Company_Name) REFERENCES Spoiled_Business_Partner(Company_Name)
);

---------------------------- Customer_Carts -----------------------------------
CREATE TABLE Spoiled_Cart(
	ID BIGINT(255) NOT NULL,
	Item_ID INTEGER NOT NULL,
	Occurence INTEGER NOT NULL,
	PRIMARY KEY(ID,Item_ID,Occurence),
	FOREIGN KEY(ID) REFERENCES Spoiled_Customer(ID),
	FOREIGN KEY(Item_ID) REFERENCES Spoiled_Item(Item_ID)
);

CREATE TABLE Spoiled_Purchase_History(
	ID BIGINT(255) NOT NULL,
	Item_ID INTEGER NOT NULL,
	Occurence INTEGER NOT NULL,
	Time_of_Purchase DATE NOT NULL,
	PRIMARY KEY(ID,Item_ID,Occurence,Time_of_Purchase),
	FOREIGN KEY(ID) REFERENCES Spoiled_Customer(ID),
	FOREIGN KEY(Item_ID) REFERENCES Spoiled_Item(Item_ID)
);
