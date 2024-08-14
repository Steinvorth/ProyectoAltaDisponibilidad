const express = require('express');
const router = express.Router();
const mysql = require('mysql2');
const fs = require('fs');
const path = require('path');

// Coneccion a la db principal
const dbPrimary = mysql.createPool({
    host: 'mysql-main',
    user: 'root',
    password: '123456789',
    database: 'AltaDisponibilidadDB_Main',
    port: 3306
});

// Coneccion a la db secundaria
const dbSecondary = mysql.createPool({
    host: 'mysql-respaldo',
    user: 'root',
    password: '123456789',
    database: 'AltaDisponibilidadDB_Respaldo',
    port: 3306
});

// Este JSON servira para poder subir los datos de la DB secundaria a la principal cuando vuelva a estar en linea
const logFilePath = path.join(__dirname, 'HA', 'db_changes.json');

// Función para agregar un registro al archivo JSON con los datos de cada query mientras la base de datos principal está caída
function logQuery(query, params) {
    // Crea un objeto que contiene la consulta (query) y sus parámetros (params)
    const logEntry = { query, params };
    
    // Lee el contenido del archivo JSON donde se guardan los logs
    fs.readFile(logFilePath, (err, data) => {
        // Inicializa un array vacío para almacenar los logs
        let logs = [];
        
        // Si no hay error al leer el archivo y este no está vacío, parsea los datos del archivo JSON y guárdalos en el array logs
        if (!err && data.length > 0) {
            logs = JSON.parse(data);
        }
        
        // Agrega el nuevo registro (logEntry) al array de logs
        logs.push(logEntry);
        
        // Escribe el array actualizado de logs en el archivo JSON, sobrescribiendo su contenido (por que esta vacio)
        fs.writeFile(logFilePath, JSON.stringify(logs, null, 2), (err) => {
            // Si ocurre un error al guardar el archivo, se muestra en la consola
            if (err) console.error('Error al guardar el query:', err);
        });
    });
}


// Función para ingresar los datos almacenados en el archivo JSON a la base de datos principal
function replayChanges() {
    // Lee el contenido del archivo JSON que contiene los logs de las consultas fallidas
    fs.readFile(logFilePath, (err, data) => {
        // Si ocurre un error al leer el archivo o el archivo está vacío, la función termina sin hacer nada
        if (err || data.length === 0) return;

        // Si la lectura fue exitosa, parsea los datos del archivo JSON y los guarda en la variable logs
        const logs = JSON.parse(data);
        
        // Recorre cada log en el array logs
        logs.forEach((log) => {
            // Intenta ejecutar la consulta en la base de datos principal
            dbPrimary.query(log.query, log.params, (err) => {
                // Si ocurre un error al intentar ejecutar la consulta, se muestra en la consola
                if (err) {
                    console.error('Could not apply changes from JSON to the primary DB:', err);
                    return;
                } else {
                    // Si la consulta se ejecuta exitosamente, se muestra un mensaje en la consola
                    console.log('Changes successfully applied to the primary database');

                    // Limpia el contenido del archivo JSON una vez que todos los cambios han sido aplicados
                    fs.writeFile(logFilePath, '[]', (err) => {
                        // Si ocurre un error al limpiar el archivo JSON, se muestra en la consola
                        if (err) console.error('Error clearing the JSON file:', err);
                    });
                }
            });
        });
    });
}

// Función para ejecutar una consulta en la base de datos principal y, si falla, intentar en la base de datos secundaria (Se usa para los SELECT)
function executeQuery(query, params, callback) {
    // Ejecuta la consulta en la base de datos principal
    dbPrimary.query(query, params, (err, results) => {
        // Si ocurre un error en la base de datos principal, se registra en la consola
        if (err) {
            console.error('Error en la DB Principal!');
            console.log('Usando la segunda DB...');

            // Intenta ejecutar la misma consulta en la base de datos secundaria
            dbSecondary.query(query, params, (err, results) => {
                // Si también ocurre un error en la base de datos secundaria, se registra en la consola y se llama al callback con el error
                if (err) {
                    console.error('Error con DB Secundaria:', err.message);
                    return callback(err, null);
                } else {
                    // Si la consulta en la base de datos secundaria es exitosa, se llama al callback con los resultados
                    return callback(null, results);
                }
            });
        } else {
            // Si la consulta en la base de datos principal es exitosa, se llama al callback con los resultados
            return callback(null, results);
        }
    });
}

