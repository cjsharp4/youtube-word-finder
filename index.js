//npm init -y

/* 
console.log(process.platform);

process.on('exit', function()){

    //do something

}



const { readfile , readFileSync, readFile, appendFile } = require('fs');

//sync
const txt = readFileSync('./hello.txt', 'utf8');
console.log(txt);

//callback
readFile('./hello.txt', 'utf8', (err, txt) => {
    console.log(txt)
});

console.log("do this asap");

*/

const{ readFile } = require('fs').promises;

const express = require('express');
const app = express();

app.use(express.static('public'));

//app.use(express.json());
app.use(express.urlencoded({ extended: true }));

var pythonScraper = function(targetWord) {

    //const  { spawn } = require('child_process');
    var spawn  = require('child_process');
    //var childPython = spawn.spawnSync('python3', ['--version'], { encoding : 'utf8' });
    var childPython = spawn.spawnSync('python3', ['videoScraper.py', targetWord], { encoding : 'utf8' });
    
    console.log('ls: ' , childPython);

};

/*
//callback/non-promise version
app.get('/', (request, response) => {
    readFile('./home.html', 'utf8', (err, html) => {
        if(err){
            response.status(500).send('sorry, out of order')
        }

        response.add(html);
    })
});
*/

//promise/async version
app.get('/', async (request, response) => {

    response.send( await readFile('./home.html', 'utf8'));
});

app.post('/', async (request, response) => {
    var inputWord = request.body.firstWord;
    console.log(inputWord);
    pythonScraper(inputWord);
    response.redirect('/results.html');

});

//host app on: http://localhost:3000/
app.listen(process.env.PORT || 3000, () => console.log('App available on http://localhost:3000'))
