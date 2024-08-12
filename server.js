const express = require('express');
const path = require('path');
const app = express();
const routes = require('./routes'); // traer las rutas
const PORT = process.env.PORT || 3008;

app.use(express.static(path.join(__dirname, 'HTML')));
app.use(express.json()); // Usar json como middleware para manejar solicitudes JSON

app.use('/', routes);

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