// Función para ejecutar consultas INSERT, UPDATE y DELETE en ambas bases de datos
function executeDualWrite(query, params, callback) {
    // Ejecuta la consulta en la base de datos principal
    dbPrimary.query(query, params, (err, results) => {
        // Si ocurre un error en la base de datos principal, se maneja aquí
        if (err) {
            console.error('Error en DB principal:');
            logQuery(query, params);  // Agrega la consulta al archivo JSON si la base de datos principal está caída

            // Intenta ejecutar la misma consulta en la base de datos secundaria
            dbSecondary.query(query, params, (err, results) => {
                // Si ocurre un error en la base de datos secundaria, se pasa el error al callback
                if (err) {
                    return callback(err, null);
                }
                // Si la consulta en la base de datos secundaria es exitosa, se pasa el resultado al callback
                return callback(null, results);
            });
        } else {
            // Si la consulta en la base de datos principal es exitosa, se replica en la base de datos secundaria
            dbSecondary.query(query, params, (err) => {
                // Si ocurre un error al replicar en la base de datos secundaria, se registra en la consola
                if (err) {
                    console.error('Error replicando datos en la DB Secundaria:', err.message);
                }
            });
            // Se pasa el resultado de la consulta exitosa al callback
            return callback(null, results);
        }
    });
}

// Trigger para replicar los cambios
router.post('/replay-changes', (req, res) => {
    replayChanges();
    res.status(200).send('Replayed changes to the primary database');
});

// Ruta para conseguir todos los carros
router.get('/carros', (req, res) => {
    const query = `
        SELECT Carros.ID, Carros.Marca, Carros.Modelo, Carros.Placa, 
               IFNULL(Disponibilidad.Estado, 'Not Available') AS Estado, 
               Carros.DetalleEstado, Carros.ImagenURL 
        FROM Carros 
        LEFT JOIN Disponibilidad ON Carros.id_disponibilidad = Disponibilidad.LogID
    `;
    executeQuery(query, [], (err, results) => {
        if (err) {
            return res.status(500).send('Error');
        }
        res.json(results);
    });
});

// Ruta para conseguir un carro especifico
router.get('/carros/:id', (req, res) => {
    const query = `
        SELECT Carros.*, IFNULL(Disponibilidad.Estado, 'Not Available') AS Estado 
        FROM Carros 
        LEFT JOIN Disponibilidad ON Carros.id_disponibilidad = Disponibilidad.LogID
        WHERE Carros.ID = ?
    `;
    const carId = req.params.id;
    executeQuery(query, [carId], (err, results) => {
        if (err) {
            return res.status(500).send('Error');
        }
        res.json(results[0]);
    });
});

// Ruta para crear un usuario
router.post('/usuarios', (req, res) => {
    const { Username, Password, Email, Nombre, Apellido } = req.body;
    const query = 'INSERT INTO Usuarios (Username, Password, Email, Nombre, Apellido) VALUES (?, ?, ?, ?, ?)';
    executeDualWrite(query, [Username, Password, Email, Nombre, Apellido], (err, results) => {
        if (err) {
            return res.status(500).send('Error');
        }
        res.status(201).send('Usuario creado con éxito');
    });
});

// Rita para autenticar usuario en login
router.post('/login', (req, res) => {
    const { Username, Password } = req.body;
    const query = 'SELECT * FROM Usuarios WHERE Username = ? AND Password = ?';

    executeQuery(query, [Username, Password], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error' });
        }

        if (results.length > 0) {
            return res.json({ message: 'Login Exitoso', userId: results[0].ID }); //return el ID para luego poder usarlo para el local session storage
        } else {
            return res.status(401).json({ message: 'Credenciales Invalidas' });
        }
    });
});

// Tura para conseguir las rentas de un usuario especifico
router.get('/rentals/:userId', (req, res) => {
    const userId = req.params.userId;
    const query = `
        SELECT Rentas.*, Carros.Marca, Carros.Modelo
        FROM Rentas
        JOIN Carros ON Rentas.id_carro = Carros.ID
        WHERE Rentas.id_usuario = ?
    `;
    executeQuery(query, [userId], (err, results) => {
        if (err) {
            return res.status(500).send('Error');
        }
        res.json(results);
    });
});

