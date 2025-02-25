import React from 'react';
import './css/Tooltip.css';

const Tooltip = ({ text, children }) => {
    return (
        <div className="tooltip">
            {children}
            <div className="tooltiptext box--shadow-btn">{text}</div>
        </div>
    );
};

export default Tooltip;