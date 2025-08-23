import { BotMessage } from "./botMessage";
import { UserMessage } from "./userMessage";

export class ConversationTurn {
    userMessage: UserMessage;
    botMessage: BotMessage;

    constructor(userMessage: UserMessage, botMessage: BotMessage) {
        this.userMessage = userMessage;
        this.botMessage = botMessage;
    }
}