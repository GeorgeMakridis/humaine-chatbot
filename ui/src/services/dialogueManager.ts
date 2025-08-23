import { BotMessage } from "../models/botMessage";
import { ChatServiceConfig } from "../models/chatServiceConfig";
import { Feedback } from "../models/feedback";
import { Message } from "../models/message";
import { Session } from "../models/session";
import { UserMessage } from "../models/userMessage";
import { UserPrompt } from "../models/userPrompt";
import { SessionEndType } from "../types/sessionType";
import { ChatService } from "./chatService";
import { DialogueAnalysis } from "./dialogueAnalysis";
import { MetricsCollector } from "./metricsCollector";
import { generateSimpleUniqueId } from "../utils/utils";

/**
 * Manages the dialogue between the user and the chatbot.
 * Handles sending user messages and receiving bot responses.
 */
export class DialogueManager extends EventTarget {
    static EVENT_MESSAGE_ADDED = "messageAdded";
    static EVENT_MESSAGE_UPDATED = "messageUpdated";

    private dialogueAnalysis: DialogueAnalysis;
    private metricsCollector: MetricsCollector;
    private chatService: ChatService;
    private messages: Message[];

    // User ID is generated locally for demo purposes
    // In production, this could be coordinated with the server
    private userId: string = generateSimpleUniqueId();
    private session: Session | null;

    constructor(serviceConfig: ChatServiceConfig, langCode: string, assetsPath: string) {
        super();

        this.chatService = new ChatService(serviceConfig);
        this.dialogueAnalysis = new DialogueAnalysis(langCode, assetsPath);
        this.metricsCollector = new MetricsCollector();
        this.messages = [];
    }

    /**
     * Start the dialogue session.
     */
    public startSession() {
        this.session = new Session(this.userId);
    }

    /**
     * End the dialogue session with reason.
     * @param endType The reason the session ended.
     */
    public endSession(endType: SessionEndType) {
        this.session.end(endType);
        this.dialogueAnalysis.sessionEnded(this.session);
        this.metricsCollector.sessionEnded(this.session);

        this.sendSessionData(this.session);
    }

    /**
     * Sends a user message to the bot and processes the bot's response.
     * @param message The message object containing the user's message.
     */
    public async sendUserMessage(message: Message) {
        const userMessage = message as UserMessage;

        // Add and process the user message.
        this.dialogueAnalysis.newMessage(userMessage);
        this.metricsCollector.newMessage(userMessage);
        this.addMessage(userMessage);

        // Add an empty bot message to show the typing indicator.
        const botMessage = new BotMessage();
        this.addMessage(botMessage);

        const userPrompt = new UserPrompt(this.session.id, this.userId, userMessage);
        try {
            const botResponse = await this.chatService.sendMessage(userPrompt);
            botMessage.setResponse(botResponse);
            this.metricsCollector.messageUpdated(botMessage);
            
            this.invokeMessageUpdated(botMessage);
        } catch(error) {
            // Handle error gracefully - show error message to user
            console.error("Error sending message to chat service:", error);
            botMessage.setResponse("I'm sorry, I encountered an error. Please try again.");
            this.metricsCollector.messageUpdated(botMessage);
            this.invokeMessageUpdated(botMessage);
        }    
    }

    /**
     * Sends user feedback on the last bot's response.
     * @param feedback positive or negative feedback.
     */
    public async sendMessageFeedback(feedback: Feedback) {
        feedback.sessionId = this.session.id;
        feedback.userId = this.userId;
        
        this.metricsCollector.feedbackReceived(feedback.botMessage);
        
        if (feedback.type === 'negative') {
            this.sendNegativeFeedback(feedback);
        } else if (feedback.type === 'positive') {
            this.sendPositiveFeedback(feedback);
        }
    }

    public async sendSessionData(session: Session) {
        try {
            const response = await this.chatService.sendSession(session);
            console.log("Session data sent successfully:", response);
            this.session = null;
            this.reset(); 
        } catch(error) {
            // Handle session data sending error gracefully
            console.error("Error sending session data to chat service:", error);
            // Don't fail the session end process, just log the error
            this.session = null;
            this.reset();
        }  
    }

    /**
     * Adds a message to the conversation history.
     * @param message The message object to be added.
     */
    private addMessage(message: Message) {
        this.messages.push(message);
        this.invokeMessageAdded(message);
    }

    private async sendNegativeFeedback(feedback: Feedback) {

        // Add an empty bot message to show the typing indicator.
        const botMessage = new BotMessage();
        this.addMessage(botMessage);

        try {
            const botResponse = await this.chatService.sendFeedback(feedback);
            botMessage.setResponse(botResponse);
            
            this.invokeMessageUpdated(botMessage);
        } catch(error) {
            // TODO process error.
            console.error("Error sending message to chat service:", error);
        }  
    }
    private async sendPositiveFeedback(feedback: Feedback) {
        try {
            await this.chatService.sendFeedback(feedback);
        } catch(error) {
            // TODO process error.
            console.error("Error sending message to chat service:", error);
        }  
    }

     /**
     * Dispatches an event indicating that a new message has been added.
     * @param message The message object that was added.
     */
    private invokeMessageAdded(message: Message) {
        this.invokeMessageEvent(message, DialogueManager.EVENT_MESSAGE_ADDED);
    }
     /**
     * Dispatches an event indicating that a message has been updated.
     * @param message The message object that has been updated.
     */
    private invokeMessageUpdated(message: Message) {
        this.invokeMessageEvent(message, DialogueManager.EVENT_MESSAGE_UPDATED);
    }
    /**
     * Dispatches a custom event with message details.
     * @param message The message object to include in the event.
     * @param eventName The name of the event to dispatch.
     */
    private invokeMessageEvent(message: Message, eventName: string) {
        this.dispatchEvent(new CustomEvent(eventName, {
            detail: { message: message }
        }));
    }

    private reset() {
        this.messages = [];
        this.dialogueAnalysis.reset();
    }
}