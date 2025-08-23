import { Component, Prop, h } from '@stencil/core';
import { Message } from '../../components';

@Component({
    tag: 'system-chat-message',
    styleUrl: 'system-chat-message.css',
    shadow: true,
})
export class SystemChatMessage {
    @Prop() message: Message;
    render() {
        return (
            <div class='container'>
                {this.message.text}
            </div>
        );
    }
}
