/* ====== Quiz Engine — Common JS for all quiz pages ====== */

let scores = {};
let submitted = false;

function selectOption(opt) {
  if (submitted) return;
  const card = opt.closest('.card');
  card.querySelectorAll('.option').forEach(o => o.classList.remove('selected'));
  opt.classList.add('selected');
  updateProgress();
}

function updateProgress() {
  var obj = 0, subj = 0;
  document.querySelectorAll('.card').forEach(function(card) {
    var t = card.dataset.type;
    if (t === 'choice') { if (card.querySelector('.option.selected')) obj++; }
    else if (t === 'fill') {
      var inps = card.querySelectorAll('.blank-input');
      var filled = true;
      inps.forEach(function(inp) { if (!inp.value.trim()) filled = false; });
      if (filled) obj++;
    }
    else if (t === 'short') { var ta = card.querySelector('.fill-input'); if (ta && ta.value.trim()) subj++; }
    else if (t === 'write') { var ed = card.querySelector('.code-editor'); if (ed && ed.value.trim()) subj++; }
  });
  document.getElementById('objDone').textContent = obj;
  document.getElementById('subjDone').textContent = subj;
}

function toggleRef(el) {
  const ref = el.nextElementSibling;
  ref.classList.toggle('show');
  el.textContent = ref.classList.contains('show') ? '收起参考答案 ▲' : '查看参考答案 ▼';
}

