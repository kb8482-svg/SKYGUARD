const express = require('express');
const app = express();
const PORT = 5003;

app.post('/upload', express.json(), (req, res) => {
    res.status(201).json({ message: "Slika poslana proti Min.io", image_id: "sky_1" });
});

app.get('/image/:id', (req, res) => {
    res.json({ url: `https://minio.skyguard.internal/bucket/${req.params.id}.png` });
});

app.listen(PORT, () => console.log(`Storage service teče na portu ${PORT}`));