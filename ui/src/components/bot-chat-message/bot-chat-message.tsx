import { Component, Prop, State, Event, h, EventEmitter } from '@stencil/core';
import { BotMessage } from '../../models/botMessage';
import { FeedbackType } from '../../types/feedbackType';

@Component({
    tag: 'bot-chat-message',
    styleUrl: 'bot-chat-message.css',
    shadow: true,
})
export class BotChatMessage {
    @Prop() message: BotMessage;
    @Prop() isLast: boolean;
    @State() feedback: FeedbackType | null = null;
    @Event() feedbackGiven: EventEmitter<BotMessage>;

    handleFeedback(feedback: FeedbackType) {
        this.feedback = feedback;
        this.message.setFeedback(feedback);
        this.feedbackGiven.emit(this.message);
    }

    startSpeechToText() {
        console.log('Speech-to-text initiated');
        // TODO Add your speech-to-text logic here
    }

    render() {
        return (
            <div class='bot-message'>
                {this.message.isPending ? (
                    <div class="typing-indicator">
                        <span class="dot"></span>
                        <span class="dot"></span>
                        <span class="dot"></span>
                    </div>
                ) : (
                    <div>
                        <div class="message-content">
                            <span>{this.message.text}</span>
                            <span class="timestamp">{this.message.getFormattedTimestamp()}</span>
                        </div>
                        <div class="message-controls">
                            {this.feedback === null && this.isLast && (
                                <div>
                                    <button
                                        class="feedback-button like"
                                        title="Like"
                                        onClick={() => this.handleFeedback('positive')}
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#5e5e5e"><path d="M720-120H280v-520l280-280 50 50q7 7 11.5 19t4.5 23v14l-44 174h258q32 0 56 24t24 56v80q0 7-2 15t-4 15L794-168q-9 20-30 34t-44 14Zm-360-80h360l120-280v-80H480l54-220-174 174v406Zm0-406v406-406Zm-80-34v80H160v360h120v80H80v-520h200Z" /></svg>
                                    </button>
                                    <button
                                        class="feedback-button dislike"
                                        title="Dislike"
                                        onClick={() => this.handleFeedback('negative')}
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#5e5e5e"><path d="M240-840h440v520L400-40l-50-50q-7-7-11.5-19t-4.5-23v-14l44-174H120q-32 0-56-24t-24-56v-80q0-7 2-15t4-15l120-282q9-20 30-34t44-14Zm360 80H240L120-480v80h360l-54 220 174-174v-406Zm0 406v-406 406Zm80 34v-80h120v-360H680v-80h200v520H680Z" /></svg>
                                    </button>
                                </div>
                            )}
                            {this.feedback === 'positive' && (
                                <div class="feedback-indicator">
                                    <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#5e5e5e"><path d="M720-120H320v-520l280-280 50 50q7 7 11.5 19t4.5 23v14l-44 174h218q32 0 56 24t24 56v80q0 7-1.5 15t-4.5 15L794-168q-9 20-30 34t-44 14ZM240-640v520H80v-520h160Z" /></svg>
                                </div>
                            )}
                            {this.feedback === 'negative' && (
                                <div class="feedback-indicator">
                                    <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#5e5e5e"><path d="M240-840h400v520L360-40l-50-50q-7-7-11.5-19t-4.5-23v-14l44-174H120q-32 0-56-24t-24-56v-80q0-7 1.5-15t4.5-15l120-282q9-20 30-34t44-14Zm480 520v-520h160v520H720Z" /></svg>
                                </div>
                            )}
                            <button
                                class="speech-to-text-button"
                                title="Speech-to-Text"
                                onClick={() => this.startSpeechToText()}
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#5e5e5e">
                                    <path d="M160-80q-33 0-56.5-23.5T80-160v-640q0-33 23.5-56.5T160-880h326l-80 80H160v640h440v-80h80v80q0 33-23.5 56.5T600-80H160Zm80-160v-80h280v80H240Zm0-120v-80h200v80H240Zm360 0L440-520H320v-200h120l160-160v520Zm80-122v-276q36 21 58 57t22 81q0 45-22 81t-58 57Zm0 172v-84q70-25 115-86.5T840-620q0-78-45-139.5T680-846v-84q104 27 172 112.5T920-620q0 112-68 197.5T680-310Z" />
                                </svg>
                            </button>
                        </div>
                    </div>
                )}
            </div>
        );
    }
}
