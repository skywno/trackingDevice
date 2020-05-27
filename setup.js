var express = require('express')
var ejs = require('ejs')
var mongoose = require('mongoose')
var bodyParser = require('body-parser')
//enable body-parser middleware for parse incoming request bodies
var app = express()
var mainRoutes = require('./routes/main')


let name = ""

mongoose.connect('mongodb://localhost:27017/project')

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({
    extended: true
}))
app.use(mainRoutes)

port = 3001
app.set('view engine', 'ejs')

app.get ('/', (req, res) => {
   res.render('login', {anything: name}) //mapping of what we have in our var inside of JavaScript
})

app.get ('/setup', (req, res) => {
   res.render('setup', {anything: name}) //mapping of what we have in our var inside of JavaScript
})

app.get ('/current', (req, res) => {
   res.render('current', {anything: name}) //mapping of what we have in our var inside of JavaScript
})

app.get ('/arc', (req, res) => {
   res.render('archive', {anything: name}) //mapping of what we have in our var inside of JavaScript
})

app.use(express.static(__dirname + '/views'));

app.listen(port, () => console.log(`Server runs on port ${port}.`)) //server starting and it is logs that it is running