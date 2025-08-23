import { MetricValue } from "../trackers/metricTracker";
import { Message } from "./message";
import { UserInputAction } from "./userInputAction";

// Dictionary to store multiple MetricValue objects
export interface MetricDictionary {
    [key: string]: MetricValue; // Each key maps to a MetricValue
}

/**
 * Represents a message sent by the user, extending the base Message class.
 * Captures additional information such as user input action.
 */
export class UserMessage extends Message {
    /** The user's input action, which includes the text and timestamps of the action */
    readonly userInputAction: UserInputAction;

    /** The message related metrics */
    metrics: MetricDictionary = {};

    /**
     * Creates an instance of UserMessage.
     * @param userInputAction - The action taken by the user, including input text and start timestamp.
     */
    constructor(userInputAction: UserInputAction) {
        super('User', userInputAction.inputText);
        this.userInputAction = userInputAction;
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
}