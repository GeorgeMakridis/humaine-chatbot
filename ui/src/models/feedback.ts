import { FeedbackType } from "../types/feedbackType";
import { BotMessage } from "./botMessage";

export class Feedback {
    sessionId: string;
    userId: string;
    type: FeedbackType;
    botMessage: BotMessage;

    constructor(botMessage: BotMessage) {
        this.type = botMessage.getFeedback();
        this.botMessage = botMessage;
    }

    toJSON(): object {
        return  {
            "session_id": this.sessionId,
            "user_id": this.userId,
            "response_text": this.botMessage.text,
            "response_start_time": this.botMessage.timestamp,
            "response_end_time": this.botMessage.endTimestamp,
            "response_duration": this.botMessage.getDuration(),
            "feedback_type": this.botMessage.getFeedback(),
            "feedback_time": this.botMessage.feedbackTimestamp,
            "feedback_delay_duration": this.botMessage.getFeedbackDelay()
        };
    }
}