function submitAll() {
  if (submitted) { showToast('已提交过，请先重置'); return; }
  let unanswered = 0;
  document.querySelectorAll('.card').forEach(card => {
    const t = card.dataset.type;
    if (t === 'choice') { if (!card.querySelector('.option.selected')) unanswered++; }
    else if (t === 'fill') {
      const inps = card.querySelectorAll('.blank-input');
      let allFilled = true;
      inps.forEach(function(inp) { if (!inp.value.trim()) allFilled = false; });
      if (!allFilled) unanswered++;
    }
  });
  let msg = '确定要提交答案吗？提交后将无法修改。\n\n📝 简答题和代码实战题为主观题，不参与计分，请自行对照参考答案。';
  if (unanswered > 0) msg += `\n\n⚠️ 还有 ${unanswered} 道选择题/填空题未作答。`;
  if (!confirm(msg)) return;
  let correct = 0, total = 0;
  const userAnswers = {};
  document.querySelectorAll('.card').forEach(card => {
    const qid = card.dataset.qid, type = card.dataset.type, answer = card.dataset.answer;
    if (type === 'choice' || type === 'fill') total++;
    if (type === 'choice') {
      const sel = card.querySelector('.option.selected');
      const isCorrect = sel && sel.dataset.opt === answer;
      if (isCorrect) correct++; scores[qid] = isCorrect;
      userAnswers[qid] = { type: 'choice', userAnswer: sel ? sel.dataset.opt : '', correctAnswer: answer, isCorrect };
      card.classList.add('submitted');
      card.querySelectorAll('.option').forEach(o => {
        if (o.dataset.opt === answer) o.classList.add('correct-option');
        if (o === sel && !isCorrect) o.classList.add('wrong-option');
      });
      const fb = card.querySelector('.feedback'), tag = fb.querySelector('.result-tag');
      if (isCorrect) { card.classList.add('correct'); fb.classList.add('correct-fb','show'); tag.className='result-tag correct-tag'; tag.textContent='✓ 正确'; }
      else { card.classList.add('wrong'); fb.classList.add('wrong-fb','show'); tag.className='result-tag wrong-tag'; tag.textContent = sel ? '✗ 错误' : '— 未作答'; }
    } else if (type === 'fill') {
      const inps = card.querySelectorAll('.blank-input');
      let uaParts = [];
      inps.forEach(function(inp) { uaParts.push(inp.value.trim()); });
      const ua = uaParts.join('、');
      const isCorrect = normalize(ua) === normalize(answer);
      if (isCorrect) correct++; scores[qid] = isCorrect;
      userAnswers[qid] = { type: 'fill', userAnswer: ua, correctAnswer: answer, isCorrect };
      card.classList.add('submitted');
      inps.forEach(function(inp) { inp.disabled = true; });
      const fb = card.querySelector('.feedback'), tag = fb.querySelector('.result-tag');
      if (isCorrect) { card.classList.add('correct'); inps.forEach(function(inp) { inp.classList.add('correct-fill'); }); fb.classList.add('correct-fb','show'); tag.className='result-tag correct-tag'; tag.textContent='✓ 正确'; }
      else { card.classList.add('wrong');
        inps.forEach(function(inp) { if (!inp.value.trim()) { inp.classList.add('wrong-fill'); inp.value='(空)'; } else { inp.classList.add('wrong-fill'); } });
        fb.classList.add('wrong-fb','show'); tag.className='result-tag wrong-tag'; tag.textContent = ua ? '✗ 错误' : '— 未作答';
        const ans=document.createElement('div'); ans.className='correct-answer'; ans.style.cssText='margin-top:0.4rem;color:var(--green)'; ans.textContent=`正确答案：${answer}`; fb.appendChild(ans); }
    } else if (type === 'short') {
      const input = card.querySelector('.fill-input');
      card.classList.add('submitted'); if (input) input.disabled = true;
      scores[qid] = null;
      userAnswers[qid] = { type: 'short', userAnswer: input ? input.value.trim() : '', isCorrect: null };
      const fb = card.querySelector('.feedback'); fb.classList.add('correct-fb','show');
      fb.querySelector('.result-tag').className='result-tag correct-tag';
      fb.querySelector('.result-tag').textContent='📝 主观题 · 自行核对';
    } else if (type === 'write') {
      const editor = card.querySelector('.code-editor');
      if (editor) editor.disabled = true;
      scores[qid] = null;
      userAnswers[qid] = { type: 'write', userAnswer: editor ? editor.value : '', isCorrect: null };
      card.classList.add('submitted');
      const fb = card.querySelector('.feedback');
      if (!fb) {
        const div = document.createElement('div'); div.className = 'feedback correct-fb show';
        div.innerHTML = '<div class="result-tag correct-tag">📝 主观题 · 自行核对</div>请对照参考答案检查你的代码。';
        card.appendChild(div);
      }
    }
  });
  submitted = true;
  const btn = document.getElementById('btnSubmit');
  btn.disabled = true; btn.style.opacity = '0.5'; btn.style.cursor = 'not-allowed';
  document.getElementById('correctCount').textContent = correct + '/' + total;
  document.getElementById('scoreResult').style.display = '';
  showToast(`客观题得分：${correct}/${total}（${Math.round(correct/total*100)}%）`);

  // Auto-save to progress
  saveRecord(correct, total, userAnswers);
  const now = new Date();
  const autoName = '提交 ' + String(now.getHours()).padStart(2,'0')+':'+String(now.getMinutes()).padStart(2,'0') + ' — ' + correct + '/' + total;
  const saves = JSON.parse(localStorage.getItem(SAVE_KEY) || '{}');
  saves[autoName] = { time: Date.now(), data: collectAnswers(), score: correct + '/' + total };
  localStorage.setItem(SAVE_KEY, JSON.stringify(saves));
}

function resetAll() {
  if (submitted && !confirm('确定要重置吗？当前答案将被清除。')) return;
  submitted = false; scores = {};
  document.querySelectorAll('.card').forEach(card => {
    card.classList.remove('submitted','correct','wrong');
    card.querySelectorAll('.option').forEach(o => o.classList.remove('selected','correct-option','wrong-option'));
    const fb = card.querySelector('.feedback');
    if (fb) { fb.classList.remove('show','correct-fb','wrong-fb'); const ca=fb.querySelector('.correct-answer'); if(ca) ca.remove(); }
    const fillInps = card.querySelectorAll('.blank-input');
    fillInps.forEach(function(inp) { inp.classList.remove('correct-fill','wrong-fill','filled'); inp.value=''; inp.disabled=false; });
    const input = card.querySelector('.fill-input');
    if (input) { input.value=''; input.disabled=false; }
    const editor = card.querySelector('.code-editor');
    if (editor) { editor.value=''; editor.disabled=false; }
    const ref = card.querySelector('.ref-answer');
    if (ref) ref.classList.remove('show');
    const refToggle = card.querySelector('.ref-toggle');
    if (refToggle) refToggle.textContent = '查看参考答案 ▼';
  });
  scores={}; submitted=false;
  const btn = document.getElementById('btnSubmit');
  btn.disabled=false; btn.style.opacity='1'; btn.style.cursor='pointer';
  document.getElementById('scoreResult').style.display='none';
  updateProgress();
  showToast('已全部重置');
}