// Ruta para conseguir los datos de un usuario
router.get('/users/:id', (req, res) => {
    const userId = req.params.id;
    const query = 'SELECT ID, Username, Email, Nombre, Apellido FROM Usuarios WHERE ID = ?';
    executeQuery(query, [userId], (err, results) => {
        if (err) {
            return res.status(500).send('Error');
        }
        res.json(results[0]);
    });
});

// Ruta para insertar una renta nueva
router.post('/rentals', (req, res) => {
    const { id_usuario, id_carro, ComienzoRenta, FinalRenta, CostoTotal } = req.body;
    const query = 'INSERT INTO Rentas (id_usuario, id_carro, ComienzoRenta, FinalRenta, CostoTotal) VALUES (?, ?, ?, ?, ?)';
    executeDualWrite(query, [id_usuario, id_carro, ComienzoRenta, FinalRenta, CostoTotal], (err, results) => {
        if (err) {
            return res.status(500).send('Error');
        }
        res.status(201).send('Renta Exitosa');
    });
});

// Ruta para conseguir todos los usuarios (Admin)
router.get('/admin/users', (req, res) => {
    const query = 'SELECT ID, Username, Email, Nombre, Apellido FROM Usuarios';
    executeQuery(query, [], (err, results) => {
        if (err) {
            return res.status(500).json({ error: 'Error' });
        }
        res.json(results);
    });
});

// Rua pra conseguir todos los carros (Admin)
router.get('/admin/cars', (req, res) => {
    const query = `
        SELECT Carros.ID, Carros.Marca, Carros.Modelo, Carros.Placa, 
               IFNULL(Disponibilidad.Estado, 'Not Available') AS Estado, 
               Carros.DetalleEstado, Carros.ImagenURL 
        FROM Carros 
        LEFT JOIN Disponibilidad ON Carros.id_disponibilidad = Disponibilidad.LogID
    `;
    executeQuery(query, [], (err, results) => {
        if (err) {
            return res.status(500).json({ error: 'Error' });
        }
        res.json(results);
    });
});

// Route para conseguir todas las rentas (Admin)
router.get('/admin/rentals', (req, res) => {
    const query = `
        SELECT Rentas.*, Carros.Marca, Carros.Modelo, Usuarios.Username 
        FROM Rentas 
        JOIN Carros ON Rentas.id_carro = Carros.ID 
        JOIN Usuarios ON Rentas.id_usuario = Usuarios.ID
    `;
    executeQuery(query, [], (err, results) => {
        if (err) {
            return res.status(500).json({ error: 'Error' });
        }
        res.json(results);
    });
});

// Conseguir un usuario basado en su ID
router.get('/usuarios/:id', (req, res) => {
    const userId = req.params.id;
    const query = 'SELECT ID, Username, Email, Nombre, Apellido FROM Usuarios WHERE ID = ?';
    executeQuery(query, [userId], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error' });
        }
        res.json(results[0]);
    });
});

// Actualizar usuario por ID
router.put('/usuarios/:id', (req, res) => {
    const userId = req.params.id;
    const { Username, Email, Nombre, Apellido } = req.body;
    const query = 'UPDATE Usuarios SET Username = ?, Email = ?, Nombre = ?, Apellido = ? WHERE ID = ?';
    executeDualWrite(query, [Username, Email, Nombre, Apellido, userId], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error' });
        }
        res.json({ message: 'Actualizado Exitosamente' });
    });
});

// Borrar Usuario Especifico
router.delete('/usuarios/:id', (req, res) => {
    const userId = req.params.id;
    const query = 'DELETE FROM Usuarios WHERE ID = ?';
    executeDualWrite(query, [userId], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error' });
        }
        res.json({ message: 'Usuario Eliminado Exitosamente.' });
    });
});

// Buscar un carro por ID
router.get('/carros/:id', (req, res) => {
    const carId = req.params.id;
    const query = `
        SELECT Carros.*, IFNULL(Disponibilidad.Estado, 'Not Available') AS Estado 
        FROM Carros 
        LEFT JOIN Disponibilidad ON Carros.id_disponibilidad = Disponibilidad.LogID
        WHERE Carros.ID = ?
    `;
    executeQuery(query, [carId], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error' });
        }
        res.json(results[0]);
    });
});

