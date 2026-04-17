Component({
  properties: {
    message: {
      type: Object,
      value: {}
    },
    isAi: {
      type: Boolean,
      value: true
    }
  },

  methods: {
    onPlayTap() {
      this.triggerEvent('play', { url: this.data.message.audioUrl })
    }
  }
})
