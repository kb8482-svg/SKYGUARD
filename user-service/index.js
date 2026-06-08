const express = require('express');
const { Pool } = require('pg');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

const app = express();
app.use(express.json());

const pool = new Pool({
  user: 'skyguard_user',
  host: 'postgres-db',
  database: 'skyguard_auth',
  password: 'password123',
  port: 5432,
});

const SECRET = "skyguard-secret";

// CREATE TABLE
pool.query(`
CREATE TABLE IF NOT EXISTS users (
id SERIAL PRIMARY KEY,
username TEXT UNIQUE,
password TEXT
)
`);

// REGISTER
app.post('/auth/register', async (req, res) => {
    const { username, password } = req.body;

    const hashed = await bcrypt.hash(password, 10);

    try {
        await pool.query(
            'INSERT INTO users (username, password) VALUES ($1, $2)',
            [username, hashed]
        );

        res.status(201).json({ message: 'Registracija uspešna!' });

    } catch (err) {
        res.status(400).json({ message: 'Napaka ali uporabnik obstaja' });
    }
});

// LOGIN
app.post('/auth/login', async (req, res) => {
    const { username, password } = req.body;

    const result = await pool.query(
        'SELECT * FROM users WHERE username=$1',
        [username]
    );

    if (result.rows.length === 0) {
        return res.status(401).json({ message: 'Uporabnik ne obstaja' });
    }

    const user = result.rows[0];

    const valid = await bcrypt.compare(password, user.password);

    if (!valid) {
        return res.status(401).json({ message: 'Napačno geslo' });
    }

    const token = jwt.sign({ user: username }, SECRET, { expiresIn: "1h" });

    res.json({ message: 'Login OK', token });
});

app.listen(5001, () => {
    console.log("User service running on 5001");
});