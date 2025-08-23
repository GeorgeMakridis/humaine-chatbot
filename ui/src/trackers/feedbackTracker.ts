import { BotMessage } from "../components";
import { Session } from "../models/session";
import { MetricTracker, MetricValue } from "./metricTracker";

export class FeedbackTracker extends MetricTracker<MetricValue> {
    protected metricName: string = "feedback";

     /** Count of positive feedback received */
    private positiveFeedbackCount: number = 0;

     /** Count of positive negative received */
    private negativeFeedbackCount: number = 0;

     /** Total count of bot messages */
    private totalBotMessagesCount: number = 0;

     /** Track the most recent bot message that received negative feedback */
    private lastBotMessageWithNegativeFeedback: BotMessage | null = null;

    /** Track the bot message that immediately follows a message with negative feedback */
    private lastBotMessageAfterNegativeFeedback: BotMessage | null = null;

    /** Count how many times positive feedback follows negative feedback */
    private positiveFeedbackAfterNegativeCount: number = 0;

    /**
     * Called when a new bot message is received.
     * 
     * @param botMessage - The bot message that has been sent.
     */
    public newBotMessage(botMessage: BotMessage) {
        this.totalBotMessagesCount++;

        // If there was a bot message with negative feedback,
        // mark the current bot message as the one following the negative feedback.
        if(this.lastBotMessageWithNegativeFeedback) {
            this.lastBotMessageWithNegativeFeedback = null;
            this.lastBotMessageAfterNegativeFeedback = botMessage;
        } else if(this.lastBotMessageAfterNegativeFeedback) {
            // No negative feedback was received previously, reset
            this.lastBotMessageAfterNegativeFeedback = null;
        }
    }

     /**
     * Called when feedback is received for a bot message.
     * 
     * @param botMessage - The bot message for which feedback is being given.
     */
    public newFeedback(botMessage: BotMessage) {
        const feedback = botMessage.getFeedback();

        if(feedback === 'positive') {
            this.positiveFeedbackCount++;

            // If the current bot message is the one following a message with negative feedback,
            // increment the "positive feedback after negative feedback" count.
            // So, increment the count of "positive feedback after negative feedback."
            if( this.lastBotMessageAfterNegativeFeedback &&
                botMessage.timestamp === this.lastBotMessageAfterNegativeFeedback.timestamp) {
                this.positiveFeedbackAfterNegativeCount++;
                this.lastBotMessageWithNegativeFeedback = null;
               } 
        } else {
            this.negativeFeedbackCount++;
            this.lastBotMessageWithNegativeFeedback = botMessage;
        }
    }

    /**
     * Called when the session ends.
     * Logs the feedback metrics.
     */
    public sessionEnded(session: Session) {
        const totalFeedbackCount = this.positiveFeedbackCount + this.negativeFeedbackCount;

        const metricValues = {
            "total_feedback_count": totalFeedbackCount,
            "total_bot_messages_count": this.totalBotMessagesCount,
            "total_feedback_ratio": totalFeedbackCount / this.totalBotMessagesCount,
            "positive_feedback_count": this.positiveFeedbackCount,
            "positive_feedback_ratio": this.positiveFeedbackCount / totalFeedbackCount,
            "negative_feedback_count": this.negativeFeedbackCount,
            "negative_feedback_ratio": this.negativeFeedbackCount / totalFeedbackCount,
            "positive_follow_up_count": this.positiveFeedbackAfterNegativeCount,
            "feedback_incorporation_rate": this.positiveFeedbackAfterNegativeCount / this.negativeFeedbackCount
        };

        session.addMetric(this.metricName, metricValues);
    }

    public reset() {
        this.positiveFeedbackCount = 0;
        this.negativeFeedbackCount = 0;
        this.totalBotMessagesCount = 0;
        this.lastBotMessageAfterNegativeFeedback = null;
        this.lastBotMessageWithNegativeFeedback = null;
        this.positiveFeedbackAfterNegativeCount = 0;
    }
}