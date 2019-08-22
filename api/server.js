const http = require('http')
var url = require('url')
var qs = require('qs')
const { get_education } = require('./api/education.js')
const { get_workYear } = require('./api/workYear.js')
const { get_salary } = require('./api/salary.js')

//用node中的http创建服务器 并传入两个形参
http.createServer(function(req, res) {
    //设置请求头  允许所有域名访问 解决跨域
    res.setHeader('Access-Control-Allow-Origin', '*')
    res.writeHead(200, { 'Content-Type': 'application/json;charset=utf-8' }) //设置response编码

    try {
        //获取地址中的参数部分
        var query = url.parse(req.url).query
        //用qs模块的方法  把地址中的参数转变成对象 方便获取
        var queryObj = qs.parse(query)
        //获取前端传来的myUrl=后面的内容　　GET方式传入的数据
        var type = queryObj.type
        // console.log(type)

        if (req.url.indexOf('/get_education?type=') > -1) {
            get_education(type, function(err, data) {
                if (err) res.end({ errmsg: err })
                console.log('[ok] /get_education')
                res.end(JSON.stringify(data))
            })
        } else if (req.url.indexOf('/get_workYear?type=') > -1) {
            get_workYear(type, function(err, data) {
                if (err) res.end({ errmsg: err })
                console.log('[ok] /get_workYear')
                res.end(JSON.stringify(data))
            })
        } else if (req.url.indexOf('/get_salary?type=') > -1) {
            get_salary(type, function(err, data) {
                if (err) res.end({ errmsg: err })
                console.log('[ok] /get_salary')
                res.end(JSON.stringify(data))
            })
        } else {
            console.log(req.url)
            res.end('404')
        }
    } catch (err) {
        res.end(err)
    }
}).listen(8989, function(err) {
    if (!err) {
        console.log('服务器启动成功，正在监听8989...')
    }
})
