const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const cors = require('cors');

let messages = []; // In-memory message store

app.use(cors());
app.use(bodyParser.json());

app.get('/messages', (req, res) => {
  res.json(messages);
});

app.post('/send', (req, res) => {
  const { sender, text } = req.body;
  messages.push({ sender, text, time: Date.now() });
  res.sendStatus(200);
});

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});
