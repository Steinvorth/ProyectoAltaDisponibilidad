const express = require('express');
const router = express.Router();
const mysql = require('mysql2');
const fs = require('fs');
const path = require('path');

// Create MySQL connection pools for both primary and secondary databases
const dbPrimary = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: '123456789',
    database: 'AltaDisponibilidadDB_Main',
    port: 3306
});

const dbSecondary = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: '123456789',
    database: 'AltaDisponibilidadDB_Respaldo',
    port: 3307
});

// Path to the JSON log file
const logFilePath = path.join(__dirname, 'HA', 'db_changes.json');

// Function to log queries to JSON file
function logQuery(query, params) {
    const logEntry = { query, params };
    fs.readFile(logFilePath, (err, data) => {
        let logs = [];
        if (!err && data.length > 0) {
            logs = JSON.parse(data);
        }
        logs.push(logEntry);
        fs.writeFile(logFilePath, JSON.stringify(logs, null, 2), (err) => {
            if (err) console.error('Failed to log query:', err);
        });
    });
}

// Function to replay logged queries to the primary database
function replayChanges() {
    fs.readFile(logFilePath, (err, data) => {
        if (err || data.length === 0) return;

        const logs = JSON.parse(data);
        logs.forEach((log) => {
            dbPrimary.query(log.query, log.params, (err) => {
                if (err) {
                    console.error('Failed to apply logged query:', err);
                } else {
                    console.log('Successfully replayed query on primary database');
                }
            });
        });

        // Clear the log file after replaying
        fs.writeFile(logFilePath, '[]', (err) => {
            if (err) console.error('Failed to clear log file:', err);
        });
    });
}

// Function to execute a query with failover logic
function executeQuery(query, params, callback) {
    dbPrimary.query(query, params, (err, results) => {
        if (err) {
            console.error('Primary DB error!');
            console.log('Connecting to Secondary Database...');
            // Try secondary database if the primary fails
            dbSecondary.query(query, params, (err, results) => {
                if (err) {
                    console.error('Secondary DB error:', err.message);
                    return callback(err, null);
                } else {
                    return callback(null, results);
                }
            });
        } else {
            return callback(null, results);
        }
    });
}

// Function to execute a dual-write query for INSERT, UPDATE, DELETE operations
function executeDualWrite(query, params, callback) {
    dbPrimary.query(query, params, (err, results) => {
        if (err) {
            console.error('Primary DB error:');
            logQuery(query, params);  // Log the query if the primary DB is down
            dbSecondary.query(query, params, (err, results) => {
                if (err) {
                    return callback(err, null);
                }
                return callback(null, results);
            });
        } else {
            dbSecondary.query(query, params, (err) => {
                if (err) {
                    console.error('Secondary DB replication error:', err.message);
                }
            });
            return callback(null, results);
        }
    });
}

// Replay any pending changes to the primary database when the server starts
replayChanges();

// Route to get all cars with availability status
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
            return res.status(500).send('Error fetching car data');
        }
        res.json(results);
    });
});

// Route to get a specific car by ID with availability status
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
            return res.status(500).send('Error fetching car data');
        }
        res.json(results[0]);
    });
});

// Route to create a new user
router.post('/usuarios', (req, res) => {
    const { Username, Password, Email, Nombre, Apellido } = req.body;
    const query = 'INSERT INTO Usuarios (Username, Password, Email, Nombre, Apellido) VALUES (?, ?, ?, ?, ?)';
    executeDualWrite(query, [Username, Password, Email, Nombre, Apellido], (err, results) => {
        if (err) {
            return res.status(500).send('Error creating user');
        }
        res.status(201).send('Usuario creado con éxito');
    });
});

// Route to authenticate a user
router.post('/login', (req, res) => {
    const { Username, Password } = req.body;
    const query = 'SELECT * FROM Usuarios WHERE Username = ? AND Password = ?';

    executeQuery(query, [Username, Password], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error during login' });
        }

        if (results.length > 0) {
            return res.json({ message: 'Login successful', userId: results[0].ID });
        } else {
            return res.status(401).json({ message: 'Invalid credentials' });
        }
    });
});

// Route to get all rentals for a specific user
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
            return res.status(500).send('Error fetching rentals');
        }
        res.json(results);
    });
});

// Route to get user information by ID
router.get('/users/:id', (req, res) => {
    const userId = req.params.id;
    const query = 'SELECT ID, Username, Email, Nombre, Apellido FROM Usuarios WHERE ID = ?';
    executeQuery(query, [userId], (err, results) => {
        if (err) {
            return res.status(500).send('Error fetching user info');
        }
        res.json(results[0]);
    });
});

// Route to create a new rental
router.post('/rentals', (req, res) => {
    const { id_usuario, id_carro, ComienzoRenta, FinalRenta, CostoTotal } = req.body;
    const query = 'INSERT INTO Rentas (id_usuario, id_carro, ComienzoRenta, FinalRenta, CostoTotal) VALUES (?, ?, ?, ?, ?)';
    executeDualWrite(query, [id_usuario, id_carro, ComienzoRenta, FinalRenta, CostoTotal], (err, results) => {
        if (err) {
            return res.status(500).send('Error creating rental');
        }
        res.status(201).send('Rental created successfully');
    });
});

