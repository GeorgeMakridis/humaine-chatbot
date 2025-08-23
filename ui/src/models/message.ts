import { generateSimpleUniqueId } from "../utils/utils";

/**
 * Represents a message in a conversation between a user, bot, or system.
 */
export class Message {
     /** Unique identifier for the message */
    id: string = generateSimpleUniqueId();

    /** The sender of the message: 'User', 'Bot', or 'System' */
    sender: MessageSender;

    /** The content of the message */
    text: string;

    /** Timestamp of when the message was created */
    timestamp: number;

    /**
     * Creates an instance of a Message.
     * @param sender - The sender of the message ('User', 'Bot', or 'System')
     * @param text - The text content of the message
     * @param id - Optional. The unique identifier for the message. If not provided, a new ID is generated.
     * @param timestamp - Optional. The timestamp of the message creation. If not provided, the current time is used.
     */
    protected constructor(sender: MessageSender, text: string, id?: string, timestamp?: number) {
        this.id = id ?? generateSimpleUniqueId();
        this.sender = sender;
        this.text = text;
        this.timestamp = timestamp ?? Date.now();
    }

    /**
     * Formats the timestamp into a readable time string.
     * @param locale - Optional. The locale to format the time string (defaults to system locale).
     * @returns The formatted time string.
     */
    getFormattedTimestamp(locale?: string): string {
        return new Date(this.timestamp).toLocaleTimeString(locale ?? undefined);
    }
}

/** Defines the allowed types for message senders */
type MessageSender = 'User' | 'Bot' | 'System';