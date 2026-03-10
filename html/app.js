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
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            // Update active link
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            // Switch views
            const targetViewId = 'view-' + link.dataset.view;
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

            // Update title
            const titles = {
                'standings': 'Live Standings',
                'members': 'Full Roster',
                'history': 'Activity History'
            };
            pageTitle.innerText = titles[link.dataset.view];
        });
    });

    // --- Data Rendering ---

    function initApp() {
        document.getElementById('last-updated-text').innerText = data.last_updated;

        renderStandingsOverview();
        renderTeamBattle();
        renderTopRunners();
        renderRosterGrid('all');
        renderHistory();

        setupFilters();
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

            const html = `
                <div class="member-card glass-panel ${teamCls}">
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
                </div>
            `;
            grid.innerHTML += html;
        });
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

    function renderHistory() {
        const timeline = document.getElementById('history-timeline');
        timeline.innerHTML = '<h2 style="font-family: var(--font-heading); margin-bottom:20px;">📜 Recent Activity</h2>';

        if (!data.recent_activities || data.recent_activities.length === 0) {
            timeline.innerHTML += '<p style="color:var(--text-muted);">No recent activities found.</p>';
            return;
        }

        data.recent_activities.forEach(act => {
            const html = `
                <div class="timeline-item flex">
                    <div class="timeline-date">${act.date}</div>
                    <div class="timeline-content">
                        <strong>${act.name}</strong> recorded <span style="color: var(--accent); font-weight:800; font-size:1.1rem;">${act.distance.toFixed(2)} km</span>
                    </div>
                </div>
            `;
            timeline.innerHTML += html;
        });
    }

    // Run
    initApp();
});
