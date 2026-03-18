// VitalWatch — Dashboard JS
// Simulates real-time patient data. Replace fetch() calls with real API endpoints.

const PATIENTS = [
  { id:1, name:'James Harlow',   bed:'Bed 1', age:67, ward:'ICU-A', status:'critical',
    vitals:{ hr:128, spo2:88,  sbp:162, dbp:98,  rr:26, temp:38.9 }},
  { id:2, name:'Maria Santos',   bed:'Bed 2', age:54, ward:'ICU-A', status:'warning',
    vitals:{ hr:102, spo2:92,  sbp:148, dbp:90,  rr:22, temp:37.8 }},
  { id:3, name:'Robert Chen',    bed:'Bed 3', age:72, ward:'ICU-A', status:'stable',
    vitals:{ hr:74,  spo2:97,  sbp:118, dbp:76,  rr:16, temp:36.7 }},
  { id:4, name:'Aisha Okonkwo',  bed:'Bed 4', age:45, ward:'ICU-A', status:'stable',
    vitals:{ hr:68,  spo2:98,  sbp:112, dbp:70,  rr:14, temp:36.5 }},
  { id:5, name:'David Reyes',    bed:'Bed 5', age:81, ward:'ICU-A', status:'warning',
    vitals:{ hr:55,  spo2:91,  sbp:155, dbp:94,  rr:20, temp:37.4 }},
  { id:6, name:'Helen Park',     bed:'Bed 6', age:63, ward:'ICU-A', status:'stable',
    vitals:{ hr:80,  spo2:96,  sbp:124, dbp:78,  rr:15, temp:36.8 }},
  { id:7, name:'Thomas Wright',  bed:'Bed 7', age:59, ward:'ICU-A', status:'critical',
    vitals:{ hr:140, spo2:86,  sbp:170, dbp:105, rr:28, temp:39.2 }},
  { id:8, name:'Sofia Andersen', bed:'Bed 8', age:38, ward:'ICU-A', status:'stable',
    vitals:{ hr:72,  spo2:99,  sbp:110, dbp:68,  rr:13, temp:36.6 }},
];

const ALERTS = [
  { type:'critical', icon:'🚨', title:'Bed 1 — HR Critical', desc:'Heart rate 128 bpm (threshold: 120)' },
  { type:'critical', icon:'🚨', title:'Bed 7 — SpO₂ Critical', desc:'Oxygen saturation 86% (threshold: 90%)' },
  { type:'warning',  icon:'⚠️', title:'Bed 2 — BP Elevated',  desc:'Systolic 148 mmHg — monitor closely' },
  { type:'warning',  icon:'⚠️', title:'Bed 5 — HR Low',       desc:'Heart rate 55 bpm (threshold: 60)' },
  { type:'info',     icon:'ℹ️', title:'Bed 3 — Scheduled meds', desc:'Next dose due in 20 minutes' },
];

// Vital alert thresholds
function vitalClass(key, val) {
  const rules = {
    hr:   v => v > 120 || v < 50 ? 'alert' : v > 100 || v < 60 ? 'warn' : '',
    spo2: v => v < 90 ? 'alert' : v < 95 ? 'warn' : '',
    sbp:  v => v > 160 || v < 80 ? 'alert' : v > 140 || v < 90 ? 'warn' : '',
    rr:   v => v > 25 || v < 10 ? 'alert' : v > 20 || v < 12 ? 'warn' : '',
    temp: v => v > 38.5 || v < 35 ? 'alert' : v > 37.3 ? 'warn' : '',
  };
  return rules[key] ? rules[key](val) : '';
}

function renderPatients() {
  const grid = document.getElementById('patientGrid');
  grid.innerHTML = PATIENTS.map(p => {
    const v = p.vitals;
    return `<div class="pt-card ${p.status}" onclick="selectPatient(${p.id})">
      <div class="pt-header">
        <div>
          <div class="pt-name">${p.name}</div>
          <div class="pt-bed">${p.bed} · ${p.age}y · ${p.ward}</div>
        </div>
        <span class="status-badge ${p.status}">${p.status}</span>
      </div>
      <div class="vitals-grid">
        <div class="vital">
          <div class="vital-label">Heart Rate</div>
          <div class="vital-val ${vitalClass('hr',v.hr)}">${v.hr}<span class="vital-unit">bpm</span></div>
        </div>
        <div class="vital">
          <div class="vital-label">SpO₂</div>
          <div class="vital-val ${vitalClass('spo2',v.spo2)}">${v.spo2}<span class="vital-unit">%</span></div>
        </div>
        <div class="vital">
          <div class="vital-label">Blood Pressure</div>
          <div class="vital-val ${vitalClass('sbp',v.sbp)}">${v.sbp}/${v.dbp}<span class="vital-unit">mmHg</span></div>
        </div>
        <div class="vital">
          <div class="vital-label">Resp. Rate</div>
          <div class="vital-val ${vitalClass('rr',v.rr)}">${v.rr}<span class="vital-unit">/min</span></div>
        </div>
        <div class="vital">
          <div class="vital-label">Temperature</div>
          <div class="vital-val ${vitalClass('temp',v.temp)}">${v.temp}<span class="vital-unit">°C</span></div>
        </div>
        <div class="vital">
          <div class="vital-label">Diastolic BP</div>
          <div class="vital-val">${v.dbp}<span class="vital-unit">mmHg</span></div>
        </div>
      </div>
      <div class="pt-time">Updated just now</div>
    </div>`;
  }).join('');
}

