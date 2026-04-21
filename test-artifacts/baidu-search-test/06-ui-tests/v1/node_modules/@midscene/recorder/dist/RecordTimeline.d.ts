import type { RecordedEvent } from './recorder';
import './RecordTimeline.css';
interface RecordTimelineProps {
    events: RecordedEvent[];
    onEventClick?: (event: RecordedEvent, index: number) => void;
}
export declare const RecordTimeline: ({ events, onEventClick, }: RecordTimelineProps) => import("react/jsx-runtime").JSX.Element;
export {};
