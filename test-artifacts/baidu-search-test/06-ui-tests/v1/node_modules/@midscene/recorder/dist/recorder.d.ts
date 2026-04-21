export interface ChromeRecordedEvent {
    type: 'click' | 'scroll' | 'input' | 'navigation' | 'setViewport' | 'keydown';
    url?: string;
    title?: string;
    value?: string;
    elementRect?: {
        left?: number;
        top?: number;
        width?: number;
        height?: number;
        x?: number;
        y?: number;
    };
    pageInfo: {
        width: number;
        height: number;
    };
    screenshotBefore?: string;
    screenshotAfter?: string;
    elementDescription?: string;
    descriptionLoading?: boolean;
    screenshotWithBox?: string;
    timestamp: number;
    hashId: string;
}
export interface RecordedEvent extends ChromeRecordedEvent {
    element?: HTMLElement;
    targetTagName?: string;
    targetId?: string;
    targetClassName?: string;
    isLabelClick?: boolean;
    labelInfo?: {
        htmlFor?: string;
        textContent?: string;
        xpath?: string;
    };
    isTrusted?: boolean;
    detail?: number;
    inputType?: string;
}
export type EventCallback = (event: RecordedEvent) => void;
export declare class EventRecorder {
    private isRecording;
    private eventCallback;
    private scrollThrottleTimer;
    private scrollThrottleDelay;
    private inputThrottleTimer;
    private inputThrottleDelay;
    private lastViewportScroll;
    private scrollTargets;
    private sessionId;
    constructor(eventCallback: EventCallback, sessionId: string);
    createNavigationEvent(url: string, title: string): ChromeRecordedEvent;
    start(): void;
    stop(): void;
    private handleClick;
    private handleScroll;
    private handleInput;
    private checkLabelClick;
    isActive(): boolean;
    optimizeEvent(event: RecordedEvent, events: RecordedEvent[]): RecordedEvent[];
}
export declare function convertToChromeEvent(event: RecordedEvent): ChromeRecordedEvent;
export declare function convertToChromeEvents(events: RecordedEvent[]): ChromeRecordedEvent[];
