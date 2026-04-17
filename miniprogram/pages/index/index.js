const api = require('../../utils/api')

Page({
  data: {
    grades: [3, 4, 5, 6],
    gradeIndex: 0,
    selectedGrade: 3,
    semesters: [
      { value: 'upper', label: '上册' },
      { value: 'lower', label: '下册' }
    ],
    semesterLabels: ['上册', '下册'],
    semesterIndex: 0,
    selectedSemester: 'upper',
    units: [],
    loading: false
  },

  onLoad() {
    this.loadUnits()
  },

  onShow() {
    // 每次显示页面时刷新单元列表
    this.loadUnits()
  },

  onGradeChange(e) {
    const index = e.detail.value
    this.setData({
      gradeIndex: index,
      selectedGrade: this.data.grades[index]
    })
    this.loadUnits()
  },

  onSemesterChange(e) {
    const index = e.detail.value
    this.setData({
      semesterIndex: index,
      selectedSemester: this.data.semesters[index].value
    })
    this.loadUnits()
  },

  async loadUnits() {
    this.setData({ loading: true })
    try {
      // 调用API获取单元列表
      const res = await api.getTextbook()
      // 根据年级和学期过滤单元
      const filteredUnits = (res.units || []).filter(unit => 
        unit.grade === this.data.selectedGrade && 
        unit.semester === this.data.selectedSemester
      )
      this.setData({ units: filteredUnits })
    } catch (err) {
      console.error('加载单元失败:', err)
      // 使用模拟数据作为降级方案
      this.setData({
        units: this.getMockUnits()
      })
    } finally {
      this.setData({ loading: false })
    }
  },

  onUnitTap(e) {
    const { unit, lesson } = e.currentTarget.dataset
    // 跳转到对话页面，传递参数
    wx.navigateTo({
      url: `/pages/dialogue/dialogue?unit=${unit}&lesson=${lesson || ''}&grade=${this.data.selectedGrade}&semester=${this.data.selectedSemester}`
    })
  },

  getMockUnits() {
    // 模拟数据，用于测试
    return [
      {
        id: 1,
        unit: 1,
        grade: this.data.selectedGrade,
        semester: this.data.selectedSemester,
        title: 'Hello!',
        titleCn: '你好！',
        scenarios: ['打招呼', '自我介绍']
      },
      {
        id: 2,
        unit: 2,
        grade: this.data.selectedGrade,
        semester: this.data.selectedSemester,
        title: 'My Family',
        titleCn: '我的家庭',
        scenarios: ['介绍家人', '家庭活动']
      },
      {
        id: 3,
        unit: 3,
        grade: this.data.selectedGrade,
        semester: this.data.selectedSemester,
        title: 'At School',
        titleCn: '在学校',
        scenarios: ['课堂对话', '课间活动']
      },
      {
        id: 4,
        unit: 4,
        grade: this.data.selectedGrade,
        semester: this.data.selectedSemester,
        title: 'My Day',
        titleCn: '我的一天',
        scenarios: ['日常作息', '时间表达']
      }
    ]
  }
})
