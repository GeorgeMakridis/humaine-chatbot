import { UserMessage } from "./userMessage";

export class UserPrompt {
    sessionId: string;
    userId: string;
    userMessage: UserMessage;

    constructor(sessionId: string, userId: string, userMessage: any) {
        this.sessionId = sessionId;
        this.userId = userId;
        this.userMessage = userMessage;        
    }

    toJSON(): object {
        const json = {
            "session_id": this.sessionId,
            "user_id": this.userId,
            "input_text": this.userMessage.userInputAction.inputText,
            "input_start_time": this.userMessage.userInputAction.startTimestamp,
            "input_end_time": this.userMessage.userInputAction.endTimestamp,
            "input_sent_time": Date.now()
        };

        Object.assign(json, this.userMessage.metrics);

        return json;
    }
}