import Taro from '@tarojs/taro'
import config from '../config/index'

function Api(path, data = {}) {
  return new Promise((resolve, reject) => {
    Taro.request({
      url: config.serverUrl + path,
      data: data,
      header: {
        'content-type': 'application/json'
      }
    })
      .then(res => {
        if (res.statusCode >= 200 && res.statusCode <= 300) {
          resolve(res.data)
        } else {
          if (res.errMsg) {
            Taro.showModal({
              title: '提示',
              content: res.errMsg,
              showCancel: false
            })
          } else {
            Taro.showModal({
              title: '提示',
              content: '出错了',
              showCancel: false
            })
            Taro.hideLoading()
          }
        }
      })
      .catch(err => {
        Taro.showModal({
          title: '提示',
          content: err.errMsg,
          showCancel: false
        })
        Taro.hideLoading()
        reject(err)
      })
  })
}

//获取学历占比
const get_education = (data = {}) => new Api('/get_education', data)
//获取工资经验占比
const get_workYear = (data = {}) => new Api('/get_workYear', data)
//获取薪资占比
const get_salary = (data = {}) => new Api('/get_salary', data)

export { get_education, get_workYear, get_salary }
