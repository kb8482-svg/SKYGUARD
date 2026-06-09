const express = require('express');
const { Pool } = require('pg');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

const app = express();
app.use(express.json());

const pool = new Pool({
  user: process.env.POSTGRES_USER || 'skyguard_user',
  host: process.env.POSTGRES_HOST || 'postgres-db',
  database: process.env.POSTGRES_DB || 'skyguard_auth',
  password: process.env.POSTGRES_PASSWORD || 'password123',
  port: Number(process.env.POSTGRES_PORT || 5432),
});

const SECRET = process.env.JWT_SECRET || "skyguard-secret";

async function initDatabase() {
    await pool.query(`
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    `);

    await pool.query(`
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            title TEXT NOT NULL,
            location TEXT NOT NULL,
            event_time TIMESTAMPTZ NOT NULL,
            event_end_time TIMESTAMPTZ,
            notes TEXT DEFAULT '',
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    `);

    await pool.query(`ALTER TABLE events ADD COLUMN IF NOT EXISTS event_end_time TIMESTAMPTZ`);
}

function authenticate(req, res, next) {
    const header = req.headers.authorization || '';
    const token = header.startsWith('Bearer ') ? header.slice(7) : null;

    if (!token) {
        return res.status(401).json({ message: 'Manjka avtentikacijski token' });
    }

    try {
        req.user = jwt.verify(token, SECRET);
        next();
    } catch (err) {
        res.status(401).json({ message: 'Neveljaven ali potekel token' });
    }
}

app.get('/health', (req, res) => {
    res.json({ status: 'user-service OK' });
});

// REGISTER
app.post('/auth/register', async (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).json({ message: 'Uporabniško ime in geslo sta obvezna' });
    }

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

    if (!username || !password) {
        return res.status(400).json({ message: 'Uporabniško ime in geslo sta obvezna' });
    }

    const result = await pool.query(
        'SELECT id, username, password FROM users WHERE username=$1',
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

    const token = jwt.sign({ id: user.id, username: user.username }, SECRET, { expiresIn: "1h" });

    res.json({ message: 'Login OK', token });
});

app.get('/events', authenticate, async (req, res) => {
    const result = await pool.query(
        `SELECT id, title, location, event_time, event_end_time, notes, created_at
         FROM events
         WHERE user_id=$1
         ORDER BY event_time ASC`,
        [req.user.id]
    );

    res.json(result.rows);
});

app.post('/events', authenticate, async (req, res) => {
    const { title, location, event_start, event_end, event_time, notes } = req.body;
    const startTime = event_start || event_time;
    const endTime = event_end || null;

    if (!title || !location || !startTime || !endTime) {
        return res.status(400).json({ message: 'Naslov, lokacija, začetek in konec dogodka so obvezni' });
    }

    if (new Date(endTime) <= new Date(startTime)) {
        return res.status(400).json({ message: 'Konec dogodka mora biti po začetku' });
    }

    const result = await pool.query(
        `INSERT INTO events (user_id, title, location, event_time, event_end_time, notes)
         VALUES ($1, $2, $3, $4, $5, $6)
         RETURNING id, title, location, event_time, event_end_time, notes, created_at`,
        [req.user.id, title, location, startTime, endTime, notes || '']
    );

    res.status(201).json(result.rows[0]);
});

app.delete('/events/:id', authenticate, async (req, res) => {
    const result = await pool.query(
        'DELETE FROM events WHERE id=$1 AND user_id=$2 RETURNING id',
        [req.params.id, req.user.id]
    );

    if (result.rowCount === 0) {
        return res.status(404).json({ message: 'Dogodek ne obstaja' });
    }

    res.json({ message: 'Dogodek izbrisan' });
});

initDatabase()
    .then(() => {
        app.listen(5001, () => {
            console.log("User service running on 5001");
        });
    })
    .catch((err) => {
        console.error("Database initialization failed", err);
        process.exit(1);
    });
