const express = require('express');
const cors = require('cors');

require('dotenv').config();

const app = express();
const router = express.Router();
const port = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

const videos = require('./get_videos');

router.route("/").get((req, res) => {
    res.status(200).json(getRandomVideo(videos));
});

app.use("/", router);

app.listen(port, () => {
    console.log(`Server is running on port: ${port}`);
});


function getRandomVideo(videos) {
    return videos[Math.round(Math.random() * videos.length)]
}