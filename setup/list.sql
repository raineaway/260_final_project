CREATE DATABASE IF NOT EXISTS list;
GRANT ALL ON list.* TO 'list-admin'@'%' IDENTIFIED BY 'l1st@dm1n';
GRANT ALL ON list.* TO 'list-admin'@'localhost' IDENTIFIED BY 'l1st@dm1n';
GRANT ALL ON test_list.* TO 'list-admin'@'%' IDENTIFIED BY 'l1st@dm1n';
GRANT ALL ON test_list.* TO 'list-admin'@'localhost' IDENTIFIED BY 'l1st@dm1n';

