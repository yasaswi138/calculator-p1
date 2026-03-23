const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const HISTORY_FILE = path.join(__dirname, 'history.json');

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Initialize history file if it doesn't exist
if (!fs.existsSync(HISTORY_FILE)) {
    fs.writeFileSync(HISTORY_FILE, JSON.stringify([]));
}

// GET /history
app.get('/history', (req, res) => {
    try {
        const data = fs.readFileSync(HISTORY_FILE, 'utf8');
        res.json(JSON.parse(data));
    } catch (error) {
        res.status(500).json({ error: 'Failed to read history' });
    }
});

// POST /calculate
app.post('/calculate', (req, res) => {
    const { expression, result } = req.body;
    if (!expression || result === undefined) {
        return res.status(400).json({ error: 'Missing expression or result' });
    }

    try {
        const data = fs.readFileSync(HISTORY_FILE, 'utf8');
        const history = JSON.parse(data);
        const newEntry = {
            id: Date.now(),
            expression,
            result: Number(result).toFixed(2),
            timestamp: new Date().toISOString()
        };
        history.unshift(newEntry);
        
        fs.writeFileSync(HISTORY_FILE, JSON.stringify(history, null, 2));
        res.status(201).json(newEntry);
    } catch (error) {
        res.status(500).json({ error: 'Failed to save calculation' });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
