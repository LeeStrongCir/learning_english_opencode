import type React from 'react';
import './shiny-text.css';
type ColorTheme = 'blue' | 'purple' | 'green' | 'rainbow';
interface ShinyTextProps {
    text: string;
    disabled?: boolean;
    speed?: number;
    className?: string;
    colorTheme?: ColorTheme;
}
export declare const ShinyText: React.FC<ShinyTextProps>;
export {};
