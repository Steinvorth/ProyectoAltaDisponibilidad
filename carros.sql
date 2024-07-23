-- Eliminar la base de datos existente si existe
DROP DATABASE IF EXISTS Carros;

-- Crear base de datos
CREATE DATABASE Carros;
USE Carros;

CREATE TABLE Usuarios (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(15) NOT NULL,
    Password VARCHAR(25) NOT NULL,
    Email VARCHAR(50) NOT NULL UNIQUE,
    Nombre VARCHAR(20),
    Apellido VARCHAR(20),
    CreadoEn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ActualizadoEn TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Carros (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Marca VARCHAR(50) NOT NULL,
    Modelo VARCHAR(50) NOT NULL,
    Placa VARCHAR(20) NOT NULL UNIQUE,
    Estado VARCHAR(20) DEFAULT 'disponible',
    DetalleEstado TEXT,
    IngresadoEn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ActualizadoEn TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Rentas (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_carro INT NOT NULL,
    ComienzoRenta TIMESTAMP NOT NULL,
    FinalRenta TIMESTAMP,
    CostoTotal DECIMAL(10, 2),
    CreadoEn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ActualizadoEn TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(ID),
    FOREIGN KEY (id_carro) REFERENCES Carros(ID)
);

CREATE TABLE Disponibilidad (
    LogID INT PRIMARY KEY AUTO_INCREMENT,
    id_carro INT NOT NULL,
    Estado VARCHAR(20) NOT NULL,
    HoraLog TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_carro) REFERENCES Carros(ID)
);

CREATE TABLE ServicioCliente (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_carro INT,
    TipoIncidencia VARCHAR(20) NOT NULL,
    Descripcion TEXT NOT NULL,
    CreadoEn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ActualizadoEn TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    Resuelto BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(ID),
    FOREIGN KEY (id_carro) REFERENCES Carros(ID)
);
USE Carros;

-- Agregar 10 carros a la tabla Carros
INSERT INTO Carros (Marca, Modelo, Placa, Estado, DetalleEstado) VALUES
('Toyota', 'Corolla', 'ABC123', 'disponible', 'En buen estado general.'),
('Honda', 'Civic', 'DEF456', 'disponible', 'Cambio de aceite reciente.'),
('Ford', 'Mustang', 'GHI789', 'disponible', 'Neumáticos nuevos.'),
('Chevrolet', 'Cruze', 'JKL012', 'disponible', 'Sin daños.'),
('Hyundai', 'Elantra', 'MNO345', 'disponible', 'Revisión técnica pasada.'),
('Mazda', '3', 'PQR678', 'disponible', 'Interior en excelentes condiciones.'),
('Nissan', 'Altima', 'STU901', 'disponible', 'Cambio de frenos reciente.'),
('Volkswagen', 'Golf', 'VWX234', 'disponible', 'Sin accidentes.'),
('Kia', 'Optima', 'YZA567', 'disponible', 'Aire acondicionado funcionando.'),
('Subaru', 'Impreza', 'BCD890', 'disponible', 'Revisión de motor reciente.');
