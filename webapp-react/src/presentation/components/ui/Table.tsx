import React from 'react';

type TableProps = {
    headers: string[];
    children: React.ReactNode;
};

export const Table: React.FC<TableProps> = ({ headers, children }) => {
    return (
        <div className="overflow-x-auto w-full">
            <table className="w-full text-left border-collapse mt-4">
                <thead>
                    <tr className="border-b border-white/10 text-textMuted uppercase text-sm">
                        {headers.map((h, i) => (
                            <th key={i} className="pb-3 px-2 font-medium">{h}</th>
                        ))}
                    </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                    {children}
                </tbody>
            </table>
        </div>
    );
};

export const TableRow: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className = '' }) => (
    <tr className={`hover:bg-white/5 transition-colors ${className}`}>
        {children}
    </tr>
);

export const TableCell: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className = '' }) => (
    <td className={`py-4 px-2 ${className}`}>
        {children}
    </td>
);
