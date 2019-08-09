const { model } = require('./db.js')

//获取学历
exports.get_salary = function(type, callback) {
    //查询所有的本科学历
    // ['4k以下', '4k-8k', '8k-12k', '12k-15k', '15k-20k', '20k-30k', '30k以上'];
    let result = [
        {
            label: '4k以下',
            count: 0
        },
        {
            label: '4k-8k',
            count: 0
        },
        {
            label: '8k-12k',
            count: 0
        },
        {
            label: '12k-15k',
            count: 0
        },
        {
            label: '15k-20k',
            count: 0
        },
        {
            label: '20k-30k',
            count: 0
        },
        {
            label: '30k以上',
            count: 0
        }
    ]

    model[type].find({}, { salary: 1 }, function(err, res) {
        if (err) return callback(err)
        //找出每种学历的数量
        res.forEach(item => {
            let Range = item.salary.split('-')
            let start_index = null //开始薪水所在范围
            Range.forEach(money => {
                money = parseFloat(money)
                if (money < 4) {
                    if (start_index !== 0) result[0].count++
                    start_index = 0
                } else if (money >= 4 && money < 8) {
                    if (start_index !== 1) result[1].count++
                    start_index = 1
                } else if (money >= 8 && money < 12) {
                    if (start_index !== 2) result[2].count++
                    start_index = 2
                } else if (money >= 12 && money < 15) {
                    if (start_index !== 3) result[3].count++
                    start_index = 3
                } else if (money >= 15 && money < 20) {
                    if (start_index !== 4) result[4].count++
                    start_index = 4
                } else if (money >= 20 && money < 30) {
                    if (start_index !== 5) result[5].count++
                    start_index = 5
                } else if (money >= 30) {
                    if (start_index !== 6) result[6].count++
                    start_index = 6
                }
            })
        })
        callback(null, result)
    })
}
