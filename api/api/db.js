const mongoose = require('mongoose')
const DB_URL = 'mongodb://localhost:27017/db'
// 连接数据库
mongoose.connect(DB_URL, { useNewUrlParser: true })

var Schema = mongoose.Schema

let collections = ['web', 'Python', 'PHP', 'Java', 'C++', 'C#', 'C']
let model = {}

collections.forEach(collection => {
    let UserSchema = new Schema(
        {
            positionName: { type: String }, //职位
            workYear: { type: String }, //工作年限
            salary: { type: String }, //薪水
            education: { type: String }, //学历
            companySize: { type: String }, //规模
            companyFullName: { type: String }, //公司名
            formatCreateTime: { type: String }, //发布时间
            positionId: { type: Number } //id
        },
        {
            collection: collection
        }
    )
    let web_model = mongoose.model(collection, UserSchema)
    model[collection] = web_model
})

exports.model = model
