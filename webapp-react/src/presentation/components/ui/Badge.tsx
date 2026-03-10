import React from 'react';

type BadgeProps = {
    team?: string;
    children?: React.ReactNode;
    className?: string;
};

export const Badge: React.FC<BadgeProps> = ({ team, children, className = '' }) => {
    let teamClass = 'bg-white/10 text-white';
    if (team === 'Mandalorian') {
        teamClass = 'bg-mandaBg text-manda border-manda/20';
    } else if (team === 'IT System') {
        teamClass = 'bg-itBg text-it border-it/20';
    }

    return (
        <span className={`px-2.5 py-1 rounded-full text-xs font-semibold border ${teamClass} ${className}`}>
            {children}
        </span>
    );
};
