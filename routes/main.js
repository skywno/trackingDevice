var router = require('express').Router()
var Product = require('../models/product')

router.get('/setup', function(req, res, next) {
    res.render('main/setup')
})

router.post('/setup', function(req, res, next) {
    var product = new Product()

    product.name = req.body.exhibition_name
    product.space = req.body.space_name
    product.start_date = req.body.Start
    product.end_date = req.body.End
    product.device = req.body.devicelist

    product.save(function(err) {
        if (err) throw err
        res.redirect('/setup')
    })
})

module.exports = router