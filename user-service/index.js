const express = require('express');
const app = express();
app.use(express.json());

const PORT = 5001;

// API klici za 2. mejnik
app.post('/register', (req, res) => res.status(201).json({ message: "Uporabnik registriran" }));
app.post('/login', (req, res) => res.json({ token: "fake-jwt-token" }));
app.get('/events', (req, res) => res.json([{ id: 1, name: "SkyGuard Event", location: "Ljubljana" }]));
app.post('/events', (req, res) => res.status(201).json({ message: "Dogodek ustvarjen", data: req.body }));
app.delete('/events/:id', (req, res) => res.json({ message: `Dogodek ${req.params.id} izbrisan` }));

app.listen(PORT, () => console.log(`User service teče na portu ${PORT}`));