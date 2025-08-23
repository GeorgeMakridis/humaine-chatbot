import { MetricTracker, MetricValue } from "./metricTracker";
import { LoggingService } from "../services/loggingService";
import { UserMessage } from "../models/userMessage";
import { BotMessage } from "../models/botMessage";
import { Session } from "../models/session";

/**
 * The EngagementTracker class tracks user and bot interaction engagement metrics, such as active time, idle time,
 * and total engagement time, during a session. It measures the time spent in communication and inactivity.
 */
export class EngagementTracker extends MetricTracker<MetricValue> {
     /** The name of the metric being tracked */
    protected metricName: string = "engagement";

    /** The timestamp of the last bot message */
    private lastMessageTimestamp: number | null = null;

    /** Time gap threshold (in milliseconds) to be considered "idle": 5 seconds */
    private messageGapLimit: number = 5 * 1000; 

    /** Total time (ms) during the session when the user was inactive
     * calculated as the sum of time gaps between consecutive messages 
     * that exceed a predefined threshold (e.g., 5 seconds).
     * */
    private idleTime: number = 0;

    /** Total time (ms) during the session when the user was active, 
     * calculated as the difference between the session duration and the idle time.
     * */
    private activeTime: number = 0;

    /** Total time (ms) spent interacting during the session, 
     * calculated as the sum of all periods when the user is typing or the chatbot is replying.
     **/
    private engagementTime: number = 0;

    constructor(loggingService: LoggingService) {
        super(loggingService);
        this.lastMessageTimestamp = Date.now();
    }

    /**
     * Processes a new user message and calculates the engagement time.
     * If the time gap since the last message exceeds the idle threshold, the idle time is updated.
     * The typing time for the user message is added to the engagement time.
     * 
     * @param userMessage - The user message containing typing details.
     */
    public newUserMessage(userMessage: UserMessage) {
        const currentTimestamp = Date.now();
        const timeGap = currentTimestamp - this.lastMessageTimestamp;

        // If the time gap exceeds the idle time limit, accumulate idle time
        if (timeGap > this.messageGapLimit) {
            this.idleTime += timeGap;
        }

        // Add the user's typing time to the total engagement time
        this.engagementTime += userMessage.userInputAction.getTotalTypingTime();
    }

    /**
     * Processes a new bot message and updates the last message timestamp.
     * The duration of the bot's response is added to the total engagement time.
     * 
     * @param botMessage - The bot message containing response duration details.
     */
    public newBotMessage(botMessage: BotMessage) {
        this.lastMessageTimestamp = Date.now();
        this.engagementTime += botMessage.getDuration();
    }

    /**
     * Finalizes the session by calculating the total active time, 
     * subtracting idle time from the total session duration.
     * Logs the engagement metrics after the session ends.
     * 
     * @param duration - The total duration of the session (in milliseconds).
     */
    public sessionEnded(session: Session) {
        this.activeTime = session.getSessionDuration() - this.idleTime;

        const metricValues = {
            "idle_time": this.idleTime,
            "active_time": this.activeTime,
            "engagement_time": this.engagementTime
        };

        session.addMetric(this.metricName, metricValues);
        // this.logMetrics();
    }

    /**
     * Resets the engagement tracker for a new session 
     * by clearing the idle time and resetting the last message timestamp.
     */
    public reset(): void {
        this.idleTime = 0;
        this.lastMessageTimestamp = Date.now();
    }
}