// ====== History ======

function saveRecord(correct, total, userAnswers) {
  const records = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  const now = new Date();
  const date = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')} ${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;
  records.unshift({ date, correct, total, percent: Math.round(correct/total*100), answers: userAnswers });
  if (records.length > 30) records.length = 30;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(records));
  renderHistory();
}

function renderHistory() {
  const records = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  const list = document.getElementById('historyList'), empty = document.getElementById('historyEmpty');
  list.innerHTML = '';
  if (records.length === 0) { empty.style.display = 'block'; return; }
  empty.style.display = 'none';
  records.forEach((r, i) => {
    const li = document.createElement('li'); li.className = 'history-item';
    const cls = r.percent >= 80 ? 'high' : (r.percent >= 60 ? 'mid' : 'low');
    li.innerHTML = `<span class="history-date">${r.date}</span><span class="history-score ${cls}">${r.correct}/${r.total}（${r.percent}%）</span>`;
    li.onclick = function() { showHistoryDetail(i); };
    list.appendChild(li);
  });
}

function toggleHistory() {
  const panel = document.getElementById('historyPanel');
  const icon = document.getElementById('historyToggleIcon');
  panel.classList.toggle('show');
  if (icon) icon.textContent = panel.classList.contains('show') ? '▲' : '▼';
}

function clearHistory() {
  if (confirm('确定要清空所有做题记录吗？此操作不可恢复。')) { localStorage.removeItem(STORAGE_KEY); renderHistory(); showToast('记录已清空'); }
}

function showHistoryDetail(index) {
  const records = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  if (index < 0 || index >= records.length) return;
  const r = records[index];
  const body = document.getElementById('historyDetailBody');
  const answers = r.answers || {};
  let html = `<div class="history-detail-info">📅 ${r.date} &nbsp; 得分：<b>${r.correct}/${r.total}</b>（${r.percent}%） &nbsp; <button onclick="loadHistoryRecord(${index})" style="background:var(--purple);color:#fff;border:none;padding:0.25rem 0.75rem;border-radius:4px;font-size:0.75rem;cursor:pointer;font-family:inherit;">加载此答案到页面</button></div>`;
  const qids = Object.keys(answers).sort((a,b) => parseInt(a)-parseInt(b));
  qids.forEach(qid => {
    const a = answers[qid];
    if (!a) return;
    html += `<div class="history-detail-q">`;
    html += `<span class="dq-num">Q${qid}</span>`;
    if (a.isCorrect === true) html += `<span class="dq-badge correct">✓ 正确</span>`;
    else if (a.isCorrect === false) html += `<span class="dq-badge wrong">✗ 错误</span>`;
    else if (a.isCorrect === null) html += `<span class="dq-badge subj">📝 主观题</span>`;
    if (a.type === 'choice') {
      html += `<span class="dq-label">你的答案：<b>${a.userAnswer || '(未作答)'}</b></span>`;
      if (a.isCorrect === false) html += `<span class="dq-correct-ans"> / 正确答案：<b>${a.correctAnswer}</b></span>`;
    } else if (a.type === 'fill') {
      html += `<span class="dq-label">你的答案：<b>${a.userAnswer || '(空)'}</b></span>`;
      if (a.isCorrect === false) html += `<span class="dq-correct-ans"> / 正确答案：<b>${a.correctAnswer}</b></span>`;
    } else if (a.type === 'short') {
      html += `<div class="dq-user" style="margin-top:0.2rem;">你的回答：${a.userAnswer || '(未作答)'}</div>`;
    } else if (a.type === 'write') {
      html += `<div class="dq-user" style="margin-top:0.2rem;font-family:'JetBrains Mono',monospace;font-size:0.78rem;white-space:pre-wrap;">${a.userAnswer || '(未作答)'}</div>`;
    }
    html += `</div>`;
  });
  body.innerHTML = html;
  document.getElementById('historyDetailOverlay').classList.add('show');
}

function closeHistoryDetail() {
  document.getElementById('historyDetailOverlay').classList.remove('show');
}

