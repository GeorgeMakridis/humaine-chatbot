import { UserMessage } from "../components";
import { MetricTracker, MetricValue } from "./metricTracker";

export class ResponseTimeTracker extends MetricTracker<MetricValue> {
    protected metricName: string = "response_time";

    private messageReceivedTime: number | null = null;

    /**
     * Marks the time when the bot responds.
     */
    public markBotResponse(): void {
        this.messageReceivedTime = Date.now();
    }

    /**
     * Marks the time when the user responds and calculates the response time.
     * @throws Error if markUserResponse is called before markBotResponse.
     */
    public markUserResponse(userMessage: UserMessage): void {
        if (this.messageReceivedTime === null) {
            return;
        }

        const typingStartTime = (userMessage.userInputAction.startTimestamp - this.messageReceivedTime);
        const responseTime = this.calculateResponseTime();
        const metricValues = { 
            "user_response_time": responseTime, 
            "user_typing_start_time": typingStartTime 
        };
        
        this.addValue(metricValues);
        userMessage.addMetric(this.metricName, metricValues);

        // reset to wait for next bot message.
        this.messageReceivedTime = null
    }

    /**
     * Calculates the response time in seconds.
     * @returns {number} The calculated response time in seconds.
     */
    private calculateResponseTime(): number {
        const currentTime = Date.now();
        const responseTime = (currentTime - this.messageReceivedTime) / 1000;
        return responseTime;
    }

    /**
     * Optionally resets the tracker if needed, especially after a session ends.
     */
    public reset(): void {
        this.messageReceivedTime = null; // Reset the last bot response time
        super.reset(); // Reset the values stored in the base class
    }
}
