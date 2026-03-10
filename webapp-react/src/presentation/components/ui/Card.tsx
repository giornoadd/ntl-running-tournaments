import React from 'react';

export const Card: React.FC<{ children: React.ReactNode; className?: string; onClick?: () => void }> = ({ children, className = '', onClick }) => {
    return (
        <div
            onClick={onClick}
            className={`glass-panel p-6 ${onClick ? 'cursor-pointer hover:scale-[1.02] active:scale-[0.98] transition-transform' : ''} ${className}`}
        >
            {children}
        </div>
    );
};
