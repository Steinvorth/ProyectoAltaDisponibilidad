const express = require('express');
const path = require('path');
const app = express();
const routes = require('./routes'); // Import the routes
const PORT = process.env.PORT || 3006;

app.use(express.static(path.join(__dirname, 'HTML')));
app.use(express.json()); // Middleware to parse JSON bodies

// Use the routes from routes.js
app.use('/', routes);

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
