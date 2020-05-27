var mongoose = require('mongoose')
var Schema = mongoose.Schema

var ProductSchema = new Schema({
    name: String,
    space: String,
    start_date: Date,
    end_date: Date,
    device: String
})

module.exports = mongoose.model('product', ProductSchema)