// Actualizar Carro Especifico
router.put('/carros/:id', (req, res) => {
    const carId = req.params.id;
    const { Marca, Modelo, Placa, id_disponibilidad, DetalleEstado, ImagenURL } = req.body;
    const query = 'UPDATE Carros SET Marca = ?, Modelo = ?, Placa = ?, id_disponibilidad = ?, DetalleEstado = ?, ImagenURL = ? WHERE ID = ?';
    executeDualWrite(query, [Marca, Modelo, Placa, id_disponibilidad, DetalleEstado, ImagenURL, carId], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error' });
        }
        res.json({ message: 'Car Actualizado Exitosamente' });
    });
});

// Borrar un Carro
router.delete('/carros/:id', (req, res) => {
    const carId = req.params.id;
    const query = 'DELETE FROM Carros WHERE ID = ?';
    executeDualWrite(query, [carId], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error' });
        }
        res.json({ message: 'Carro Eliminado Exitosamente' });
    });
});

// Conseguir una renta especifica
router.get('/rentals/:id', (req, res) => {
    const rentalId = req.params.id;
    const query = `
        SELECT Rentas.*, Usuarios.Username, Carros.Marca, Carros.Modelo 
        FROM Rentas 
        JOIN Usuarios ON Rentas.id_usuario = Usuarios.ID 
        JOIN Carros ON Rentas.id_carro = Carros.ID 
        WHERE Rentas.ID = ?
    `;
    executeQuery(query, [rentalId], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error' });
        }
        res.json(results[0]);
    });
});

// Actualiar renta especifica
router.put('/rentals/:id', (req, res) => {
    const rentalId = req.params.id;
    const { id_usuario, id_carro, ComienzoRenta, FinalRenta, CostoTotal } = req.body;
    const query = `
        UPDATE Rentas 
        SET id_usuario = ?, id_carro = ?, ComienzoRenta = ?, FinalRenta = ?, CostoTotal = ? 
        WHERE ID = ?
    `;
    executeDualWrite(query, [id_usuario, id_carro, ComienzoRenta, FinalRenta, CostoTotal, rentalId], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error' });
        }
        res.json({ message: 'Renta Actualizada Exitosamente' });
    });
});

// Borrar renta 
router.delete('/rentals/:id', (req, res) => {
    const rentalId = req.params.id;
    const query = 'DELETE FROM Rentas WHERE ID = ?';
    executeDualWrite(query, [rentalId], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error' });
        }
        res.json({ message: 'Renta Elminadad Exitosamente' });
    });
});

// Agregar Usuario nuevo desde Admin
router.post('/admin/users', (req, res) => {
    const { Username, Password, Email, Nombre, Apellido } = req.body;
    const query = 'INSERT INTO Usuarios (Username, Password, Email, Nombre, Apellido) VALUES (?, ?, ?, ?, ?)';
    executeDualWrite(query, [Username, Password, Email, Nombre, Apellido], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error' });
        }
        res.status(201).json({ message: 'Usuario Agregado Exitosamente!' });
    });
});

// Agregar Vehiculo nuevo desde Admin
router.post('/admin/cars', (req, res) => {
    const { Marca, Modelo, Placa, id_disponibilidad, ImagenURL, DetalleEstado } = req.body;
    const query = 'INSERT INTO Carros (Marca, Modelo, Placa, id_disponibilidad, ImagenURL, DetalleEstado) VALUES (?, ?, ?, ?, ?, ?)';
    executeDualWrite(query, [Marca, Modelo, Placa, id_disponibilidad, ImagenURL, DetalleEstado], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error' });
        }
        res.status(201).json({ message: 'Carro Agregado Exitosamente!' });
    });
});

// Ruta para conseguir los estados de los vehiculos
router.get('/availability', (req, res) => {
    const query = 'SELECT * FROM Disponibilidad';
    executeQuery(query, [], (err, results) => {
        if (err) {
            return res.status(500).json({ error: 'Error' });
        }
        res.json(results);
    });
});

module.exports = router;
