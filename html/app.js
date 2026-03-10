"use strict";

document.addEventListener("DOMContentLoaded", () => {
    // Make sure data is ready
    if (typeof COMPETITION_DATA === 'undefined') {
        console.error("COMPETITION_DATA not found. Ensure data.js is loaded correctly.");
        return;
    }

    const data = COMPETITION_DATA;

    // Elements
    const navLinks = document.querySelectorAll('.nav-links li');
    const views = document.querySelectorAll('.view');
    const pageTitle = document.getElementById('page-title');

    // --- Routing & Navigation ---
    function switchView(viewName) {
        // Update active link if there's a matching nav item
        navLinks.forEach(l => {
            l.classList.remove('active');
            if (l.dataset.view === viewName) {
                l.classList.add('active');
            }
        });

        // Switch views
        const targetViewId = 'view-' + viewName;
        views.forEach(view => {
            view.style.display = 'none';
            view.classList.remove('active-view');
        });

        const targetView = document.getElementById(targetViewId);
        if (targetView) {
            targetView.style.display = 'block';
            // Trigger reflow for animation
            void targetView.offsetWidth;
            targetView.classList.add('active-view');
        }

        // Update title cleanly
        const titles = {
            'standings': 'Live Standings',
            'members': 'Full Roster',
            'history': 'Activity History',
            'roster-detail': 'Roster Profile'
        };

        if (titles[viewName]) {
            pageTitle.innerText = titles[viewName];
        }
    }

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            switchView(link.dataset.view);
        });
    });

    // --- Data Rendering ---

    function initApp() {
        document.getElementById('last-updated-text').innerText = data.last_updated;

        renderStandingsOverview();
        renderTeamBattle();
        renderTopRunners();
        renderRosterGrid('all');
        initHistory();

        setupFilters();
    }

    // Attach Back Button Handler
    const backBtn = document.getElementById('btn-back-roster');
    if (backBtn) {
        backBtn.addEventListener('click', () => {
            switchView('roster');
        });
    }

    function renderStandingsOverview() {
        const mandaDist = data.teams["Mandalorian"].total_distance;
        const itDist = data.teams["IT System"].total_distance;
        const total = mandaDist + itDist;

        document.getElementById('global-total-distance').innerText = total.toFixed(2) + ' km';

        let mandaPerc = 50;
        let itPerc = 50;
        if (total > 0) {
            mandaPerc = (mandaDist / total) * 100;
            itPerc = (itDist / total) * 100;
        }

        // Ensure UI updates smoothly for the progress bars
        setTimeout(() => {
            document.getElementById('progress-manda').style.width = mandaPerc + '%';
            document.getElementById('progress-it').style.width = itPerc + '%';
        }, 300);

        document.getElementById('manda-percent').innerText = mandaPerc.toFixed(1) + '%';
        document.getElementById('it-percent').innerText = itPerc.toFixed(1) + '%';
    }

    function renderTeamBattle() {
        const grid = document.getElementById('team-battle-grid');
        grid.innerHTML = '';

        const teams = [
            { key: "IT System", icon: "💻", cls: "it" },
            { key: "Mandalorian", icon: "🪖", cls: "manda" }
        ];

        // Sort to show leader first
        teams.sort((a, b) => data.teams[b.key].total_distance - data.teams[a.key].total_distance);

        teams.forEach((t, index) => {
            const tData = data.teams[t.key];
            const html = `
                <div class="team-card glass-panel ${t.cls}">
                    <div class="team-header">
                        <div class="team-name">${t.icon} ${t.key}</div>
                        ${index === 0 ? '<span style="font-size: 1.5rem;" title="Current Leader">👑</span>' : ''}
                    </div>
                    <div class="team-stats">
                        <div class="stat-inner">
                            <div class="stat-box">
                                <div class="stat-label">Total Q1</div>
                                <div class="stat-value" style="font-size: 2rem;">${tData.total_distance.toFixed(2)} <span style="font-size: 1rem;">km</span></div>
                            </div>
                        </div>
                        <div class="stat-inner">
                            <div class="stat-box">
                                <div class="stat-label">Avg / Person</div>
                                <div class="stat-value" style="font-size: 2rem;">${tData.avg_distance.toFixed(2)} <span style="font-size: 1rem;">km</span></div>
                            </div>
                        </div>
                    </div>
                    <div style="margin-top: 16px; font-size: 0.9rem; color: var(--text-muted); opacity: 0.8;">
                        Active Members: <strong>${tData.active_members} / ${tData.members}</strong>
                    </div>
                </div>
            `;
            grid.innerHTML += html;
        });
    }

    function renderTopRunners() {
        const tbody = document.querySelector('#top-runners-table tbody');
        tbody.innerHTML = '';

        // Roster is already sorted by total_distance descending
        const top5 = data.roster.slice(0, 5);

        top5.forEach((r, idx) => {
            const teamBadgeCls = r.team === 'Mandalorian' ? 'badge-manda' : 'badge-it';
            let rankIcon = idx + 1;
            if (idx === 0) rankIcon = '🥇 1';
            if (idx === 1) rankIcon = '🥈 2';
            if (idx === 2) rankIcon = '🥉 3';

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${rankIcon}</strong></td>
                <td><strong>${r.nickname}</strong> <span style="opacity: 0.5;">(${r.thai_name})</span></td>
                <td><span class="team-badge ${teamBadgeCls}">${r.team}</span></td>
                <td><strong>${r.total_distance.toFixed(2)} km</strong></td>
                <td>📅 ${r.active_days} days</td>
            `;
            tbody.appendChild(tr);
        });
    }

    function renderRosterGrid(filterTeam) {
        const grid = document.getElementById('roster-grid');
        grid.innerHTML = '';

        let filtered = data.roster;
        if (filterTeam !== 'all') {
            filtered = data.roster.filter(r => r.team === filterTeam);
        }

        filtered.forEach(r => {
            const teamCls = r.team.replace(' ', '_');
            const teamIcon = r.team === 'Mandalorian' ? '🪖' : '💻';

            // Build additional stats if available constraints
            let detailHtml = '';
            if (r.stats_details) {
                if (r.stats_details.best_pace) {
                    const bpMins = Math.floor(r.stats_details.best_pace / 60);
                    const bpSecs = String(r.stats_details.best_pace % 60).padStart(2, '0');
                    detailHtml += `<div style="font-size:0.85rem; color:var(--text-muted); margin-top:8px;">⚡ Best Pace: ${bpMins}:${bpSecs}/km</div>`;
                }
                if (r.stats_details.longest_run_dist > 0) {
                    detailHtml += `<div style="font-size:0.85rem; color:var(--text-muted); margin-top:4px;">🏅 Longest: ${r.stats_details.longest_run_dist} km</div>`;
                }
            }

            let imagesHtml = '';
            if (r.recent_images && r.recent_images.length > 0) {
                imagesHtml = '<div style="display:flex; gap:8px; margin-top:12px; overflow-x:auto;">';
                r.recent_images.forEach(img => {
                    imagesHtml += `<img src="${img}" style="width:40px; height:40px; border-radius:8px; object-fit:cover; border:1px solid rgba(255,255,255,0.1)">`;
                });
                imagesHtml += '</div>';
            }

            const card = document.createElement('div');
            card.className = `member-card glass-panel fade-in ${teamCls}`;
            card.style.cursor = 'pointer';
            card.style.transition = 'transform 0.2s';
            card.addEventListener('mouseenter', () => card.style.transform = 'scale(1.02)');
            card.addEventListener('mouseleave', () => card.style.transform = 'scale(1)');

            // Fix: send relative index in the global data.roster array
            const globalIndex = data.roster.indexOf(r);
            card.addEventListener('click', () => openRosterDetail(globalIndex));

            card.innerHTML = `
                <h3>${r.nickname} <span style="font-size:1rem; opacity:0.6; font-weight: normal;">${r.thai_name}</span></h3>
                <div style="font-size:0.85rem; margin-bottom: 12px; opacity:0.8;">
                    ${teamIcon} ${r.team}
                </div>
                <div class="member-dist gradient-text">${r.total_distance.toFixed(2)} <span style="font-size:1rem">km</span></div>
                
                <div style="font-size:0.9rem;">
                    📅 Active Days: <strong>${r.active_days}</strong><br>
                    📸 Screenshots: <strong>${r.image_count}</strong>
                </div>
                ${detailHtml}
                ${imagesHtml}
            `;
            grid.appendChild(card);
        });
    }

    function openRosterDetail(memberIndex) {
        const m = data.roster[memberIndex];
        if (!m) return;

        switchView('roster-detail');

        const isManda = m.team === 'Mandalorian';
        const teamIcon = isManda ? '🪖' : '💻';
        const teamCls = isManda ? 'badge-manda' : 'badge-it';

        // Set Header
        const header = document.getElementById('detail-header');
        header.innerHTML = `
            <div style="font-size: 2.5rem; font-family: var(--font-heading); font-weight: 800; margin-bottom: 8px;">
                ${m.nickname} <span style="color: var(--text-muted); font-size: 1.2rem; font-weight: normal;">(${m.thai_name})</span>
            </div>
            <div class="team-badge ${teamCls}" style="display: inline-block; padding: 4px 12px; font-size: 1rem;">
                ${teamIcon} ${m.team}
            </div>
            <div style="margin-top: 15px; font-size: 1.1rem; opacity: 0.9;">
                🔥 <strong>${m.total_distance.toFixed(2)} km</strong> run over <strong>${m.active_days}</strong> active days.
            </div>
        `;

        // Render Markdown safely
        const mdObj = m.markdown || {};
        const divReadme = document.getElementById('detail-readme');
        const divPlan = document.getElementById('detail-plan');
        const divStats = document.getElementById('detail-stats');

        // Use marked.parse if available (which we added via CDN)
        const parseMd = text => window.marked ? window.marked.parse(text || "*No data available*") : "<p>Markdown parser not loaded.</p>";

        divReadme.innerHTML = `<h2 style="margin-top:0">👤 Profile README</h2>` + parseMd(mdObj.readme);
        divStats.innerHTML = `<h2 style="margin-top:0">📊 Statistics</h2>` + parseMd(mdObj.statistics);
        divPlan.innerHTML = `<h2 style="margin-top:0">📝 Running Plan</h2>` + parseMd(mdObj.plan);

        // Scroll to top
        window.scrollTo(0, 0);
    }

    function setupFilters() {
        const btns = document.querySelectorAll('.filter-btn');
        btns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                btns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                renderRosterGrid(btn.dataset.filter);
            });
        });
    }

    let currentHistoryFilter = 'all';
    let historyPage = 1;
    const HISTORY_PAGE_SIZE = 20;
    let filteredHistory = [];

    function setupHistoryFilters() {
        const filterBar = document.getElementById('history-filter-bar');

        // Extract distinct months from data to add them as filters
        const months = new Set();
        data.activities.forEach(a => months.add(a.month));

        // Add month buttons dynamically
        Array.from(months).sort().forEach(m => {
            const btn = document.createElement('button');
            btn.className = 'filter-btn';
            btn.dataset.filter = m;
            btn.innerText = m;
            filterBar.appendChild(btn);
        });

        const btns = filterBar.querySelectorAll('.filter-btn');
        btns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                btns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                currentHistoryFilter = btn.dataset.filter;
                historyPage = 1;
                renderHistory(true);
            });
        });

        // Setup infinite scroll
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.addEventListener('scroll', () => {
                if (document.getElementById('view-history').style.display === 'block') {
                    if ((mainContent.clientHeight + mainContent.scrollTop) >= mainContent.scrollHeight - 200) {
                        loadMoreHistory();
                    }
                }
            });
        }
    }

    function initHistory() {
        if (!data.activities) data.activities = [];
        setupHistoryFilters();
        renderHistory(true);
    }

    function renderHistory(reset = false) {
        const timeline = document.getElementById('history-timeline');

        if (reset) {
            timeline.innerHTML = '<h2 style="font-family: var(--font-heading); margin-bottom:20px;">📜 Recent Activity</h2>';

            // Apply filter
            if (currentHistoryFilter === 'all') {
                filteredHistory = data.activities;
            } else if (currentHistoryFilter === 'Q1') {
                // Assuming all 2026-Jan/Feb/Mar are Q1
                filteredHistory = data.activities.filter(a => a.month.includes('Jan') || a.month.includes('Feb') || a.month.includes('Mar'));
            } else {
                // Exact month filter
                filteredHistory = data.activities.filter(a => a.month === currentHistoryFilter);
            }
        }

        if (filteredHistory.length === 0) {
            timeline.innerHTML += '<p style="color:var(--text-muted);">No activities found for this filter.</p>';
            document.getElementById('history-loading').style.display = 'none';
            return;
        }

        const startIndex = (historyPage - 1) * HISTORY_PAGE_SIZE;
        const endIndex = startIndex + HISTORY_PAGE_SIZE;
        const pageItems = filteredHistory.slice(startIndex, endIndex);

        pageItems.forEach(act => {
            // Build the mini-table for this date
            let runnersHtml = '';
            act.runners_list.forEach(r => {
                const isManda = r.team === 'Mandalorian';
                const teamIcon = isManda ? '🪖' : '💻';
                const teamCls = isManda ? 'badge-manda' : 'badge-it';

                let runnerImages = '';
                if (r.images && r.images.length > 0) {
                    runnerImages = '<div style="display:flex; gap:4px; margin-top:4px;">';
                    r.images.forEach(img => {
                        runnerImages += `<img src="${img}" style="width:30px; height:30px; border-radius:4px; object-fit:cover; border:1px solid rgba(255,255,255,0.1)">`;
                    });
                    runnerImages += '</div>';
                }

                runnersHtml += `
                    <tr>
                        <td><strong>${r.name}</strong> <span class="team-badge ${teamCls}" style="margin-left:8px; padding:2px 6px; font-size:0.7rem;">${teamIcon}</span></td>
                        <td><strong>${r.distance.toFixed(2)}</strong> km</td>
                        <td>${runnerImages}</td>
                    </tr>
                `;
            });

            const html = `
                <div class="timeline-item timeline-group">
                    <div class="timeline-group-header">
                        <h3>📅 ${act.date}</h3>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 20px; margin-top: 16px;">
                        
                        <!-- Runners Table -->
                        <div class="table-responsive" style="padding:0; margin:0; overflow-x:auto;">
                            <table class="data-table" style="font-size: 0.9rem;">
                                <thead>
                                    <tr>
                                        <th>Runner</th>
                                        <th>Dist</th>
                                        <th>Evidence</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${runnersHtml}
                                </tbody>
                            </table>
                        </div>

                        <!-- Daily Scoreboard -->
                        <div class="daily-scoreboard glass-panel" style="padding: 16px; align-self: start;">
                            <div style="font-weight:600; font-size: 0.85rem; color:var(--text-muted); text-transform:uppercase; margin-bottom: 12px; letter-spacing:1px;">Daily Summary</div>
                            
                            <div style="display:flex; justify-content: space-between; margin-bottom: 8px;">
                                <span>🪖 Manda Today:</span>
                                <strong>+${act.mando_daily.toFixed(2)} km</strong>
                            </div>
                            <div style="display:flex; justify-content: space-between; margin-bottom: 16px; border-bottom:1px solid rgba(255,255,255,0.05); padding-bottom:16px;">
                                <span>💻 IT Today:</span>
                                <strong>+${act.it_daily.toFixed(2)} km</strong>
                            </div>

                            <div style="display:flex; justify-content: space-between; margin-bottom: 8px; font-size: 0.85rem; opacity: 0.8;">
                                <span>Manda Total:</span>
                                <span>${act.mando_accum.toFixed(2)} km</span>
                            </div>
                            <div style="display:flex; justify-content: space-between; font-size: 0.85rem; opacity: 0.8;">
                                <span>IT Total:</span>
                                <span>${act.it_accum.toFixed(2)} km</span>
                            </div>
                        </div>

                    </div>
                </div>
            `;
            timeline.innerHTML += html;
        });

        // Toggle loader visibility
        if (endIndex >= filteredHistory.length) {
            document.getElementById('history-loading').style.display = 'none';
        } else {
            document.getElementById('history-loading').style.display = 'block';
        }
    }

    let isLoadingHistory = false;
    function loadMoreHistory() {
        if (isLoadingHistory) return;

        const endIndex = historyPage * HISTORY_PAGE_SIZE;
        if (endIndex < filteredHistory.length) {
            isLoadingHistory = true;
            historyPage++;

            // brief simulated delay for "loading" feel
            setTimeout(() => {
                renderHistory(false);
                isLoadingHistory = false;
            }, 300);
        }
    }

    // Run
    initApp();
});
