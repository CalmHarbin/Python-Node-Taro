const { model } = require('./db.js')

//获取学历
exports.get_workYear = function(type, callback) {
    //查询所有的本科学历
    model[type].find({}, { workYear: 1 }, function(err, res) {
        if (err) return callback(err)
        let result = [],
            type = []
        //找出每种学历的数量
        res.forEach(item => {
            if (type.includes(item.workYear)) {
                result[type.indexOf(item.workYear)].count++
            } else {
                type.push(item.workYear)
                result.push({
                    label: item.workYear,
                    count: 1
                })
            }
        })
        callback(null, result)
    })
}
