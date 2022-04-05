#Base de datos para la aplicación web Fruver
CREATE DATABASE IF NOT EXISTS fruverdb;

#Seleccionar base de datos
USE fruverdb;

#Tabla Comuna, almacena todas las comunas de la provincia de Santiago
CREATE TABLE IF NOT EXISTS comuna(
	PRIMARY KEY(id_comuna),
	id_comuna VARCHAR(30) NOT NULL
)ENGINE=INNODB;

#Tabla Cliente, almacena datos de los clientes de Fruver
CREATE TABLE IF NOT EXISTS cliente(
	PRIMARY KEY(id_cliente),
	id_cliente INT NOT NULL,
    nombre_cliente VARCHAR(20) NOT NULL,
    apellido_cliente VARCHAR(20) NOT NULL,
    email_cliente VARCHAR(30) NOT NULL,
    password_cliente VARCHAR(12) NOT NULL,
    telefono_cliente INT NOT NULL,
    domicilio_cliente VARCHAR(40) NOT NULL,
    comuna VARCHAR(30) NOT NULL,
    CONSTRAINT fkcomuna
    FOREIGN KEY(comuna)
    REFERENCES comuna(id_comuna)
)ENGINE=INNODB;
