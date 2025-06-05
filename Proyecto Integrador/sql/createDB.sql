create database proyecto_integrador;
use proyecto_integrador;
CREATE TABLE categories (
  CategoryID    INT            NOT NULL AUTO_INCREMENT,
  CategoryName  VARCHAR(45)    NOT NULL,
  PRIMARY KEY (CategoryID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE countries (
  CountryID     INT            NOT NULL AUTO_INCREMENT,
  CountryName   VARCHAR(45)    NOT NULL,
  CountryCode   VARCHAR(2)     NOT NULL,
  PRIMARY KEY (CountryID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE cities (
  CityID        INT            NOT NULL AUTO_INCREMENT,
  CityName      VARCHAR(45)    NOT NULL,
  Zipcode       DECIMAL(5,0),
  CountryID     INT            NOT NULL,
  PRIMARY KEY (CityID),
  INDEX idx_cities_country (CountryID),
  CONSTRAINT fk_cities_countries 
    FOREIGN KEY (CountryID) 
    REFERENCES countries (CountryID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4) Tabla de productos
CREATE TABLE products (
  ProductID     INT            NOT NULL AUTO_INCREMENT,
  ProductName   VARCHAR(45)    NOT NULL,
  Price         DECIMAL(10,0)  NOT NULL,
  CategoryID    INT            NOT NULL,
  Class         VARCHAR(45),
  ModifyDate    DATE,
  Resistant     VARCHAR(45),
  IsAllergic    VARCHAR(10),
  VitalityDays  DECIMAL(3,0),
  PRIMARY KEY (ProductID),
  INDEX idx_products_category (CategoryID),
  CONSTRAINT fk_products_categories 
    FOREIGN KEY (CategoryID) 
    REFERENCES categories (CategoryID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5) Tabla de clientes
CREATE TABLE customers (
  CustomerID      INT            NOT NULL AUTO_INCREMENT,
  FirstName       VARCHAR(45)    NOT NULL,
  MiddleInitial   VARCHAR(1),
  LastName        VARCHAR(45)    NOT NULL,
  CityID          INT            NOT NULL,
  Address         VARCHAR(90),
  PRIMARY KEY (CustomerID),
  INDEX idx_customers_city (CityID),
  CONSTRAINT fk_customers_cities 
    FOREIGN KEY (CityID) 
    REFERENCES cities (CityID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6) Tabla de empleados
CREATE TABLE employees (
  EmployeeID      INT            NOT NULL AUTO_INCREMENT,
  FirstName       VARCHAR(45)    NOT NULL,
  MiddleInitial   VARCHAR(1),
  LastName        VARCHAR(45)    NOT NULL,
  BirthDate       DATE,
  Gender          VARCHAR(1),
  CityID          INT            NOT NULL,
  HireDate        DATE,
  PRIMARY KEY (EmployeeID),
  INDEX idx_employees_city (CityID),
  CONSTRAINT fk_employees_cities 
    FOREIGN KEY (CityID) 
    REFERENCES cities (CityID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7) Tabla de ventas (hechos)
CREATE TABLE sales (
  SalesID            INT             NOT NULL AUTO_INCREMENT,
  SalesPersonID      INT             NOT NULL,
  CustomerID         INT             NOT NULL,
  ProductID          INT             NOT NULL,
  Quantity           INT,
  Discount           DECIMAL(10,2),
  TotalPrice         DECIMAL(10,2),
  SaleDate           DATETIME,
  TransactionNumber  VARCHAR(255),
  PRIMARY KEY (SalesID),
  INDEX idx_sales_salesperson  (SalesPersonID),
  INDEX idx_sales_customer     (CustomerID),
  INDEX idx_sales_product      (ProductID),
  CONSTRAINT fk_sales_employees 
    FOREIGN KEY (SalesPersonID) 
    REFERENCES employees (EmployeeID),
  CONSTRAINT fk_sales_customers 
    FOREIGN KEY (CustomerID) 
    REFERENCES customers (CustomerID),
  CONSTRAINT fk_sales_products 
    FOREIGN KEY (ProductID) 
    REFERENCES products (ProductID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;