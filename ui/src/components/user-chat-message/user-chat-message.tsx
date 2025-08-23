import { Component, Prop, h } from '@stencil/core';
import { UserMessage } from '../../models/userMessage';

@Component({
    tag: 'user-chat-message',
    styleUrl: 'user-chat-message.css',
    shadow: true
})
export class UserChatMessage {
    @Prop() message: UserMessage;

    render() {
        return (
            <div class='user-message'>
                <span>{this.message.text}</span>
                <span class="timestamp">{this.message.getFormattedTimestamp()}</span>
            </div>
        );
    }
}
