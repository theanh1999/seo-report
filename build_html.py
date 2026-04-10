import json

# Load compact history data
with open('/sessions/admiring-hopeful-wozniak/history_compact.json', 'r') as f:
    embedded_data = f.read()

html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SEO Index Analysis Dashboard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0f172a;color:#f1f5f9;padding:20px;min-height:100vh}
.container{max-width:1400px;margin:0 auto}
header{margin-bottom:24px}
h1{font-size:28px;font-weight:700;margin-bottom:6px}
.subtitle{color:#94a3b8;font-size:13px}
.controls{display:flex;gap:16px;margin-top:16px;flex-wrap:wrap;align-items:center}
.control-group{display:flex;gap:6px;align-items:center}
.control-label{color:#94a3b8;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.5px;margin-right:4px}
.btn{padding:7px 14px;border:1px solid #334155;background:#1e293b;color:#e2e8f0;border-radius:6px;cursor:pointer;font-size:13px;font-weight:500;transition:all .15s}
.btn:hover{background:#334155;border-color:#475569}
.btn.active{background:#3b82f6;border-color:#3b82f6;color:#fff}
.card{background:#1e293b;border:1px solid #334155;border-radius:10px;padding:20px;margin-bottom:20px}
.card-title{font-size:15px;font-weight:600;margin-bottom:14px;color:#e2e8f0}
.chart-wrap{position:relative;width:100%;height:340px}
.chart-wrap canvas{width:100%!important;height:100%!important}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px}
@media(max-width:900px){.grid-2{grid-template-columns:1fr}}
.stats-row{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px}
.stat-box{background:#0f172a;border:1px solid #334155;border-radius:8px;padding:14px 18px;min-width:140px;flex:1}
.stat-val{font-size:22px;font-weight:700;color:#f1f5f9}
.stat-lbl{font-size:11px;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px;margin-top:2px}
.tabs{display:flex;gap:0;border-bottom:2px solid #334155;margin-bottom:20px;overflow-x:auto}
.tab{padding:10px 18px;background:transparent;border:none;color:#94a3b8;cursor:pointer;font-size:14px;font-weight:500;border-bottom:3px solid transparent;margin-bottom:-2px;white-space:nowrap;transition:all .15s}
.tab:hover{color:#f1f5f9}
.tab.active{color:#f1f5f9;border-bottom-color:#3b82f6}
.tab-panel{display:none}
.tab-panel.active{display:block}
.group-hdr{font-size:18px;font-weight:600;margin-bottom:14px;padding-bottom:8px;border-bottom:2px solid #334155;display:flex;align-items:center;gap:8px}
.dot{width:10px;height:10px;border-radius:3px;display:inline-block}
.domain-card{background:#0f172a;border:1px solid #334155;border-radius:8px;padding:16px;margin-bottom:14px}
.domain-name{font-size:14px;font-weight:600;margin-bottom:8px}
.domain-stats{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:10px}
.d-stat-val{font-size:15px;font-weight:700}
.d-stat-lbl{font-size:10px;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px}
.mini-wrap{position:relative;height:100px;margin-bottom:4px}
.mini-wrap canvas{width:100%!important;height:100%!important}
.pos{color:#22c55e}.neg{color:#ef4444}.muted{color:#64748b}
.doughnut-wrap{position:relative;height:260px;max-width:380px;margin:0 auto}
.doughnut-wrap canvas{width:100%!important;height:100%!important}
.growth-wrap{position:relative;height:280px}
.growth-wrap canvas{width:100%!important;height:100%!important}
table{width:100%;border-collapse:collapse;margin-top:10px}
th{background:#0f172a;border:1px solid #334155;padding:10px 12px;text-align:left;font-size:11px;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px}
td{border:1px solid #334155;padding:10px 12px;font-size:13px}
tr:hover{background:rgba(59,130,246,.05)}
</style>
</head>
<body>
<div class="container">
<header>
<h1>SEO Index Analysis Dashboard</h1>
<p class="subtitle" id="lastUpdated">Loading...</p>
<div class="controls">
<div class="control-group">
<span class="control-label">Period:</span>
<button class="btn time-btn active" data-days="0">All</button>
<button class="btn time-btn" data-days="30">30d</button>
<button class="btn time-btn" data-days="60">60d</button>
<button class="btn time-btn" data-days="90">90d</button>
<button class="btn time-btn" data-days="180">6m</button>
</div>
</div>
</header>

<div id="kpi-row" class="stats-row"></div>

<div class="card">
<div class="card-title">Overview — Group Totals Over Time</div>
<div class="chart-wrap"><canvas id="overviewChart"></canvas></div>
</div>

<div class="tabs" id="tabBar">
<button class="tab active" data-tab="all">All Groups</button>
<button class="tab" data-tab="nha_hang">Nhà Hàng</button>
<button class="tab" data-tab="hotel">Hotel</button>
<button class="tab" data-tab="doi_thu">Đối Thủ</button>
</div>

<div id="panel-all" class="tab-panel active"></div>
<div id="panel-nha_hang" class="tab-panel"></div>
<div id="panel-hotel" class="tab-panel"></div>
<div id="panel-doi_thu" class="tab-panel"></div>

<div class="card">
<div class="card-title">Growth Ranking</div>
<div style="overflow-x:auto">
<table><thead><tr><th>#</th><th>Domain</th><th>Group</th><th>Current</th><th>vs Hôm qua</th><th>vs 7 ngày</th><th>vs 14 ngày</th><th>vs 30 ngày</th></tr></thead><tbody id="growthBody"></tbody></table>
</div>
</div>
</div>

<script>
// ===== EMBEDDED DATA =====
var EMBEDDED_DATA = ''' + embedded_data + ''';

// ===== CONFIG =====
var SITE_GROUPS = {
    nha_hang: ["goto-where.com","menu-world.com","grubbio.com","menustic.com","menufyy.com","res-menu.net","restaurants-world.net","wherevi.com","localoria.com","placejoys.com","wherebly.com","foodplacee.com","locallya.com"],
    hotel: ["gohotelly.com"],
    doi_thu: ["wheree.com","www.wheree.com","com-cuisine.com","com-fnb.com","com-place.com","goto-restaurants.com","wanderlog.com","menu-res.com","restaurantmenu.us.com","com-hotel.com","gotoeat.net","restaurants-info.com","hey-restaurants.com","nearby-res.com","res-pick.com","uk-restaurants.com","weeblyte.com","com-bistro.com","eaterygrid.com","taste-pick.com","pressupeats.com"]
};
var GROUP_LABELS = {nha_hang:"Nhà Hàng",hotel:"Hotel",doi_thu:"Đối Thủ"};
var GROUP_COLORS = {nha_hang:"#22c55e",hotel:"#a855f7",doi_thu:"#ef4444"};
var PALETTE = ["#3b82f6","#22c55e","#ef4444","#eab308","#a855f7","#06b6d4","#f97316","#ec4899","#8b5cf6","#14b8a6","#f43f5e","#84cc16","#0ea5e9"];

// ===== STATE =====
var allData = [];
var filtered = [];
var timeDays = 0;
var activeTab = "all";
var charts = {};

// ===== LOAD DATA =====
function loadData() {
    return fetch("history.json").then(function(r) {
        if (r.ok) return r.json();
        throw new Error("fetch failed");
    }).then(function(d) { allData = d; }).catch(function() {
        allData = EMBEDDED_DATA;
    });
}

// ===== UTILS =====
function fmtNum(n) {
    if (n == null || isNaN(n)) return "0";
    if (Math.abs(n) >= 1e6) return (n/1e6).toFixed(1)+"M";
    if (Math.abs(n) >= 1e3) return (n/1e3).toFixed(1)+"K";
    return Math.round(n).toLocaleString();
}
function fmtDate(d) { var p=d.split("-"); return p[2]+"/"+p[1]; }
function sid(s) { return s.replace(/[^a-zA-Z0-9]/g,"_"); }
function ma7(arr) {
    var r=[];
    for(var i=0;i<arr.length;i++){
        if(i<6){r.push(null);continue;}
        var s=0;for(var j=i-6;j<=i;j++)s+=arr[j];
        r.push(s/7);
    }
    return r;
}

function filterByTime() {
    var base;
    if (timeDays === 0) { base = allData.slice(); }
    else {
        var cut = new Date();
        cut.setDate(cut.getDate() - timeDays);
        base = allData.filter(function(d) { return new Date(d.date) >= cut; });
    }
    filtered = fillMissingDates(base);
}

// Fill in missing calendar dates with null entries so Chart.js shows gaps
// instead of drawing a misleading straight line between distant data points.
function fillMissingDates(arr) {
    if (!arr || arr.length === 0) return [];
    var result = [];
    var start = new Date(arr[0].date);
    var end = new Date(arr[arr.length-1].date);
    var byDate = {};
    arr.forEach(function(d){ byDate[d.date] = d; });
    var cur = new Date(start);
    while (cur <= end) {
        var ds = cur.toISOString().slice(0,10);
        if (byDate[ds]) {
            result.push(byDate[ds]);
        } else {
            // placeholder with null totals/groups — Chart.js treats null as gap
            result.push({date: ds, totals: null, nha_hang: null, hotel: null, doi_thu: null, _missing: true});
        }
        cur.setDate(cur.getDate() + 1);
    }
    return result;
}

function destroyChart(id) {
    if (charts[id]) { charts[id].destroy(); delete charts[id]; }
}

function getDomains(group) {
    // Use SITE_GROUPS as base, but also include any extra domains found in data
    var base = SITE_GROUPS[group] || [];
    var extra = {};
    allData.forEach(function(entry) {
        if (entry[group]) {
            Object.keys(entry[group]).forEach(function(d) { extra[d] = true; });
        }
    });
    var result = base.slice();
    Object.keys(extra).forEach(function(d) {
        if (result.indexOf(d) === -1) result.push(d);
    });
    return result;
}

// Return last/first entry that actually has data (skips _missing placeholders)
function lastReal() {
    for (var i = filtered.length - 1; i >= 0; i--) {
        if (!filtered[i]._missing) return filtered[i];
    }
    return {};
}
function firstReal() {
    for (var i = 0; i < filtered.length; i++) {
        if (!filtered[i]._missing) return filtered[i];
    }
    return {};
}

// ===== KPI =====
function renderKPI() {
    var last = lastReal();
    var t = last.totals || {};
    var own = (t.nha_hang||0) + (t.hotel||0);
    var rival = t.doi_thu || 0;
    var ratio = (own+rival) > 0 ? ((own/(own+rival))*100).toFixed(1) : "0";
    document.getElementById("kpi-row").innerHTML =
        '<div class="stat-box"><div class="stat-val">' + fmtNum(own) + '</div><div class="stat-lbl">Your Total</div></div>' +
        '<div class="stat-box"><div class="stat-val">' + fmtNum(t.nha_hang||0) + '</div><div class="stat-lbl">Nhà Hàng</div></div>' +
        '<div class="stat-box"><div class="stat-val">' + fmtNum(t.hotel||0) + '</div><div class="stat-lbl">Hotel</div></div>' +
        '<div class="stat-box"><div class="stat-val">' + fmtNum(rival) + '</div><div class="stat-lbl">Đối Thủ</div></div>' +
        '<div class="stat-box"><div class="stat-val">' + ratio + '%</div><div class="stat-lbl">Your Share</div></div>';
}

// ===== OVERVIEW CHART =====
function renderOverview() {
    var labels = filtered.map(function(d){return fmtDate(d.date);});
    var datasets = ["nha_hang","hotel","doi_thu"].map(function(g){
        return {
            label: GROUP_LABELS[g],
            data: filtered.map(function(d){return d._missing ? null : ((d.totals||{})[g]||0);}),
            borderColor: GROUP_COLORS[g],
            backgroundColor: GROUP_COLORS[g]+"20",
            tension: 0.3,
            fill: true,
            spanGaps: false,
            pointRadius: filtered.length > 40 ? 0 : 3,
            borderWidth: 2
        };
    });
    destroyChart("overview");
    charts["overview"] = new Chart(document.getElementById("overviewChart"), {
        type: "line",
        data: {labels:labels, datasets:datasets},
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            plugins: {
                legend: {position:"top", labels:{color:"#e2e8f0",usePointStyle:true,pointStyle:"circle",padding:16}}
            },
            scales: {
                x: {ticks:{color:"#94a3b8",maxRotation:0,autoSkip:true,maxTicksLimit:12},grid:{color:"rgba(148,163,184,0.08)"}},
                y: {ticks:{color:"#94a3b8",callback:function(v){return fmtNum(v);}},grid:{color:"rgba(148,163,184,0.08)"}}
            }
        }
    });
}

// ===== GROUP LINE CHART =====
function renderGroupLine(group, canvasId) {
    var domains = getDomains(group);
    var labels = filtered.map(function(d){return fmtDate(d.date);});
    var datasets = domains.map(function(dom, idx) {
        return {
            label: dom,
            data: filtered.map(function(d){return d._missing ? null : ((d[group]||{})[dom]||0);}),
            borderColor: PALETTE[idx % PALETTE.length],
            backgroundColor: PALETTE[idx % PALETTE.length]+"20",
            tension: 0.3,
            fill: false,
            spanGaps: false,
            pointRadius: filtered.length > 40 ? 0 : 2,
            borderWidth: 2
        };
    });
    destroyChart(canvasId);
    charts[canvasId] = new Chart(document.getElementById(canvasId), {
        type: "line",
        data: {labels:labels, datasets:datasets},
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            plugins: {legend:{position:"top",labels:{color:"#e2e8f0",usePointStyle:true,pointStyle:"circle",padding:12,font:{size:11}}}},
            scales: {
                x: {ticks:{color:"#94a3b8",maxRotation:0,autoSkip:true,maxTicksLimit:10},grid:{color:"rgba(148,163,184,0.08)"}},
                y: {ticks:{color:"#94a3b8",callback:function(v){return fmtNum(v);}},grid:{color:"rgba(148,163,184,0.08)"}}
            }
        }
    });
}

// ===== GROUP DOUGHNUT =====
function renderGroupDoughnut(group, canvasId) {
    var domains = getDomains(group);
    var last = lastReal();
    var values = domains.map(function(d){return (last[group]||{})[d]||0;});
    destroyChart(canvasId);
    charts[canvasId] = new Chart(document.getElementById(canvasId), {
        type: "doughnut",
        data: {
            labels: domains,
            datasets: [{data:values, backgroundColor:PALETTE.slice(0,domains.length), borderWidth:0}]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            plugins: {legend:{position:"right",labels:{color:"#e2e8f0",padding:8,font:{size:11}}}}
        }
    });
}

// ===== GROUP GROWTH BAR =====
function renderGroupGrowth(group, canvasId) {
    var domains = getDomains(group);
    var first = firstReal();
    var last = lastReal();
    var growths = domains.map(function(d){
        var fv = (first[group]||{})[d]||0;
        var lv = (last[group]||{})[d]||0;
        return fv === 0 ? 0 : ((lv-fv)/fv)*100;
    });
    var colors = growths.map(function(g){return g>=0 ? "#22c55e" : "#ef4444";});
    destroyChart(canvasId);
    charts[canvasId] = new Chart(document.getElementById(canvasId), {
        type: "bar",
        data: {
            labels: domains,
            datasets: [{label:"Growth %", data:growths, backgroundColor:colors, borderRadius:4}]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            plugins: {legend:{display:false}},
            scales: {
                x: {ticks:{color:"#94a3b8",callback:function(v){return v.toFixed(0)+"%";}},grid:{color:"rgba(148,163,184,0.08)"}},
                y: {ticks:{color:"#e2e8f0",font:{size:11}},grid:{display:false}}
            }
        }
    });
}

// ===== BUILD ALL-GROUPS PANEL =====
function buildAllPanel() {
    var html = "";
    ["nha_hang","hotel","doi_thu"].forEach(function(g) {
        var color = GROUP_COLORS[g];
        var lineId = "all-line-"+g;
        var doughId = "all-dough-"+g;
        var growId = "all-grow-"+g;
        html += '<div class="group-hdr"><span class="dot" style="background:'+color+'"></span>'+GROUP_LABELS[g]+' ('+getDomains(g).length+' sites)</div>';
        html += '<div class="grid-2">';
        html += '<div class="card"><div class="card-title">Index Over Time</div><div class="chart-wrap"><canvas id="'+lineId+'"></canvas></div></div>';
        html += '<div class="card"><div class="card-title">Distribution</div><div class="doughnut-wrap"><canvas id="'+doughId+'"></canvas></div></div>';
        html += '</div>';
        html += '<div class="card"><div class="card-title">Growth %</div><div class="growth-wrap"><canvas id="'+growId+'"></canvas></div></div>';
    });
    document.getElementById("panel-all").innerHTML = html;
}

function renderAllPanel() {
    ["nha_hang","hotel","doi_thu"].forEach(function(g) {
        renderGroupLine(g, "all-line-"+g);
        renderGroupDoughnut(g, "all-dough-"+g);
        renderGroupGrowth(g, "all-grow-"+g);
    });
}

// ===== BUILD DETAIL PANEL =====
function buildDetailPanel(group) {
    var domains = getDomains(group);
    var color = GROUP_COLORS[group];
    var lineId = "det-line-"+group;
    var doughId = "det-dough-"+group;
    var growId = "det-grow-"+group;

    var html = "";
    html += '<div class="group-hdr"><span class="dot" style="background:'+color+'"></span>'+GROUP_LABELS[group]+' — Detail View</div>';
    html += '<div class="grid-2">';
    html += '<div class="card"><div class="card-title">All Domains</div><div class="chart-wrap"><canvas id="'+lineId+'"></canvas></div></div>';
    html += '<div class="card"><div class="card-title">Distribution</div><div class="doughnut-wrap"><canvas id="'+doughId+'"></canvas></div></div>';
    html += '</div>';
    html += '<div class="card"><div class="card-title">Growth %</div><div class="growth-wrap"><canvas id="'+growId+'"></canvas></div></div>';

    // Domain cards
    var realEntries = filtered.filter(function(d){return !d._missing;});
    domains.forEach(function(dom) {
        var values = realEntries.map(function(d){return (d[group]||{})[dom]||0;});
        var latest = values[values.length-1]||0;
        var highest = values.length > 0 ? Math.max.apply(null, values) : 0;
        var nonZero = values.filter(function(v){return v>0;});
        var lowest = nonZero.length > 0 ? Math.min.apply(null, nonZero) : 0;
        var firstVal = values[0]||0;
        var growth = firstVal===0 ? 0 : ((latest-firstVal)/firstVal)*100;
        var cid = "mini-"+sid(dom)+"-"+group;

        html += '<div class="domain-card">';
        html += '<div class="domain-name">'+dom+'</div>';
        html += '<div class="domain-stats">';
        html += '<div><div class="d-stat-val">'+fmtNum(latest)+'</div><div class="d-stat-lbl">Current</div></div>';
        html += '<div><div class="d-stat-val">'+fmtNum(highest)+'</div><div class="d-stat-lbl">Highest</div></div>';
        html += '<div><div class="d-stat-val">'+fmtNum(lowest)+'</div><div class="d-stat-lbl">Lowest</div></div>';
        html += '<div><div class="d-stat-val '+(growth>=0?"pos":"neg")+'">'+( growth>=0?"+":"")+growth.toFixed(1)+'%</div><div class="d-stat-lbl">Growth</div></div>';
        html += '</div>';
        html += '<div class="mini-wrap"><canvas id="'+cid+'"></canvas></div>';
        html += '</div>';
    });

    document.getElementById("panel-"+group).innerHTML = html;
}

function renderDetailPanel(group) {
    renderGroupLine(group, "det-line-"+group);
    renderGroupDoughnut(group, "det-dough-"+group);
    renderGroupGrowth(group, "det-grow-"+group);

    var domains = getDomains(group);
    domains.forEach(function(dom, idx) {
        var cid = "mini-"+sid(dom)+"-"+group;
        var canvas = document.getElementById(cid);
        if (!canvas) return;
        var values = filtered.map(function(d){return d._missing ? null : ((d[group]||{})[dom]||0);});
        var avg = ma7(values.map(function(v){return v===null?0:v;}));
        var labels = filtered.map(function(d){return fmtDate(d.date);});
        destroyChart(cid);
        charts[cid] = new Chart(canvas, {
            type: "line",
            data: {
                labels: labels,
                datasets: [
                    {label:"Index",data:values,borderColor:PALETTE[idx%PALETTE.length],borderWidth:1.5,pointRadius:0,tension:0.3,spanGaps:false},
                    {label:"7d MA",data:avg,borderColor:"#94a3b8",borderDash:[4,4],borderWidth:1,pointRadius:0,tension:0.3}
                ]
            },
            options: {
                responsive:true, maintainAspectRatio:false, animation:false,
                plugins:{legend:{display:false}},
                scales:{y:{display:false},x:{display:false}}
            }
        });
    });
}

// ===== GROWTH TABLE =====
// Find entry in allData at (or before) latest.date - daysAgo.
// Returns null if no data that old.
function findEntryDaysAgo(daysAgo) {
    if (allData.length === 0) return null;
    var latest = new Date(allData[allData.length-1].date);
    var target = new Date(latest);
    target.setDate(target.getDate() - daysAgo);
    var targetStr = target.toISOString().slice(0,10);
    var best = null;
    for (var i = allData.length-1; i >= 0; i--) {
        if (allData[i].date <= targetStr) { best = allData[i]; break; }
    }
    return best;
}

function fmtDelta(curr, prev) {
    if (prev === null || prev === 0) {
        if (curr > 0 && (prev === null || prev === 0)) return '<span class="muted">—</span>';
        return '<span class="muted">—</span>';
    }
    var diff = curr - prev;
    var pct = (diff / prev) * 100;
    var cls = diff >= 0 ? "pos" : "neg";
    var sign = diff >= 0 ? "+" : "";
    return '<span class="'+cls+'">'+sign+fmtNum(diff)+' ('+sign+pct.toFixed(2)+'%)</span>';
}

function renderGrowthTable() {
    // Use allData (not filtered) so lookback isn't limited by time filter
    var last = (function(){
        for (var i = allData.length-1; i >= 0; i--) {
            if (!allData[i]._missing) return allData[i];
        }
        return {};
    })();
    var e1 = findEntryDaysAgo(1);
    var e7 = findEntryDaysAgo(7);
    var e14 = findEntryDaysAgo(14);
    var e30 = findEntryDaysAgo(30);

    var rows = [];
    ["nha_hang","hotel","doi_thu"].forEach(function(g){
        getDomains(g).forEach(function(dom){
            var lv = (last[g]||{})[dom]||0;
            var v1 = e1 ? ((e1[g]||{})[dom]||0) : null;
            var v7 = e7 ? ((e7[g]||{})[dom]||0) : null;
            var v14 = e14 ? ((e14[g]||{})[dom]||0) : null;
            var v30 = e30 ? ((e30[g]||{})[dom]||0) : null;
            // sort key: 7-day % growth (fallback to raw current)
            var sortPct = (v7 && v7 > 0) ? ((lv - v7) / v7) * 100 : -Infinity;
            if (lv > 0 || v1 > 0 || v7 > 0 || v14 > 0 || v30 > 0) {
                rows.push({dom:dom,group:GROUP_LABELS[g],lv:lv,v1:v1,v7:v7,v14:v14,v30:v30,sortPct:sortPct});
            }
        });
    });
    rows.sort(function(a,b){return b.sortPct - a.sortPct;});

    var tbody = document.getElementById("growthBody");
    tbody.innerHTML = rows.slice(0,50).map(function(r,i){
        return "<tr>"+
            "<td>"+(i+1)+"</td>"+
            "<td>"+r.dom+"</td>"+
            "<td>"+r.group+"</td>"+
            "<td><b>"+fmtNum(r.lv)+"</b></td>"+
            "<td>"+fmtDelta(r.lv, r.v1)+"</td>"+
            "<td>"+fmtDelta(r.lv, r.v7)+"</td>"+
            "<td>"+fmtDelta(r.lv, r.v14)+"</td>"+
            "<td>"+fmtDelta(r.lv, r.v30)+"</td>"+
            "</tr>";
    }).join("");
}

// ===== TAB SWITCHING =====
function switchTab(tab) {
    activeTab = tab;
    document.querySelectorAll(".tab").forEach(function(t){t.classList.remove("active");});
    document.querySelectorAll(".tab-panel").forEach(function(p){p.classList.remove("active");});
    var tabBtn = document.querySelector('.tab[data-tab="'+tab+'"]');
    if (tabBtn) tabBtn.classList.add("active");
    var panel = document.getElementById("panel-"+tab);
    if (panel) panel.classList.add("active");

    // Render after panel is visible
    requestAnimationFrame(function() {
        if (tab === "all") {
            renderAllPanel();
        } else {
            buildDetailPanel(tab);
            renderDetailPanel(tab);
        }
    });
}

// ===== MAIN RENDER =====
function render() {
    filterByTime();
    if (filtered.length === 0) return;
    renderKPI();
    renderOverview();
    renderGrowthTable();
    switchTab(activeTab);
}

// ===== EVENT LISTENERS =====
document.querySelectorAll(".time-btn").forEach(function(btn){
    btn.addEventListener("click", function(){
        document.querySelectorAll(".time-btn").forEach(function(b){b.classList.remove("active");});
        btn.classList.add("active");
        timeDays = parseInt(btn.getAttribute("data-days"));
        render();
    });
});
document.querySelectorAll(".tab").forEach(function(btn){
    btn.addEventListener("click", function(){
        switchTab(btn.getAttribute("data-tab"));
    });
});

// ===== INIT =====
loadData().then(function() {
    if (allData.length === 0) { document.getElementById("lastUpdated").textContent = "No data available"; return; }
    document.getElementById("lastUpdated").textContent = "Last updated: " + allData[allData.length-1].date + " | " + allData.length + " data points";
    buildAllPanel();
    render();
});
</script>
</body>
</html>'''

with open('/sessions/admiring-hopeful-wozniak/index-analysis-new.html', 'w') as f:
    f.write(html)

print(f"File written: {len(html)} chars, {len(html.splitlines())} lines")
