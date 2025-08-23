import { UserMessage } from "../components";
import { LoggingService } from "../services/loggingService";
import { MetricTracker, MetricValue } from "./metricTracker";
import Sentiment from "sentiment"; // https://github.com/thisandagain/sentiment

export class SentimentTracker extends MetricTracker<MetricValue> {
    protected metricName: string = "sentiment";

    private sentiment: Sentiment;

    constructor(loggingService: LoggingService) {
        super(loggingService);
        this.sentiment = new Sentiment();
    }

    /**
     * Analyzes the sentiment of the user message and adds the sentiment score to the metric tracker.
     * @param userMessage The user message containing the input text.
     */
    public addUserMessage(userMessage: UserMessage): void {
        const inputText = userMessage.userInputAction.inputText; // Get the input text from the user action
        
        // Analyze the sentiment of the input text
        const sentimentResult = this.sentiment.analyze(inputText);
        
        const score = sentimentResult.score;
        const comparative = sentimentResult.comparative;
        const metricValues ={
            "sentiment_score": score, 
            "normalized_sentiment_score": comparative
        }; 
        
        // Add the sentiment score to the metric tracker
        this.addValue(metricValues);

        // Add metric to user message
        userMessage.addMetric(this.metricName, metricValues);
    }
}
