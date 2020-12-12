const csv = require('csv-parser');
const fs = require('fs');

var videos = [];
fs.createReadStream('./../get_data/videos_no_dups.csv')
.pipe(csv())
.on('data', (row) => {
    videos.push(row);
})
.on('end', () => {
    console.log('CSV file successfully processed');
});

module.exports = videos;