import Taro, { Component } from '@tarojs/taro'
import styles from './index.module.scss'

export default class Type extends Component {
  constructor(props) {
    super(props)
  }
  componentWillMount() {}
  render() {
    return (
      <view>
        <text class={styles.title}>请选择查询的类型</text>
        <Navigator url='/pages/index/index?type=web'>前端</Navigator>
        <Navigator url='/pages/index/index?type=Python'>Python</Navigator>
        <Navigator url='/pages/index/index?type=Java'>Java</Navigator>
        <Navigator url='/pages/index/index?type=PHP'>PHP</Navigator>
        <Navigator url='/pages/index/index?type=C'>C</Navigator>
        <Navigator url='/pages/index/index?type=C++'>C++</Navigator>
        <Navigator url='/pages/index/index?type=C#'>C#</Navigator>
      </view>
    )
  }
}
