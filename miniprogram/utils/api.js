const app = getApp()

/**
 * 封装HTTP请求
 * @param {string} method - HTTP方法
 * @param {string} path - 请求路径
 * @param {object} data - 请求数据
 * @returns {Promise}
 */
function request(method, path, data) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${app.globalData.baseUrl}${path}`,
      method,
      data,
      header: { 'Content-Type': 'application/json' },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data)
        } else {
          reject(res.data)
        }
      },
      fail: (err) => reject(err)
    })
  })
}

/**
 * 上传文件（用于语音文件）
 * @param {string} filePath - 文件路径
 * @param {object} formData - 额外表单数据
 * @returns {Promise}
 */
function uploadFile(filePath, formData = {}) {
  return new Promise((resolve, reject) => {
    wx.uploadFile({
      url: `${app.globalData.baseUrl}/api/upload`,
      filePath,
      name: 'file',
      formData,
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(JSON.parse(res.data))
        } else {
          reject(res.data)
        }
      },
      fail: (err) => reject(err)
    })
  })
}

module.exports = {
  // 对话相关
  startDialogue(data) {
    return request('POST', '/api/dialogue/start', data)
  },
  sendTurn(data) {
    return request('POST', '/api/dialogue/turn', data)
  },
  endDialogue(sessionId) {
    return request('POST', `/api/dialogue/${sessionId}/end`, {})
  },
  getDialogueHistory(sessionId) {
    return request('GET', `/api/dialogue/${sessionId}`, {})
  },

  // 报告相关
  getReport(sessionId) {
    return request('GET', `/api/report/${sessionId}`, {})
  },

  // 教材相关
  getTextbook() {
    return request('GET', '/api/textbook', {})
  },

  // 上传语音
  uploadVoice(filePath) {
    return uploadFile(filePath, { type: 'voice' })
  }
}
