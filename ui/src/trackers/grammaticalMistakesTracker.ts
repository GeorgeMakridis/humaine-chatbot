import { UserMessage } from "../components";
import { LoggingService } from "../services/loggingService";
import { MetricTracker, MetricValue } from "./metricTracker";
import Typo from 'typo-js'; // https://github.com/cfinke/Typo.js

export class GrammaticalMistakesTracker extends MetricTracker<MetricValue> {
    protected metricName: string = "grammar";
    private typo: any;

    constructor(loggingService: LoggingService, langCode: string, assetsPath: string) {
        super(loggingService);
        const dictionaryPath = `${assetsPath}/dictionaries`;
        this.typo = new Typo(langCode, false, false, { dictionaryPath: dictionaryPath });
    }

    public addUserMessage(userMessage: UserMessage): void {
        const inputText = userMessage.userInputAction.inputText;
        const mistakes = this.countMistakes(inputText);
        const totalWords = this.countWords(inputText);

        if (totalWords > 0) {
            //The frequency of grammatical mistakes in the user's message, 
            // calculated as the ratio of grammatical mistakes to the total number of words in the message.
            const frequency = mistakes / totalWords;

            const metricValues = { 
                "total_words_count": totalWords, 
                "mistakes_count": mistakes, 
                "grammatical_mistakes_frequency": frequency 
            }; 

            this.addValue(metricValues);
            userMessage.addMetric(this.metricName, metricValues);
        }
    }

    /** 
     * Counts the total number of grammatical mistakes identified in the user's message.
     * @param text The user message text content.
     * */
    private countMistakes(text: string): number {
        // Remove all punctuation and special characters except for apostrophes in contractions
        // Keep letters, digits, whitespace, and apostrophes
        const sanitizedText = text.replace(/[^\w\s']|_/g, "").toLowerCase(); 
        const words = sanitizedText.split(/\s+/); // Split the text into words
        let mistakes = 0;

        for (const word of words) {
            if (word === "") continue;
            if (!this.typo.check(word)) {
                mistakes++;
            }
        }
        
        return mistakes; // Return the total number of mistakes found
    }

    /** 
     * Counts the total number of words in the user's message, 
     * It's used to calculate the grammatical mistakes frequency relative to the message's length 
     * @param text The user message text content.
     * */
    private countWords(text: string): number {
        return text.trim().split(/\s+/).length; // Count words by splitting the text on whitespace
    }
}
