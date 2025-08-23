import { SessionEndType } from "../types/sessionType";
import { MetricTracker, MetricValue } from "./metricTracker";

export class SessionDurationTracker extends MetricTracker<MetricValue> {
    protected metricName: string = "sessionDuration";

    private sessionStart: number | null = null;
    private sessionEnd: number | null = null;
    private sessionEndType: SessionEndType | null = null;

    /**
     * Starts the session timer by recording the current timestamp.
     */
    public startSession(): void {
        this.sessionStart = Date.now();
        this.sessionEnd = null;  // Reset end time in case of a new session
        this.logMetrics();
    }

    /**
     * Ends the session timer by recording the current timestamp.
     */
    public endSession(endType: SessionEndType): void {
        if (this.sessionStart !== null) {
            this.sessionEnd = Date.now();
            this.sessionEndType = endType;
            this.logMetrics();
        } else {
            console.warn("Session has not started. Cannot end session.");
        }
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

    protected logMetrics() {

        const json: {
            metric: string;
            sessionStart: number;
            sessionEnd?: number;
            sessionEndType?: string;
            sessionDuration?: number;
        } = {
            metric: this.metricName,
            sessionStart: this.sessionStart,
        };

        if(!this.isSessionActive()) {
            json.sessionEnd = this.sessionEnd;
            json.sessionEndType = this.sessionEndType,
            json.sessionDuration = this.getSessionDuration()
        }

        this.loggingService.send(json);
    }
}