function loadHistoryRecord(index) {
  const records = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  if (index < 0 || index >= records.length) return;
  const r = records[index];
  if (!confirm(`加载「${r.date}」的答案到页面？当前进度将被覆盖。`)) return;
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
  document.getElementById('historyDetailOverlay').classList.remove('show');
}

// ====== Save/Load ======

function collectAnswers() {
  const data = {};
  document.querySelectorAll('.card').forEach(card => {
    const qid = card.dataset.qid, type = card.dataset.type;
    if (!qid || !type) return;
    if (type === 'choice') { const sel = card.querySelector('.option.selected'); if (sel) data[qid] = { type, value: sel.dataset.opt }; }
    else if (type === 'fill') {
      const inps = card.querySelectorAll('.blank-input');
      let parts = [];
      inps.forEach(function(inp) { parts.push(inp.value.trim()); });
      const val = parts.join('、');
      if (val) data[qid] = { type, value: val };
    }
    else if (type === 'short') { const ta = card.querySelector('.fill-input'); if (ta && ta.value.trim()) data[qid] = { type, value: ta.value.trim() }; }
    else if (type === 'write') { const ed = card.querySelector('.code-editor'); if (ed && ed.value.trim()) data[qid] = { type, value: ed.value.trim() }; }
  });
  return data;
}

function restoreAnswers(data) {
  submitted = false; scores = {};
  document.querySelectorAll('.card').forEach(card => {
    card.classList.remove('submitted','correct','wrong');
    card.querySelectorAll('.option').forEach(o => o.classList.remove('selected','correct-option','wrong-option'));
    const fb = card.querySelector('.feedback');
    if (fb) { fb.classList.remove('show','correct-fb','wrong-fb'); const ca=fb.querySelector('.correct-answer'); if(ca) ca.remove(); }
    const fillInps = card.querySelectorAll('.blank-input');
    fillInps.forEach(function(inp) { inp.classList.remove('correct-fill','wrong-fill','filled'); inp.value=''; });
    const inp = card.querySelector('.fill-input'); if (inp) { inp.value=''; inp.disabled=false; }
    const ce = card.querySelector('.code-editor'); if (ce) { ce.value=''; ce.disabled=false; }
  });
  document.getElementById('scoreResult').style.display = 'none';
  document.getElementById('btnSubmit').disabled = false;
  setTimeout(() => {
    document.querySelectorAll('.card').forEach(card => {
      const qid = card.dataset.qid, type = card.dataset.type;
      if (!qid || !data[qid]) return;
      const d = data[qid];
      if (d.type === 'choice') { const opt = card.querySelector(`.option[data-opt="${d.value}"]`); if (opt) selectOption(opt); }
      else if (d.type === 'fill') {
        const inps = card.querySelectorAll('.blank-input');
        var parts = d.value.split('、');
        inps.forEach(function(inp, idx) { if (idx < parts.length) { inp.value = parts[idx]; inp.classList.toggle('filled', parts[idx].length > 0); } });
      }
      else if (d.type === 'short') { const ta = card.querySelector('.fill-input'); if (ta) { ta.value = d.value; ta.dispatchEvent(new Event('input')); } }
      else if (d.type === 'write') { const ed = card.querySelector('.code-editor'); if (ed) { ed.value = d.value; ed.dispatchEvent(new Event('input')); } }
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
  let msg = '选择一个存档加载：\n\n';
  names.forEach((n, i) => { msg += (i+1) + '. ' + n + ' (' + new Date(saves[n].time).toLocaleString() + ')\n'; });
  msg += '\n输入编号或名称：';
  const choice = prompt(msg);
  if (!choice) return;
  let key = null;
  const idx = parseInt(choice);
  if (idx >= 1 && idx <= names.length) key = names[idx - 1];
  else if (names.includes(choice)) key = choice;
  if (!key) { showToast('未找到该存档'); return; }
  restoreAnswers(saves[key].data);
  showToast('已加载：' + key);
}

// ====== Export / Import ======

function exportProgress() {
  const saves = JSON.parse(localStorage.getItem(SAVE_KEY) || '{}');
  const records = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  const exportData = {
    version: 1,
    exportedAt: new Date().toISOString(),
    saves,
    records
  };
  const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'quiz_progress_' + new Date().toISOString().slice(0, 10) + '.json';
  a.click();
  URL.revokeObjectURL(url);
  showToast('数据已导出');
}

function importProgress() {
  document.getElementById('importFileInput').click();
}

function handleImportFile(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      const data = JSON.parse(e.target.result);
      if (!data.version || !data.saves) {
        showToast('文件格式不正确');
        return;
      }
      if (confirm('导入将覆盖现有的暂存存档和做题记录，是否继续？')) {
        localStorage.setItem(SAVE_KEY, JSON.stringify(data.saves));
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data.records || []));
        renderHistory();
        showToast('数据已导入（共 ' + Object.keys(data.saves).length + ' 个存档）');
      }
    } catch (err) {
      showToast('文件读取失败：' + err.message);
    }
  };
  reader.readAsText(file);
  event.target.value = '';
}

