/**
 * Represents the user's input action, including the text input, start time, and end time.
 */
export class UserInputAction {
     /** The timestamp when the user started typing */
    readonly startTimestamp: number;

    /** The timestamp when the user finished typing or updated the input */
    endTimestamp: number;

    /** The text input entered by the user */
    inputText: string;

    /**
     * Initializes a new UserInputAction, setting the start timestamp to the current time.
     */
    constructor() {
        this.startTimestamp = Date.now();
        this.endTimestamp = this.startTimestamp; // Initialize to start time by default
        this.inputText = ''; // Initialize as empty string
    }

    /**
     * Updates the input text and sets the current time as the end timestamp.
     * @param inputText - The text input from the user.
     */
    public update(inputText: string) {
        this.inputText = inputText;
        this.endTimestamp = Date.now();
    }

     /**
     * Calculates the total time the user has been typing, in milliseconds.
     * @returns The total typing time in milliseconds.
     */
     public getTotalTypingTime(): number {
        return this.endTimestamp - this.startTimestamp;
    }
}