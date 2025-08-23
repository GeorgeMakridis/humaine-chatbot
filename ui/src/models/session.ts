import { generateSimpleUniqueId } from '../utils/utils';
import { SessionEndType } from '../types/sessionType';
import { MetricDictionary } from './userMessage';
import { MetricTracker, MetricValue } from '../trackers/metricTracker';

export class Session {
    id: string;

    private userId: string;

    private sessionStart: number | null = null;
    private sessionEnd: number | null = null;
    private sessionEndType: SessionEndType | null = null;

    /** The message related metrics */
    metrics: MetricDictionary = {};

    constructor(userId: string) {
        this.userId = userId;
        this.id = generateSimpleUniqueId();
        this.sessionStart = Date.now();
    }

    /**
     * Adds a new metric to the user message.
     * @param {string} name - The key under which the metric will be stored.
     * @param {MetricValue} value - The metric value to store, which can be a string or number.
     * @returns {void}
     */
    public addMetric(name: string, value: MetricValue): void {
        this.metrics[name] = value;
    }

    public addAverageMetrics(metricTracker: MetricTracker<MetricValue>): void {
        this.metrics[metricTracker.getMetricName()] = metricTracker.getAverage();
    }

    /**
     * Calculates the duration of the session in milliseconds.
     * @returns {number} Session duration in milliseconds, or 0 if session hasn't started or ended.
     */
    public getSessionDuration(): number {
        if (this.sessionStart !== null && this.sessionEnd !== null) {
            return (this.sessionEnd - this.sessionStart);
        }
        console.warn("Session duration cannot be calculated without a valid start and end time.");
        return 0;
    }

    /**
     * Checks if the session is currently active.
     * @returns {boolean} True if the session has started and not yet ended.
     */
    public isSessionActive(): boolean {
        return this.sessionStart !== null && this.sessionEnd === null;
    }

    public end(endType: SessionEndType) {
        this.sessionEnd = Date.now();
        this.sessionEndType = endType;
    }

    toJSON(): object {
        const json = {
            "session_id": this.id,
            "user_id": this.userId,
            "session_start": this.sessionStart,
            "session_end": this.sessionEnd,
            "session_end_type": this.sessionEndType,
            "session_duration": this.getSessionDuration()
        };

        Object.assign(json, this.metrics);

        return json;
    }
}