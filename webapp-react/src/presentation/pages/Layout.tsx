import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';

export const Layout: React.FC = () => {
    return (
        <div className="flex h-screen w-full overflow-hidden text-textMain relative">

            {/* Sidebar Navigation */}
            <nav className="w-64 flex-shrink-0 glass-panel border-r border-white/10 flex flex-col p-6 m-4 mr-0 z-10 hidden md:flex">
                <div className="flex items-center gap-3 mb-10 text-2xl font-heading font-black">
                    <span className="text-3xl">🏃</span>
                    <span>Run 2026</span>
                </div>

                <ul className="flex flex-col gap-2">
                    <NavItem to="/" icon="🏆" label="Standings" />
                    <NavItem to="/roster" icon="👥" label="Full Roster" />
                    <NavItem to="/history" icon="⏱️" label="History" />
                </ul>

                <div className="mt-auto pt-6 border-t border-white/10">
                    <a
                        href="/ntl-running-tournaments/docs/index.html"
                        className="flex items-center gap-3 p-3 rounded-lg font-medium transition-colors text-lg text-textMuted hover:bg-white/5 hover:text-white"
                    >
                        <span className="text-xl">🏠</span>
                        Tournament Home
                    </a>
                </div>
            </nav>

            {/* Mobile Nav Top Bar (Simplistic) */}
            <div className="md:hidden absolute top-0 w-full glass-panel z-20 flex justify-between p-4 px-6 items-center">
                <div className="font-heading font-black text-xl">🏃 Run 2026</div>
                <div className="flex gap-4">
                    <NavLink to="/">🏆</NavLink>
                    <NavLink to="/roster">👥</NavLink>
                    <NavLink to="/history">⏱️</NavLink>
                    <a href="/ntl-running-tournaments/docs/index.html">🏠</a>
                </div>
            </div>

            {/* Main Content Area */}
            <main className="flex-1 flex flex-col h-full overflow-y-auto p-4 md:p-8 pt-20 md:pt-8 w-full z-10">
                <header className="mb-8 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                    <h1 id="page-title" className="text-3xl md:text-5xl font-heading font-black tracking-tight" style={{ textShadow: "0 4px 20px rgba(107,76,222,0.4)" }}>
                        Running Competition
                    </h1>
                </header>

                <section className="flex-1 pb-10">
                    <Outlet />
                </section>
            </main>
        </div>
    );
};

const NavItem: React.FC<{ to: string; icon: string; label: string }> = ({ to, icon, label }) => {
    return (
        <li>
            <NavLink
                to={to}
                className={({ isActive }) => `
                    flex items-center gap-3 p-3 rounded-lg font-medium transition-colors text-lg
                    ${isActive ? 'bg-accent/20 text-accent border border-accent/30' : 'text-textMuted hover:bg-white/5 hover:text-white'}
                `}
            >
                <span className="text-xl">{icon}</span>
                {label}
            </NavLink>
        </li>
    );
};
