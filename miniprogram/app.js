App({
  globalData: {
    baseUrl: 'http://localhost:8000',
    currentSessionId: null
  },

  onLaunch() {
    // 检查录音权限
    this.checkRecordPermission()
  },

  checkRecordPermission() {
    wx.getSetting({
      success: (res) => {
        if (!res.authSetting['scope.record']) {
          wx.authorize({
            scope: 'scope.record',
            fail() {
              // 如果用户拒绝，提示手动开启
              wx.showModal({
                title: '提示',
                content: '需要录音权限才能使用语音功能，请在设置中开启',
                showCancel: false
              })
            }
          })
        }
      }
    })
  }
})