// ====== UI Helpers ======

function showToast(msg) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div'); toast.id = 'toast'; toast.className = 'toast';
    document.body.appendChild(toast);
  }
  toast.textContent = msg; toast.classList.add('show');
  clearTimeout(toast._t); toast._t = setTimeout(() => toast.classList.remove('show'), 2500);
}

function normalize(s) {
  return s.replace(/\s+/g,'').replace(/[（）\(\)]/g,'()').replace(/[；;]/g,',').replace(/[。.]/g,'').toLowerCase();
}

function toggleDropdown(btn) {
  var dd = btn.parentElement;
  dd.classList.toggle('open');
}

document.addEventListener('click', function(e) {
  if (!e.target.closest('.quiz-dropdown')) {
    document.querySelectorAll('.quiz-dropdown.open').forEach(function(dd) { dd.classList.remove('open'); });
  }
});

// ====== Keyboard shortcuts ======
document.addEventListener('keydown', function(e) {
  // Skip if user is typing in an input/textarea
  const tag = e.target.tagName;
  if (tag === 'INPUT' || tag === 'TEXTAREA' || e.target.contentEditable === 'true') return;

  if (e.key === 'j' || e.key === 'J' || e.key === 'ArrowDown') {
    // Next question
    const current = document.querySelector('.card:focus');
    const cards = Array.from(document.querySelectorAll('.card[data-qid]'));
    const idx = current ? cards.indexOf(current) : -1;
    if (idx < cards.length - 1) {
      cards[idx + 1].scrollIntoView({ behavior: 'smooth', block: 'start' });
      cards[idx + 1].setAttribute('tabindex', '-1');
      cards[idx + 1].focus();
    }
  } else if (e.key === 'k' || e.key === 'K' || e.key === 'ArrowUp') {
    // Previous question
    const current = document.querySelector('.card:focus');
    const cards = Array.from(document.querySelectorAll('.card[data-qid]'));
    const idx = current ? cards.indexOf(current) : 0;
    if (idx > 0) {
      cards[idx - 1].scrollIntoView({ behavior: 'smooth', block: 'start' });
      cards[idx - 1].setAttribute('tabindex', '-1');
      cards[idx - 1].focus();
    }
  } else if (e.key === 'Escape') {
    closeHistoryDetail();
  }
});

// ====== Auto-expand code editor & blank input ======
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.code-editor').forEach(function(editor) {
    // Auto-expand height based on content
    function resizeEditor() {
      editor.style.height = 'auto';
      editor.style.height = editor.scrollHeight + 'px';
    }

    editor.addEventListener('input', resizeEditor);
    editor.addEventListener('keydown', function(e) {
      if (e.key === 'Tab' && !submitted) {
        e.preventDefault();
        const start = editor.selectionStart, end = editor.selectionEnd;
        editor.value = editor.value.substring(0, start) + '    ' + editor.value.substring(end);
        editor.selectionStart = editor.selectionEnd = start + 4;
        resizeEditor();
        updateProgress();
      }
    });
    setTimeout(resizeEditor, 50);
  });

  // Track blank fill state
  document.querySelectorAll('.blank-input').forEach(function(inp) {
    inp.addEventListener('input', function() {
      this.classList.toggle('filled', this.value.trim().length > 0);
      updateProgress();
    });
  });

  updateProgress();
  renderHistory();
});
