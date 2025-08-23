import { FeedbackType } from "../types/feedbackType";
import { Message } from "./message";

/**
 * Represents a message sent by the bot.
 * It tracks whether the response is still pending and calculates the duration of the response.
 */
export class BotMessage extends Message {
     /** Indicates whether the bot's response is pending */
    isPending: boolean = true;

    /** The timestamp when the bot finishes responding */
    endTimestamp: number | null = null;

    /** Stores the feedback from the user (either 'positive', 'negative', or null if no feedback has been provided) */
    feedback: FeedbackType | null = null;

    /** The timestamp when the feedback is given */
    feedbackTimestamp: number | null = null;

    /**
     * Initializes a new BotMessage with default values.
     */
    constructor() {
        super('Bot', '');
    }

    /**
     * Sets the bot's response text and marks the response as complete.
     * Also records the end timestamp of the response.
     * 
     * @param text - The bot's response text.
     */
    public setResponse(text: string) {
        this.text = text;
        this.isPending = false;
        this.endTimestamp = Date.now();
    }

    /**
     * Creates a deep copy of the current BotMessage.
     * 
     * @returns A new BotMessage instance with identical properties.
     */
    public deepCopy(): BotMessage {
        return Object.assign(new BotMessage(), this);
    }

     /**
     * Calculates the duration between when the message was created and when the bot finished responding.
     * If the end timestamp is not set, it calculates the duration up to the current time.
     * 
     * @returns The duration in milliseconds.
     */
     public getDuration(): number {
        const endTime = this.endTimestamp ?? Date.now(); // If endTimestamp is null, use the current time
        return endTime - this.timestamp; // Return the duration in milliseconds
    }

    /**
     * Sets the feedback provided by the user (either 'positive' or 'negative').
     * This method allows the feedback state to be updated for this message.
     * 
     * @param feedback - The feedback value, which can either be 'positive' or 'negative'.
     */
    public setFeedback(feedback: FeedbackType) {
        this.feedback = feedback;
        this.feedbackTimestamp = Date.now();
    }

    public getFeedbackDelay() {
        if(this.feedback == null) return -1;
        return this.feedbackTimestamp - this.endTimestamp;
    }
    
    /**
     * Gets the current feedback provided by the user for this message.
     * If no feedback has been provided yet, it returns null.
     * 
     * @returns The current feedback, either 'positive', 'negative', or null if no feedback has been given.
     */
    public getFeedback() {
        return this.feedback;
    }
}