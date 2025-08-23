import { BotMessage } from "../models/botMessage";
import { Message } from "../models/message";
import { ResponseTimeTracker } from "../trackers/responseTimeTracker";
import { TypingSpeedTracker } from "../trackers/typingSpeedTracker";
import { UserMessage } from "../models/userMessage";
import { LoggingService } from "./loggingService";
import { EngagementTracker } from "../trackers/engagementTracker";
import { FeedbackTracker } from "../trackers/feedbackTracker";
import { Session } from "../models/session";

export class MetricsCollector {
    private loggingService: LoggingService = new LoggingService();

    private idleTracker: EngagementTracker;
    private responseTimeTracker : ResponseTimeTracker;
    private typingSpeedTracker: TypingSpeedTracker;
    private feedbackTracker: FeedbackTracker;

    constructor() {
        this.idleTracker = new EngagementTracker(this.loggingService);
        this.responseTimeTracker = new ResponseTimeTracker(this.loggingService);
        this.typingSpeedTracker = new TypingSpeedTracker(this.loggingService);
        this.feedbackTracker = new FeedbackTracker(this.loggingService);
    }

    public sessionEnded(session: Session) {
        this.idleTracker.sessionEnded(session);
        this.feedbackTracker.sessionEnded(session);

        session.addAverageMetrics(this.responseTimeTracker);
        session.addAverageMetrics(this.typingSpeedTracker);

        this.resetTrackers();
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
    public messageUpdated(message: Message) {
        if (message instanceof UserMessage) {
            // Not processing updated user messages.
        } 
        else if (message instanceof BotMessage) {
            this.updatedBotMessage(message as BotMessage);
        } 
        else {
            console.error("Unknown message type:", message);
        }
    }

    public feedbackReceived(botMessage: BotMessage) {
        this.feedbackTracker.newFeedback(botMessage);
    }

    private newUserMessage(userMessage: UserMessage) {
        this.responseTimeTracker.markUserResponse(userMessage);
        this.typingSpeedTracker.addTypingSpeed(userMessage);
        this.idleTracker.newUserMessage(userMessage);
    }
    private updatedBotMessage(botMessage: BotMessage) {
        this.responseTimeTracker.markBotResponse();
        this.idleTracker.newBotMessage(botMessage);
        this.feedbackTracker.newBotMessage(botMessage);
    }

    private resetTrackers() {
        this.responseTimeTracker.reset();
        this.typingSpeedTracker.reset();
        this.idleTracker.reset();
        this.feedbackTracker.reset();
    }
}