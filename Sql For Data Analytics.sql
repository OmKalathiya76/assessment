create database try;
use try;

CREATE TABLE employees ( 
  employee_id INT AUTO_INCREMENT PRIMARY KEY, 
  name VARCHAR(100), 
  position VARCHAR(100), 
  salary DECIMAL(10,2), 
  hire_date DATE
);
 INSERT INTO employees (name, position, salary, hire_date) VALUES ('John Doe',
'Software Engineer', 80000.00, '2022-01-15'),
('Jane Smith', 'Project Manager', 90000.00, '2021-05-22'),
('Alice Johnson', 'UX Designer', 75000.00, '2023-03-01');
 
 select * from employees;
 select * from employee_audit;
 
 
CREATE TABLE employee_audit ( 
  audit_id INT AUTO_INCREMENT PRIMARY KEY, 
  employee_id INT,
  name VARCHAR(100), 
  position VARCHAR(100),
  salary DECIMAL(10,2),
  hire_date DATE,
  action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$

CREATE TRIGGER trg_employee_insert
AFTER INSERT ON employees
FOR EACH ROW
BEGIN
    INSERT INTO employee_audit (employee_id, name, position, salary, hire_date)
    VALUES (NEW.employee_id, NEW.name, NEW.position, NEW.salary, NEW.hire_date);
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE add_employee (
    IN p_name VARCHAR(100),
    IN p_position VARCHAR(100),
    IN p_salary DECIMAL(10,2),
    IN p_hire_date DATE
)
BEGIN
    INSERT INTO employees (name, position, salary, hire_date)
    VALUES (p_name, p_position, p_salary, p_hire_date);
END$$

DELIMITER ;

CALL add_employee(
    'Michael Brown',
    'Data Analyst',
    68000.00,
    '2024-06-15'
);


