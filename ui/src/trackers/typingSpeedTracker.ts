import { MetricTracker, MetricValue } from "./metricTracker";
import { UserInputAction } from "../models/userInputAction";
import { UserMessage } from "../models/userMessage";

export class TypingSpeedTracker extends MetricTracker<MetricValue> {
    protected metricName: string = "typing_speed";

    /**
     * Adds typing speed to the metric tracker after calculating it from user input.
     * @param userMessage The user message containing user input details for typing speed calculation.
     */
    public addTypingSpeed(userMessage: UserMessage): void {

        // The total time it takes for the user to type and send their message, 
        // measured from the moment they start typing until they send the message.
        const duration = this.calculateDurationInSeconds(userMessage.userInputAction);

        // Check for non-positive duration to prevent division by zero or invalid speed
        if (duration <= 0) {
            console.warn("Invalid time duration. Typing speed cannot be calculated.");
            return;
        }

        // The total number of characters in the user’s message, 
        // used to assess the length of the message in relation to typing speed.
        const messageLength = userMessage.userInputAction.inputText.length;

        // The speed at which the user types,
        // calculated as the message length divided by the duration in seconds.
        const typingSpeed = messageLength / duration;

        const metricValues = { 
            "duration": duration, 
            "message_length": messageLength, 
            "typing_speed": typingSpeed
        };

        this.addValue(metricValues);
        userMessage.addMetric(this.metricName, metricValues);
    }

    private calculateDurationInSeconds(userInputAction: UserInputAction) {
        // Calculate the duration in seconds (timestamps are in milliseconds)
        return (userInputAction.endTimestamp - userInputAction.startTimestamp) / 1000;
    }
}