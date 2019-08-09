const { model } = require('./db.js')

//获取学历
exports.get_education = function(type, callback) {
    //查询所有的本科学历
    model[type].find({}, { education: 1 }, function(err, res) {
        if (err) return callback(err)
        let result = [],
            type = []
        //找出每种学历的数量
        res.forEach(item => {
            if (type.includes(item.education)) {
                result[type.indexOf(item.education)].count++
            } else {
                type.push(item.education)
                result.push({
                    label: item.education,
                    count: 1
                })
            }
        })
        callback(null, result)
    })
}