// Route to get all users (Admin only)
router.get('/admin/users', (req, res) => {
    const query = 'SELECT ID, Username, Email, Nombre, Apellido FROM Usuarios';
    executeQuery(query, [], (err, results) => {
        if (err) {
            return res.status(500).json({ error: 'Error fetching users' });
        }
        res.json(results);
    });
});

// Route to get all cars (Admin only)
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
            return res.status(500).json({ error: 'Error fetching cars' });
        }
        res.json(results);
    });
});

// Route to get all rentals (Admin only)
router.get('/admin/rentals', (req, res) => {
    const query = `
        SELECT Rentas.*, Carros.Marca, Carros.Modelo, Usuarios.Username 
        FROM Rentas 
        JOIN Carros ON Rentas.id_carro = Carros.ID 
        JOIN Usuarios ON Rentas.id_usuario = Usuarios.ID
    `;
    executeQuery(query, [], (err, results) => {
        if (err) {
            return res.status(500).json({ error: 'Error fetching rentals' });
        }
        res.json(results);
    });
});

// Fetch a specific user by ID
router.get('/usuarios/:id', (req, res) => {
    const userId = req.params.id;
    const query = 'SELECT ID, Username, Email, Nombre, Apellido FROM Usuarios WHERE ID = ?';
    executeQuery(query, [userId], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error fetching user' });
        }
        res.json(results[0]);
    });
});

// Update a specific user by ID
router.put('/usuarios/:id', (req, res) => {
    const userId = req.params.id;
    const { Username, Email, Nombre, Apellido } = req.body;
    const query = 'UPDATE Usuarios SET Username = ?, Email = ?, Nombre = ?, Apellido = ? WHERE ID = ?';
    executeDualWrite(query, [Username, Email, Nombre, Apellido, userId], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error updating user' });
        }
        res.json({ message: 'User updated successfully' });
    });
});

// Delete a specific user by ID
router.delete('/usuarios/:id', (req, res) => {
    const userId = req.params.id;
    const query = 'DELETE FROM Usuarios WHERE ID = ?';
    executeDualWrite(query, [userId], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error deleting user' });
        }
        res.json({ message: 'User deleted successfully' });
    });
});

// Fetch a specific car by ID
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
            return res.status(500).json({ message: 'Error fetching car' });
        }
        res.json(results[0]);
    });
});

// Update a specific car by ID
router.put('/carros/:id', (req, res) => {
    const carId = req.params.id;
    const { Marca, Modelo, Placa, id_disponibilidad, DetalleEstado, ImagenURL } = req.body;
    const query = 'UPDATE Carros SET Marca = ?, Modelo = ?, Placa = ?, id_disponibilidad = ?, DetalleEstado = ?, ImagenURL = ? WHERE ID = ?';
    executeDualWrite(query, [Marca, Modelo, Placa, id_disponibilidad, DetalleEstado, ImagenURL, carId], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error updating car' });
        }
        res.json({ message: 'Car updated successfully' });
    });
});

// Delete a specific car by ID
router.delete('/carros/:id', (req, res) => {
    const carId = req.params.id;
    const query = 'DELETE FROM Carros WHERE ID = ?';
    executeDualWrite(query, [carId], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error deleting car' });
        }
        res.json({ message: 'Car deleted successfully' });
    });
});

// Fetch a specific rental by ID
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
            return res.status(500).json({ message: 'Error fetching rental' });
        }
        res.json(results[0]);
    });
});

// Update a specific rental by ID
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
            return res.status(500).json({ message: 'Error updating rental' });
        }
        res.json({ message: 'Rental updated successfully' });
    });
});

// Delete a specific rental by ID
router.delete('/rentals/:id', (req, res) => {
    const rentalId = req.params.id;
    const query = 'DELETE FROM Rentas WHERE ID = ?';
    executeDualWrite(query, [rentalId], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error deleting rental' });
        }
        res.json({ message: 'Rental deleted successfully' });
    });
});

// Add a new user
router.post('/admin/users', (req, res) => {
    const { Username, Password, Email, Nombre, Apellido } = req.body;
    const query = 'INSERT INTO Usuarios (Username, Password, Email, Nombre, Apellido) VALUES (?, ?, ?, ?, ?)';
    executeDualWrite(query, [Username, Password, Email, Nombre, Apellido], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error adding user' });
        }
        res.status(201).json({ message: 'User added successfully!' });
    });
});

// Add a new car
router.post('/admin/cars', (req, res) => {
    const { Marca, Modelo, Placa, id_disponibilidad, ImagenURL, DetalleEstado } = req.body;
    const query = 'INSERT INTO Carros (Marca, Modelo, Placa, id_disponibilidad, ImagenURL, DetalleEstado) VALUES (?, ?, ?, ?, ?, ?)';
    executeDualWrite(query, [Marca, Modelo, Placa, id_disponibilidad, ImagenURL, DetalleEstado], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error adding car' });
        }
        res.status(201).json({ message: 'Car added successfully!' });
    });
});

// Route to get all availability statuses
router.get('/availability', (req, res) => {
    const query = 'SELECT * FROM Disponibilidad';
    executeQuery(query, [], (err, results) => {
        if (err) {
            return res.status(500).json({ error: 'Error fetching availability statuses' });
        }
        res.json(results);
    });
});

module.exports = router;
