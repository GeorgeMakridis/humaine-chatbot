import { Component, Event, EventEmitter, Prop, h } from '@stencil/core';
import { Message } from '../../models/message';
import { BotMessage, UserMessage } from '../../components';

@Component({
    tag: 'chat-messages',
    styleUrl: 'chat-messages.css',
    shadow: true
})
export class ChatMessages {
    @Prop() messages: Message[];
    @Event() feedbackReceived: EventEmitter<BotMessage>;

    private container: HTMLDivElement;

    componentDidLoad() {
        this.scrollToBottom();
    }

    componentDidUpdate() {
        this.scrollToBottom();
    }

    scrollToBottom() {
        requestAnimationFrame(() => {
            this.container.scrollTop = this.container.scrollHeight;
        });
    }

    handleFeedback(event: CustomEvent) {
        const botMessage = event.detail as BotMessage;
        this.feedbackReceived.emit(botMessage);
    }

    render() {
        return (
            <div class="chat-logs" ref={(el) => (this.container = el as HTMLDivElement)}>
                {this.messages.map((msg, index) => (
                    msg.sender === 'User' ? (
                        <user-chat-message message={msg as UserMessage}></user-chat-message>
                    ) : msg.sender === 'Bot' ? (
                        <bot-chat-message
                            message={msg as BotMessage}
                            isLast={index === this.messages.length - 1}
                            onFeedbackGiven={(event) => this.handleFeedback(event)}
                        ></bot-chat-message>
                    ) : (
                        <system-chat-message message={msg}></system-chat-message>
                    )
                ))}
            </div>
        );
    }
}
