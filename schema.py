tables_definitions = {
	"Users": """CREATE TABLE Users (
				id INT AUTO_INCREMENT PRIMARY KEY, 
				name VARCHAR(255), 
				role VARCHAR(30),
				timestamp VARCHAR(30)
			)""",
	"Services": """CREATE TABLE Services (
				id INT AUTO_INCREMENT PRIMARY KEY, 
				name VARCHAR(255), 
				duration VARCHAR(30)
			)""",
	"WorkOrders": """CREATE TABLE WorkOrders (
				id INT AUTO_INCREMENT PRIMARY KEY, 
				startTime VARCHAR(30),
				duration INT,
				ServiceId INT, 
				CustomerId INT,
				EmployeeId INT,
				FOREIGN KEY (ServiceId) REFERENCES Services(id),
				FOREIGN KEY (CustomerId) REFERENCES Users(id),
				FOREIGN KEY (EmployeeId) REFERENCES Users(id)
			)""",
	"Holidays": """CREATE TABLE Holidays (
				id INT AUTO_INCREMENT PRIMARY KEY, 
				holiday VARCHAR(255), 
				date VARCHAR(30)
			)"""
	}


