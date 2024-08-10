docker run --name mysql-respaldo -e MYSQL_ROOT_PASSWORD=123456789 -p 3307:3306 -d mysql:latest

docker run --name mysql-main -e MYSQL_ROOT_PASSWORD=123456789 -p 3306:3306 -d mysql:latest