function renderAlerts() {
  document.getElementById('alertList').innerHTML = ALERTS.map(a =>
    `<div class="alert-item ${a.type}">
      <div class="alert-icon">${a.icon}</div>
      <div class="alert-body">
        <div class="alert-title">${a.title}</div>
        <div class="alert-desc">${a.desc}</div>
      </div>
    </div>`
  ).join('');
}

// Live simulation — jitter vitals slightly
function jitterVitals() {
  PATIENTS.forEach(p => {
    p.vitals.hr   = Math.max(40, Math.min(180, p.vitals.hr   + (Math.random()-0.5)*4));
    p.vitals.spo2 = Math.max(80, Math.min(100, p.vitals.spo2 + (Math.random()-0.5)*1));
    p.vitals.sbp  = Math.max(70, Math.min(200, p.vitals.sbp  + (Math.random()-0.5)*3));
    p.vitals.rr   = Math.max(8,  Math.min(35,  p.vitals.rr   + (Math.random()-0.5)*1));
    p.vitals.temp = Math.max(34, Math.min(41,  p.vitals.temp + (Math.random()-0.5)*0.1));
    // Round
    p.vitals.hr   = Math.round(p.vitals.hr);
    p.vitals.spo2 = Math.round(p.vitals.spo2);
    p.vitals.sbp  = Math.round(p.vitals.sbp);
    p.vitals.rr   = Math.round(p.vitals.rr);
    p.vitals.temp = Math.round(p.vitals.temp * 10) / 10;
  });
  renderPatients();
}

// Clock
function updateClock() {
  document.getElementById('clock').textContent =
    new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit', second:'2-digit'});
}

// Charts for Bed 4
function initCharts() {
  const labels = Array.from({length:20}, (_,i) => `-${20-i}s`);
  const hrData = Array.from({length:20}, () => 65 + Math.random()*10);
  const spo2Data = Array.from({length:20}, () => 96 + Math.random()*3);

  const cfg = (label, data, color) => ({
    type: 'line',
    data: {
      labels,
      datasets:[{
        label, data, borderColor: color,
        backgroundColor: color.replace(')',', 0.08)').replace('rgb','rgba'),
        borderWidth: 1.5, pointRadius: 0, tension: 0.4, fill: true
      }]
    },
    options:{
      responsive: true, animation: false,
      plugins:{ legend:{ display:false } },
      scales:{
        x:{ grid:{ color:'rgba(255,255,255,0.04)' }, ticks:{ color:'#7d8590', font:{size:9} } },
        y:{ grid:{ color:'rgba(255,255,255,0.04)' }, ticks:{ color:'#7d8590', font:{size:9} } }
      }
    }
  });

  const hrChart   = new Chart(document.getElementById('hrChart'),   cfg('HR',   hrData,   'rgb(248,81,73)'));
  const spo2Chart = new Chart(document.getElementById('spo2Chart'), cfg('SpO₂', spo2Data, 'rgb(56,139,253)'));

  // Push new data every 2s
  setInterval(() => {
    hrChart.data.datasets[0].data.shift();
    hrChart.data.datasets[0].data.push(65 + Math.random()*10);
    hrChart.update('none');
    spo2Chart.data.datasets[0].data.shift();
    spo2Chart.data.datasets[0].data.push(96 + Math.random()*3);
    spo2Chart.update('none');
  }, 2000);
}

function selectPatient(id) {
  // In a full app this would navigate to patient detail page
  console.log('Selected patient', id);
}

// Init
renderPatients();
renderAlerts();
initCharts();
updateClock();
setInterval(updateClock, 1000);
setInterval(jitterVitals, 2000);
