import { BotMessage } from "../models/botMessage";
import { Message } from "../models/message";
import { Session } from "../models/session";
import { UserMessage } from "../models/userMessage";
import { GrammaticalMistakesTracker } from "../trackers/grammaticalMistakesTracker";
import { LanguageComplexityTracker } from "../trackers/languageComplexityTracker";
import { SentimentTracker } from "../trackers/sentimentTracker";
import { LoggingService } from "./loggingService";

export class DialogueAnalysis {
    private loggingService: LoggingService = new LoggingService();
    
    private sentimentTracker: SentimentTracker;
    private grammaticalMistakesTracker: GrammaticalMistakesTracker;
    private languageComplexityTracker: LanguageComplexityTracker;

    constructor(langCode: string, assetsPath: string) {
        this.sentimentTracker = new SentimentTracker(this.loggingService);
        this.grammaticalMistakesTracker = new GrammaticalMistakesTracker(this.loggingService, langCode, assetsPath);
        this.languageComplexityTracker = new LanguageComplexityTracker(this.loggingService);
    }

    public newMessage(message: Message) {
        if (message instanceof UserMessage) {
            this.newUserMessage(message as UserMessage);
        } 
        else if (message instanceof BotMessage) {
            // Not processing new bot messages.
        } 
        else {
            console.error("Unknown message type:", message);
        }
    }
    public sessionEnded(session: Session) {
        session.addAverageMetrics(this.sentimentTracker);
        session.addAverageMetrics(this.grammaticalMistakesTracker);
        session.addAverageMetrics(this.languageComplexityTracker);
    }
    public reset() {
        this.sentimentTracker.reset();
        this.grammaticalMistakesTracker.reset();
        this.languageComplexityTracker.reset();
    }

    private newUserMessage(userMessage: UserMessage) {
        this.sentimentTracker.addUserMessage(userMessage);
        this.grammaticalMistakesTracker.addUserMessage(userMessage);
        this.languageComplexityTracker.addUserMessage(userMessage);
    }
}