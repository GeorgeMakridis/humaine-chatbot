import { ChatServiceConfig } from "../models/chatServiceConfig";
import { Feedback } from "../models/feedback";
import { Session } from "../models/session";
import { UserPrompt } from "../models/userPrompt";

export class ChatService {
    private apiKey: string;
    private baseUrl: string;

    constructor(config: ChatServiceConfig) {
        this.baseUrl = config.baseUrl;
        this.apiKey = config.apiKey;
    }

    public async sendMessage(userPrompt: UserPrompt): Promise<string> {
        console.log("Sending message to HumAIne backend:", JSON.stringify(userPrompt.toJSON(), null, 2));

        try {
            const response = await fetch(`${this.baseUrl}/interact`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.apiKey}`
                },
                body: JSON.stringify(userPrompt.toJSON())
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }

            const data = await response.json();
            console.log("Backend response:", data);
            
            // Extract message from backend response format
            return data.message || "I'm sorry, I didn't receive a proper response.";
        } catch (error) {
            console.error('Error sending message to HumAIne backend:', error);
            // Return a user-friendly error message
            return "I'm sorry, I'm having trouble connecting right now. Please try again in a moment.";
        }
    }

    public async sendFeedback(feedback: Feedback): Promise<string> {
        console.log("Sending feedback to HumAIne backend:", JSON.stringify(feedback, null, 2));

        try {
            const response = await fetch(`${this.baseUrl}/feedback`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.apiKey}`
                },
                body: JSON.stringify(feedback)
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }

            const data = await response.json();
            console.log("Feedback response:", data);
            
            // Extract message from backend response format
            return data.message || "Feedback received. Thank you!";
        } catch (error) {
            console.error('Error sending feedback to HumAIne backend:', error);
            // Return a user-friendly message even if feedback fails
            return "Feedback received. Thank you!";
        }
    }

    public async sendSession(session: Session): Promise<string> {
        console.log("Sending session data to HumAIne backend:", JSON.stringify(session, null, 2));

        try {
            const response = await fetch(`${this.baseUrl}/session`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.apiKey}`
                },
                body: JSON.stringify(session)
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }

            const data = await response.json();
            console.log("Session response:", data);
            
            // Extract message from backend response format
            return data.message || "Session data recorded.";
        } catch (error) {
            console.error('Error sending session data to HumAIne backend:', error);
            // Return a user-friendly message even if session recording fails
            return "Session data recorded.";
        }
    }
}