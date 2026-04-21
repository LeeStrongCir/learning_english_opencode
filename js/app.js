const app = {
  state: {
    currentView: 'home',
    selectedGrade: null,
    selectedVolume: null,
    selectedUnit: null
  },

  init() {
    this.renderGradeGrid();
    this.bindNavEvents();
    this.bindBreadcrumbEvents();
  },

  bindNavEvents() {
    document.querySelectorAll('.nav-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const view = e.target.dataset.view;
        this.switchView(view);
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
      });
    });
  },

  bindBreadcrumbEvents() {
    document.getElementById('breadcrumb').addEventListener('click', (e) => {
      if (e.target.classList.contains('breadcrumb-item') && e.target.dataset.action) {
        const action = e.target.dataset.action;
        if (action === 'reset') {
          this.resetSelection();
        } else if (action === 'select-volume') {
          this.state.selectedVolume = null;
          this.state.selectedUnit = null;
          this.renderVolumeSelector();
          this.hideContentDisplay();
        }
      }
    });
  },

  switchView(view) {
    document.querySelectorAll('.main > section').forEach(s => s.classList.remove('active'));
    document.getElementById(`${view}-view`).classList.add('active');
    this.state.currentView = view;
    if (view === 'content' && !this.state.selectedGrade) {
      this.showSelectGradeMessage();
    }
  },

  renderGradeGrid() {
    const grid = document.getElementById('grade-grid');
    grid.innerHTML = textbookData.grades.map(grade => `
      <div class="grade-card" data-grade="${grade.id}">
        <span class="emoji">${grade.emoji}</span>
        <span class="label">${grade.name}</span>
      </div>
    `).join('');

    grid.addEventListener('click', (e) => {
      const card = e.target.closest('.grade-card');
      if (card) {
        this.selectGrade(card.dataset.grade);
      }
    });
  },

  selectGrade(gradeId) {
    this.state.selectedGrade = gradeId;
    this.state.selectedVolume = null;
    this.state.selectedUnit = null;

    const grade = textbookData.grades.find(g => g.id === gradeId);
    document.querySelectorAll('.grade-card').forEach(c => c.style.borderColor = 'transparent');
    document.querySelector(`.grade-card[data-grade="${gradeId}"]`).style.borderColor = 'var(--primary)';

    this.switchView('content');
    document.querySelector('.nav-btn[data-view="content"]').classList.add('active');
    document.querySelector('.nav-btn[data-view="home"]').classList.remove('active');

    this.updateBreadcrumb();
    this.renderVolumeSelector();
    this.hideContentDisplay();
  },

  renderVolumeSelector() {
    const container = document.getElementById('volume-selector');
    container.innerHTML = textbookData.volumes.map(vol => `
      <button class="volume-btn" data-volume="${vol.id}">${vol.emoji} ${vol.name}</button>
    `).join('');

    container.addEventListener('click', (e) => {
      if (e.target.classList.contains('volume-btn')) {
        this.selectVolume(e.target.dataset.volume);
      }
    });
  },

  selectVolume(volumeId) {
    this.state.selectedVolume = volumeId;
    this.state.selectedUnit = null;

    document.querySelectorAll('.volume-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`.volume-btn[data-volume="${volumeId}"]`).classList.add('active');

    this.updateBreadcrumb();
    this.renderUnitSelector();
    this.hideContentDisplay();
  },

  renderUnitSelector() {
    const key = `${this.state.selectedGrade}_${this.state.selectedVolume}`;
    const units = textbookData.units[key] || [];
    const container = document.getElementById('unit-selector');

    container.innerHTML = units.map(unit => `
      <button class="unit-btn" data-unit="${unit.id}">${unit.emoji} ${unit.name}</button>
    `).join('');

    container.addEventListener('click', (e) => {
      if (e.target.classList.contains('unit-btn')) {
        this.selectUnit(e.target.dataset.unit);
      }
    });
  },

  selectUnit(unitId) {
    this.state.selectedUnit = unitId;

    document.querySelectorAll('.unit-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`.unit-btn[data-unit="${unitId}"]`).classList.add('active');

    this.updateBreadcrumb();
    this.renderContent();
  },

  updateBreadcrumb() {
    const breadcrumb = document.getElementById('breadcrumb');
    let items = [];

    if (this.state.selectedGrade) {
      const grade = textbookData.grades.find(g => g.id === this.state.selectedGrade);
      items.push(`<span class="breadcrumb-item" data-action="reset">${grade.emoji} ${grade.name}</span>`);
    }

    if (this.state.selectedVolume) {
      const vol = textbookData.volumes.find(v => v.id === this.state.selectedVolume);
      items.push(`<span class="breadcrumb-sep">›</span>`);
      items.push(`<span class="breadcrumb-item" data-action="select-volume">${vol.emoji} ${vol.name}</span>`);
    }

    if (this.state.selectedUnit) {
      const key = `${this.state.selectedGrade}_${this.state.selectedVolume}`;
      const unit = (textbookData.units[key] || []).find(u => u.id === this.state.selectedUnit);
      if (unit) {
        items.push(`<span class="breadcrumb-sep">›</span>`);
        items.push(`<span class="breadcrumb-item active">${unit.emoji} ${unit.name}</span>`);
      }
    }

    breadcrumb.innerHTML = items.join('');
  },

  renderContent() {
    const key = `${this.state.selectedGrade}_${this.state.selectedVolume}`;
    const unit = (textbookData.units[key] || []).find(u => u.id === this.state.selectedUnit);
    if (!unit) return;

    const display = document.getElementById('content-display');
    let html = `<h2>${unit.emoji} ${unit.name}</h2>`;

    html += '<h3 style="margin: 1.5rem 0 1rem; color: var(--primary-dark);">📝 重点词汇</h3>';
    html += '<div class="word-list">';
    unit.words.forEach(w => {
      html += `
        <div class="word-card">
          <div class="english">${w.en}</div>
          <div class="phonetic">${w.phonetic}</div>
          <div class="chinese">${w.cn}</div>
        </div>
      `;
    });
    html += '</div>';

    html += '<h3 style="margin: 1.5rem 0 1rem; color: var(--secondary);">💬 重点句型</h3>';
    html += '<div class="sentence-list">';
    unit.sentences.forEach(s => {
      html += `
        <div class="sentence-card">
          <div class="english">${s.en}</div>
          <div class="chinese">${s.cn}</div>
        </div>
      `;
    });
    html += '</div>';

    html += '<h3 style="margin: 1.5rem 0 1rem; color: var(--accent);">🎭 情景对话</h3>';
    html += '<div class="dialogue-list">';
    unit.dialogues.forEach(d => {
      html += `
        <div class="dialogue-item">
          <div class="dialogue-avatar ${d.avatar}">${d.avatar === 'a' ? '👦' : '👧'}</div>
          <div class="dialogue-content">
            <div class="speaker">${d.speaker === 'A' ? '小明' : '小红'}</div>
            <div class="text">${d.en}</div>
            <div class="translation">${d.cn}</div>
          </div>
        </div>
      `;
    });
    html += '</div>';

    display.innerHTML = html;
    display.style.display = 'block';
  },

  hideContentDisplay() {
    document.getElementById('content-display').style.display = 'none';
  },

  showSelectGradeMessage() {
    const display = document.getElementById('content-display');
    display.innerHTML = '<p style="text-align: center; color: var(--text-light); padding: 3rem;">请先在首页选择一个年级 📚</p>';
    display.style.display = 'block';
  },

  resetSelection() {
    this.state.selectedGrade = null;
    this.state.selectedVolume = null;
    this.state.selectedUnit = null;
    document.querySelectorAll('.grade-card').forEach(c => c.style.borderColor = 'transparent');
    this.switchView('home');
    document.querySelector('.nav-btn[data-view="home"]').classList.add('active');
    document.querySelector('.nav-btn[data-view="content"]').classList.remove('active');
    this.updateBreadcrumb();
  }
};

document.addEventListener('DOMContentLoaded', () => {
  app.init();
});
