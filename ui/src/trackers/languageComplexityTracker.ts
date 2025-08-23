import { UserMessage } from "../components";
import { LoggingService } from "../services/loggingService";
import { MetricTracker, MetricValue } from "./metricTracker";

export class LanguageComplexityTracker extends MetricTracker<MetricValue> {
    protected metricName: string = "language_complexity";
    private alpha: number;
    private beta: number;

    constructor(loggingService: LoggingService, alpha: number = 0.5, beta: number = 0.5) {
        super(loggingService);
        this.alpha = alpha; 
        this.beta = beta;
    }

    public addUserMessage(userMessage: UserMessage): void {
        const inputText = userMessage.userInputAction.inputText; // Get the input text from the user action

        const sentences = this.splitIntoSentences(inputText);
        const totalWords = this.countWords(inputText);
        const uniqueWords = this.countUniqueWords(inputText);

        const averageSentenceLength = this.calculateAverageSentenceLength(sentences);
        const typeTokenRatio = this.calculateTypeTokenRatio(uniqueWords, totalWords);
        const complexity = this.calculateLanguageComplexity(averageSentenceLength, typeTokenRatio);

        const metricValue = {
            "message_average_sentence_length": averageSentenceLength,
            "type_token_ratio": typeTokenRatio,
            "complexity_of_language": complexity
        };

        this.addValue(metricValue);
        userMessage.addMetric(this.metricName, metricValue);
    }

    private splitIntoSentences(text: string): string[] {
        // Simple split based on punctuation. This can be refined.
        return text.split(/[.!?]+/).filter(Boolean).map(sentence => sentence.trim());
    }

    private countWords(text: string): number {
        return text.split(/\s+/).filter(Boolean).length;
    }

    private countUniqueWords(text: string): number {
        const words = text.split(/\s+/).filter(Boolean);
        const uniqueWords = new Set(words.map(word => word.toLowerCase())); // Convert to lowercase for uniqueness
        return uniqueWords.size;
    }

    private calculateAverageSentenceLength(sentences: string[]): number {
        const totalWords = sentences.reduce((sum, sentence) => sum + this.countWords(sentence), 0);
        return sentences.length > 0 ? totalWords / sentences.length : 0;
    }

    private calculateTypeTokenRatio(uniqueWords: number, totalWords: number): number {
        return totalWords > 0 ? uniqueWords / totalWords : 0;
    }

    private calculateLanguageComplexity(averageSentenceLength: number, typeTokenRatio: number): number {
        return this.alpha * averageSentenceLength + this.beta * typeTokenRatio;
    }
}
