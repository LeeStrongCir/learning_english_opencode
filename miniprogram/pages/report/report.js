const api = require('../../utils/api')

Page({
  data: {
    report: null,
    loading: true
  },

  onLoad(options) {
    if (options.sessionId) {
      this.loadReport(options.sessionId)
    } else {
      // 如果没有sessionId，显示空状态
      this.setData({ loading: false })
    }
  },

  async loadReport(sessionId) {
    this.setData({ loading: true })
    try {
      // 调用API获取报告
      const res = await api.getReport(sessionId)
      this.setData({
        report: res,
        loading: false
      })
    } catch (err) {
      console.error('获取报告失败:', err)
      // 使用模拟数据
      this.setData({
        report: this.getMockReport(),
        loading: false
      })
    }
  },

  onRetry() {
    // 返回上一页重新练习
    wx.navigateBack({
      delta: 1
    })
  },

  onGoHome() {
    // 返回首页
    wx.switchTab({
      url: '/pages/index/index'
    })
  },

  getMockReport() {
    // 模拟报告数据
    return {
      totalScore: 85,
      encouragement: '太棒了！继续加油，你的英语越来越好了！🎉',
      pronunciationScore: 82,
      pronunciationFeedback: '发音清晰，注意 th 音的咬舌发音。',
      grammarScore: 78,
      grammarFeedback: '句子结构基本正确，注意第三人称单数要加s。',
      vocabularyScore: 88,
      vocabularyUsageRate: 75,
      targetWords: [
        { word: 'hello', used: true },
        { word: 'friend', used: true },
        { word: 'school', used: true },
        { word: 'teacher', used: false },
        { word: 'classmate', used: true }
      ],
      strengths: [
        '敢于开口说英语，非常勇敢！',
        '能够使用学过的单词造句',
        '语音语调比较自然'
      ],
      suggestions: [
        '注意单词的发音细节，可以多听多模仿',
        '尝试使用更完整的句子表达',
        '复习本单元的目标词汇，争取全部用上'
      ]
    }
  }
})
