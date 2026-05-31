"""
Apply save/load + history integration features from 004 to 001/002/003.
Each page already has code highlighting fixed; this adds the toolbar & JS features.
"""
import re

def patch_file(path, storage_prefix, obj_total, subj_total):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update toolbar: add save-row, change reset text, add history panel floating
    old_toolbar = '''<div class="sticky-toolbar">
    <a href="/" class="back-link">&larr; 返回主页</a>
    <div class="score-bar">
      <div class="score-item"><div class="score-label">客观题</div><div class="score-num"><span id="objDone">0</span>/''' + str(obj_total) + '''</div></div>
      <div class="score-item"><div class="score-label">主观题</div><div class="score-num"><span id="subjDone">0</span>/''' + str(subj_total) + '''</div></div>
      <div class="score-item" id="scoreResult" style="display:none"><div class="score-label">得分</div><div class="score-num"><span id="correctCount">0</span></div></div>
      <button class="score-btn" id="btnSubmit" onclick="submitAll()">提交答案</button>
      <button class="score-btn" style="background:var(--muted)" onclick="resetAll()">重置</button>
    </div>
  </div>

  <div class="history-toggle"><span onclick="toggleHistory()">查看做题记录 ▼</span></div>
  <div class="history-panel" id="historyPanel">'''

    new_toolbar = '''<div class="sticky-toolbar">
    <a href="/" class="back-link">&larr; 返回主页</a>
    <div class="score-bar">
      <div class="score-item"><div class="score-label">客观题</div><div class="score-num"><span id="objDone">0</span>/''' + str(obj_total) + '''</div></div>
      <div class="score-item"><div class="score-label">主观题</div><div class="score-num"><span id="subjDone">0</span>/''' + str(subj_total) + '''</div></div>
      <div class="score-item" id="scoreResult" style="display:none"><div class="score-label">得分</div><div class="score-num"><span id="correctCount">0</span></div></div>
      <div style="flex:1;min-width:0;"></div>
      <div style="display:flex;flex-direction:column;align-items:flex-end;gap:0.35rem;position:relative;">
        <div style="display:flex;gap:0.5rem;">
          <button class="score-btn" id="btnSubmit" onclick="submitAll()">提交答案</button>
          <button class="score-btn" style="background:var(--muted)" onclick="resetAll()">重置进度</button>
        </div>
      </div>
    </div>
    <div style="width:100%;display:flex;align-items:center;justify-content:space-between;padding-top:0.35rem;border-top:1px dashed var(--border);position:relative;">
      <span onclick="toggleHistory()" style="cursor:pointer;font-size:0.78rem;color:var(--sub);user-select:none;">做题记录 <span id="historyToggleIcon">▼</span></span>
      <div style="display:flex;gap:0.5rem;">
        <button class="score-btn" style="background:var(--green)" onclick="saveProgress()">暂存进度</button>
        <button class="score-btn" style="background:var(--purple)" onclick="loadProgress()">加载进度</button>
      </div>
      <div class="history-panel" id="historyPanel">'''

    html = html.replace(old_toolbar, new_toolbar)

    # 2. Update history panel CSS to floating
    html = html.replace(
        '.history-panel { display: none; background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 1rem; margin-bottom: 1.5rem; }',
        '.history-panel { display: none; position: absolute; top: 100%; right: 0; width: 380px; max-width: 90vw; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; margin-top: 0.3rem; box-shadow: 0 8px 24px rgba(0,0,0,0.12); z-index: 300; max-height: 360px; overflow-y: auto; }')

    # 3. Update toggleHistory function
    old_toggle = '''function toggleHistory() {
  const panel = document.getElementById('historyPanel'), toggle = document.querySelector('.history-toggle span');
  panel.classList.toggle('show');
  toggle.textContent = panel.classList.contains('show') ? '收起做题记录 ▲' : '查看做题记录 ▼';
}'''
    new_toggle = '''function toggleHistory() {
  const panel = document.getElementById('historyPanel');
  const icon = document.getElementById('historyToggleIcon');
  panel.classList.toggle('show');
  if (icon) icon.textContent = panel.classList.contains('show') ? '▲' : '▼';
}'''
    html = html.replace(old_toggle, new_toggle)

    # 4. Add save/load JS before toggleDropdown
    SAVE_KEY = storage_prefix + '_saves'
    save_js = '''const SAVE_KEY = \'''' + SAVE_KEY + '''\';

function collectAnswers() {
  const data = {};
  document.querySelectorAll('.card').forEach(card => {
    const qid = card.dataset.qid;
    const type = card.dataset.type;
    if (!qid || !type) return;
    if (type === 'choice') {
      const sel = card.querySelector('.option.selected');
      if (sel) data[qid] = { type, value: sel.dataset.opt };
    } else if (type === 'fill') {
      const inp = card.querySelector('.fill-input');
      if (inp && inp.value.trim()) data[qid] = { type, value: inp.value.trim() };
    } else if (type === 'short') {
      const ta = card.querySelector('.fill-input');
      if (ta && ta.value.trim()) data[qid] = { type, value: ta.value.trim() };
    } else if (type === 'write') {
      const ed = card.querySelector('.code-editor');
      if (ed && ed.value.trim()) data[qid] = { type, value: ed.value.trim() };
    }
  });
  return data;
}

function restoreAnswers(data) {
  submitted = false;
  scores = {};
  document.querySelectorAll('.card').forEach(card => {
    card.classList.remove('submitted','correct','wrong');
    card.querySelectorAll('.option').forEach(o => o.classList.remove('selected','correct-option','wrong-option'));
    const fb = card.querySelector('.feedback');
    if (fb) { fb.classList.remove('show','correct-fb','wrong-fb'); const ca=fb.querySelector('.correct-answer'); if(ca) ca.remove(); }
    const blank = card.querySelector('.blank');
    if (blank) { blank.classList.remove('correct-fill','wrong-fill','filled'); blank.textContent=''; }
    const inp = card.querySelector('.fill-input');
    if (inp) { inp.value=''; inp.disabled=false; }
    const ce = card.querySelector('.code-editor');
    if (ce) { ce.value=''; ce.disabled=false; }
  });
  document.getElementById('scoreResult').style.display = 'none';
  document.getElementById('btnSubmit').disabled = false;
  setTimeout(() => {
    document.querySelectorAll('.card').forEach(card => {
      const qid = card.dataset.qid;
      const type = card.dataset.type;
      if (!qid || !data[qid]) return;
      const d = data[qid];
      if (d.type === 'choice') {
        const opt = card.querySelector('.option[data-opt="' + d.value + '"]');
        if (opt) selectOption(opt);
      } else if (d.type === 'fill') {
        const inp = card.querySelector('.fill-input');
        if (inp) { inp.value = d.value; inp.dispatchEvent(new Event('input')); }
      } else if (d.type === 'short') {
        const ta = card.querySelector('.fill-input');
        if (ta) { ta.value = d.value; ta.dispatchEvent(new Event('input')); }
      } else if (d.type === 'write') {
        const ed = card.querySelector('.code-editor');
        if (ed) { ed.value = d.value; ed.dispatchEvent(new Event('input')); }
      }
    });
    updateProgress();
    showToast('进度已恢复');
  }, 50);
}

function saveProgress() {
  const name = prompt('请输入存档名称：', '存档 ' + new Date().toLocaleDateString());
  if (!name) return;
  const data = collectAnswers();
  const saves = JSON.parse(localStorage.getItem(SAVE_KEY) || '{}');
  saves[name] = { time: Date.now(), data };
  localStorage.setItem(SAVE_KEY, JSON.stringify(saves));
  showToast('已保存：' + name);
}

function loadProgress() {
  const saves = JSON.parse(localStorage.getItem(SAVE_KEY) || '{}');
  const names = Object.keys(saves).sort((a, b) => saves[b].time - saves[a].time);
  if (names.length === 0) { showToast('没有已保存的进度'); return; }
  let msg = '选择一个存档加载：\\n\\n';
  names.forEach((n, i) => {
    msg += (i+1) + '. ' + n + ' (' + new Date(saves[n].time).toLocaleString() + ')\\n';
  });
  msg += '\\n输入编号或名称：';
  const choice = prompt(msg);
  if (!choice) return;
  let key = null;
  const idx = parseInt(choice);
  if (idx >= 1 && idx <= names.length) {
    key = names[idx - 1];
  } else if (names.includes(choice)) {
    key = choice;
  }
  if (!key) { showToast('未找到该存档'); return; }
  restoreAnswers(saves[key].data);
  showToast('已加载：' + key);
}

function loadHistoryRecord(index) {
  const records = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  if (index < 0 || index >= records.length) return;
  const r = records[index];
  if (!confirm('加载「' + r.date + '」的答案到页面？当前进度将被覆盖。')) return;
  const data = {};
  const answers = r.answers || {};
  Object.keys(answers).forEach(qid => {
    const a = answers[qid];
    if (a.type === 'choice') data[qid] = { type: 'choice', value: a.userAnswer };
    else if (a.type === 'fill') data[qid] = { type: 'fill', value: a.userAnswer };
    else if (a.type === 'short') data[qid] = { type: 'short', value: a.userAnswer };
    else if (a.type === 'write') data[qid] = { type: 'write', value: a.userAnswer };
  });
  restoreAnswers(data);
  document.getElementById('historyModal').classList.remove('show');
}

'''

    html = html.replace('function toggleDropdown(btn) {', save_js + 'function toggleDropdown(btn) {')

    # 5. Add auto-save on submit (after saveRecord call)
    old_save = 'saveRecord(correct, total, userAnswers);'
    auto_save = '''saveRecord(correct, total, userAnswers);
  const now = new Date();
  const autoName = '提交 ' + String(now.getHours()).padStart(2,'0')+':'+String(now.getMinutes()).padStart(2,'0') + ' — ' + correct + '/' + total;
  const saves = JSON.parse(localStorage.getItem(SAVE_KEY) || '{}');
  saves[autoName] = { time: Date.now(), data: collectAnswers(), score: correct + '/' + total };
  localStorage.setItem(SAVE_KEY, JSON.stringify(saves));'''
    html = html.replace(old_save, auto_save)

    # 6. Add "加载此答案" button in history detail
    old_detail = 'let html = `<div class="history-detail-info">📅 ${r.date} &nbsp; 得分：<b>${r.correct}/${r.total}</b>（${r.percent}%）</div>`;'
    new_detail = 'let html = `<div class="history-detail-info">📅 ${r.date} &nbsp; 得分：<b>${r.correct}/${r.total}</b>（${r.percent}%） &nbsp; <button onclick="loadHistoryRecord(${index})" style="background:var(--purple);color:#fff;border:none;padding:0.25rem 0.75rem;border-radius:4px;font-size:0.75rem;cursor:pointer;font-family:inherit;">加载此答案到页面</button></div>`;'
    html = html.replace(old_detail, new_detail)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'Patched: {path.split(chr(92))[-1]}')
    print(f'  SAVE_KEY: {SAVE_KEY}')
    return True

# Patch all three
patch_file(r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_001.html', 'py_day01', 20, 18)
patch_file(r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_002.html', 'py_day02', 20, 18)
patch_file(r'E:\AI_itheima\VS_code\my_blog\static\python_basic_test_003.html', 'py_day03', 20, 14)
print('All done')
