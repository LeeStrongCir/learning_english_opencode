const api = require('../../utils/api')
const app = getApp()

Page({
  data: {
    sessionId: null,
    scenarioName: '',
    grade: 3,
    unit: 1,
    messages: [],
    currentTurn: 0,
    maxTurns: 10,
    isRecording: false,
    inputText: '',
    isAiThinking: false,
    scrollToId: '',
    recorderManager: null,
    innerAudioContext: null
  },

  onLoad(options) {
    // 保存页面参数
    this.setData({
      grade: options.grade || 3,
      unit: options.unit || 1
    })
    // 初始化录音管理器
    this.initRecorder()
    this.initAudioPlayer()
    // 开始对话
    this.startDialogue(options)
  },

  onUnload() {
    // 页面卸载时清理资源
    if (this.data.innerAudioContext) {
      this.data.innerAudioContext.destroy()
    }
  },

  initRecorder() {
    const recorderManager = wx.getRecorderManager()
    this.setData({ recorderManager })

    // 监听录音开始
    recorderManager.onStart(() => {
      console.log('录音开始')
      this.setData({ isRecording: true })
    })

    // 监听录音停止
    recorderManager.onStop((res) => {
      console.log('录音停止', res)
      this.setData({ isRecording: false })
      if (res.tempFilePath) {
        this.sendVoiceMessage(res.tempFilePath)
      }
    })

    // 监听录音错误
    recorderManager.onError((err) => {
      console.error('录音错误', err)
      this.setData({ isRecording: false })
      wx.showToast({
        title: '录音失败，请重试',
        icon: 'none'
      })
    })
  },

  initAudioPlayer() {
    const innerAudioContext = wx.createInnerAudioContext()
    this.setData({ innerAudioContext })

    // 监听播放错误
    innerAudioContext.onError((err) => {
      console.error('音频播放错误', err)
      wx.showToast({
        title: '播放失败',
        icon: 'none'
      })
    })
  },

  async startDialogue(options) {
    wx.showLoading({ title: '开始对话...' })
    try {
      // 调用API开始对话
      const res = await api.startDialogue({
        grade: this.data.grade,
        unit: options.unit,
        semester: options.semester,
        scenario: options.scenario
      })
      
      this.setData({
        sessionId: res.sessionId,
        scenarioName: res.scenarioName || `Unit ${options.unit} 情景对话`,
        maxTurns: res.maxTurns || 10
      })

      // 保存sessionId到全局
      app.globalData.currentSessionId = res.sessionId

      // 添加AI欢迎消息
      if (res.welcomeMessage) {
        this.addMessage({
          isAi: true,
          text: res.welcomeMessage.text,
          translation: res.welcomeMessage.translation,
          audioUrl: res.welcomeMessage.audioUrl
        })
      }
    } catch (err) {
      console.error('开始对话失败:', err)
      // 使用模拟数据
      this.setData({
        sessionId: 'mock-session-' + Date.now(),
        scenarioName: `Unit ${options.unit} 情景对话`
      })
      this.addMessage({
        isAi: true,
        text: `Hello! Let's practice English together. This is Unit ${options.unit}.`,
        translation: '你好！让我们一起练习英语吧。这是第' + options.unit + '单元。'
      })
    } finally {
      wx.hideLoading()
    }
  },

  onTouchStart() {
    // 开始录音
    if (this.data.isAiThinking) {
      wx.showToast({
        title: 'AI正在思考，请稍等',
        icon: 'none'
      })
      return
    }

    const recorderManager = this.data.recorderManager
    recorderManager.start({
      duration: 60000,
      sampleRate: 16000,
      numberOfChannels: 1,
      encodeBitRate: 96000,
      format: 'mp3'
    })
  },

  onTouchEnd() {
    // 停止录音
    if (this.data.isRecording) {
      this.data.recorderManager.stop()
    }
  },

  async sendVoiceMessage(tempFilePath) {
    if (!this.data.sessionId) {
      wx.showToast({
        title: '对话未开始',
        icon: 'none'
      })
      return
    }

    wx.showLoading({ title: '识别中...' })
    this.setData({ isAiThinking: true })

    try {
      // 上传语音文件
      const uploadRes = await api.uploadVoice(tempFilePath)
      
      // 发送对话轮次
      const res = await api.sendTurn({
        sessionId: this.data.sessionId,
        text: uploadRes.text,
        audioUrl: uploadRes.audioUrl
      })

      // 添加用户消息
      this.addMessage({
        isAi: false,
        text: uploadRes.text || '[语音消息]'
      })

      // 添加AI回复
      if (res.reply) {
        this.addMessage({
          isAi: true,
          text: res.reply.text,
          translation: res.reply.translation,
          audioUrl: res.reply.audioUrl
        })
      }

      // 更新轮次
      this.setData({
        currentTurn: this.data.currentTurn + 1
      })

      // 检查是否达到最大轮次
      if (this.data.currentTurn >= this.data.maxTurns) {
        this.endDialogue()
      }
    } catch (err) {
      console.error('发送语音消息失败:', err)
      wx.showToast({
        title: '发送失败，请重试',
        icon: 'none'
      })
    } finally {
      wx.hideLoading()
      this.setData({ isAiThinking: false })
    }
  },

  async sendTextMessage() {
    const text = this.data.inputText.trim()
    if (!text || !this.data.sessionId) return

    this.setData({
      inputText: '',
      isAiThinking: true
    })

    try {
      // 发送对话轮次
      const res = await api.sendTurn({
        sessionId: this.data.sessionId,
        text: text
      })

      // 添加用户消息
      this.addMessage({
        isAi: false,
        text: text
      })

      // 添加AI回复
      if (res.reply) {
        this.addMessage({
          isAi: true,
          text: res.reply.text,
          translation: res.reply.translation,
          audioUrl: res.reply.audioUrl
        })
      }

      // 更新轮次
      this.setData({
        currentTurn: this.data.currentTurn + 1
      })

      // 检查是否达到最大轮次
      if (this.data.currentTurn >= this.data.maxTurns) {
        this.endDialogue()
      }
    } catch (err) {
      console.error('发送消息失败:', err)
      // 模拟AI回复
      this.addMessage({
        isAi: false,
        text: text
      })
      this.addMessage({
        isAi: true,
        text: `Great job! You said: "${text}". Keep practicing!`,
        translation: `说得好！你说的是："${text}"。继续练习！`
      })
      this.setData({
        currentTurn: this.data.currentTurn + 1
      })
    } finally {
      this.setData({ isAiThinking: false })
    }
  },

  onInputChange(e) {
    this.setData({
      inputText: e.detail.value
    })
  },

  onSendText() {
    this.sendTextMessage()
  },

  onPlayAudio(e) {
    const url = e.currentTarget.dataset.url
    this.playAudio(url)
  },

  playAudio(url) {
    if (!url) {
      wx.showToast({
        title: '暂无语音',
        icon: 'none'
      })
      return
    }

    const innerAudioContext = this.data.innerAudioContext
    innerAudioContext.src = url
    innerAudioContext.play()
  },

  addMessage(message) {
    const messages = this.data.messages
    messages.push({
      ...message,
      id: Date.now() + Math.random()
    })
    this.setData({
      messages,
      scrollToId: `msg-${messages.length - 1}`
    })
  },

  async endDialogue() {
    wx.showLoading({ title: '生成报告...' })
    try {
      // 结束对话
      await api.endDialogue(this.data.sessionId)
      // 跳转到报告页
      wx.redirectTo({
        url: `/pages/report/report?sessionId=${this.data.sessionId}`
      })
    } catch (err) {
      console.error('结束对话失败:', err)
      // 直接跳转到报告页
      wx.redirectTo({
        url: `/pages/report/report?sessionId=${this.data.sessionId}`
      })
    } finally {
      wx.hideLoading()
    }
  },

  onEndDialogue() {
    wx.showModal({
      title: '结束对话',
      content: '确定要结束当前对话吗？将生成学习报告。',
      success: (res) => {
        if (res.confirm) {
          this.endDialogue()
        }
      }
    })
  }
})
