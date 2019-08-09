import Taro, { Component } from '@tarojs/taro'
import { View, Text } from '@tarojs/components'
import { get_education, get_workYear, get_salary } from '../../api/index'
import * as echarts from '../../components/ec-canvas/echarts'
import './index.scss'

export default class Index extends Component {
  config = {
    navigationBarTitleText: '数据分析',
    // 定义需要引入的第三方组件
    usingComponents: {
      'ec-canvas': '../../components/ec-canvas/ec-canvas' // 书写第三方组件的相对路径
    }
  }
  constructor(props) {
    super(props)
    this.state = {
      ec: {
        // onInit: this.initChart
        lazyLoad: true // 延迟加载
      },
      ec2: {
        // onInit: initChart2
        lazyLoad: true // 延迟加载
      },
      ec3: {
        // onInit: initChart3
        lazyLoad: true // 延迟加载
      },
      education: [],
      workYear: [],
      salary: []
    }
    // this.initChart = this.initChart.bind(this)
  }
  componentWillMount() {
    // console.log(params)
    console.log(this.$router.params.type)

    Taro.showLoading({
      title: 'loading'
    })
    Promise.all([
      get_education({ type: this.$router.params.type }),
      get_workYear({ type: this.$router.params.type }),
      get_salary({ type: this.$router.params.type })
    ])
      .then(res => {
        Taro.hideLoading()
        let education = [],
          workYear = []
        res[0].forEach(item => {
          let { label, count } = item
          education.push({
            name: label + count,
            value: count
          })
        })
        res[1].forEach(item => {
          let { label, count } = item
          workYear.push({
            name: label,
            value: count
          })
        })
        this.setState(
          {
            education,
            workYear,
            salary: res[2]
          },
          () => {
            this.$scope.selectComponent('#mychart-dom-bar1').init(this.initChart.bind(this))
            this.$scope.selectComponent('#mychart-dom-bar2').init(this.initChart2.bind(this))
            this.$scope.selectComponent('#mychart-dom-bar3').init(this.initChart3.bind(this))
          }
        )
      })
      .catch(err => {
        Taro.hideLoading()
      })
  }

  // 学历占比
  initChart(canvas, width, height) {
    const chart = echarts.init(canvas, null, {
      width: width,
      height: height
    })
    canvas.setChart(chart)

    var option = {
      title: {
        text: '学历占比',
        subtext: '数据来源: 拉勾网',
        textAlign: 'left'
        //   x: 'center'
      },
      calculable: true,
      series: [
        {
          name: '学历占比',
          type: 'funnel',
          sort: 'ascending', //排序, 升高
          silent: true,
          left: '0',
          width: '100%',
          gap: 1, //间距
          label: {
            show: true,
            position: 'right'
          },
          //   data: [
          //     { value: 60, name: '不限' },
          //     { value: 40, name: '硕士' },
          //     { value: 80, name: '大专' },
          //     { value: 200, name: '本科' }
          //   ]
          data: this.state.education
        }
      ]
    }
    chart.setOption(option)
    return chart
  }
  // 薪资占比
  initChart2(canvas, width, height) {
    const chart = echarts.init(canvas, null, {
      width: width,
      height: height
    })
    canvas.setChart(chart)

    var option = {
      title: {
        text: '工作经验',
        subtext: '数据来源: 拉勾网',
        x: 'center'
      },
      series: [
        {
          name: '面积模式',
          type: 'pie',
          radius: [30, 110],
          center: ['50%', '50%'],
          roseType: 'area',
          data: this.state.workYear
        }
      ]
    }
    chart.setOption(option)
    return chart
  }
  //工作经验占比
  initChart3(canvas, width, height) {
    let xAxisData = this.state.salary.map(item => item.label)
    let seriesData = this.state.salary.map(item => item.count)
    const chart = echarts.init(canvas, null, {
      width: width,
      height: height
    })
    canvas.setChart(chart)

    var option = {
      title: {
        text: '薪资占比',
        subtext: '数据来源: 拉勾网',
        x: 'center'
      },
      xAxis: {
        type: 'category',
        data: xAxisData,
        axisLabel: {
          //坐标轴刻度标签的相关设置。
          interval: 0,
          rotate: '45'
        }
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          data: seriesData,
          type: 'bar'
        }
      ]
    }
    chart.setOption(option)
    return chart
  }
  render() {
    return (
      <View className='index'>
        <Text className='title'>
          {this.$router.params.type === 'web' ? '前端' : this.$router.params.type}岗位分析
        </Text>
        {/* <Text>前端岗位分析</Text> */}
        <View className='container'>
          <ec-canvas id='mychart-dom-bar1' canvas-id='mychart-bar1' ec={this.state.ec} />
        </View>
        <View className='container2'>
          <ec-canvas id='mychart-dom-bar2' canvas-id='mychart-bar2' ec={this.state.ec2} />
        </View>
        <View className='container3'>
          <ec-canvas id='mychart-dom-bar3' canvas-id='mychart-bar3' ec={this.state.ec3} />
        </View>
      </View>
    )
  }
}
