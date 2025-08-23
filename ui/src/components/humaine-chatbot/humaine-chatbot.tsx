import { Component, Listen, Prop, State, getAssetPath, h, Element } from '@stencil/core';
import { Message } from '../../models/message';
import { DialogueManager } from '../../services/dialogueManager';
import { BotMessage, UserInputAction } from '../../components';
import { UserMessage } from '../../models/userMessage';
import { ChatServiceConfig } from '../../models/chatServiceConfig';
import { ActivityMonitor } from '../../services/activityMonitor';
import { SessionEndType } from '../../types/sessionType';
import { Feedback } from '../../models/feedback';

@Component({
    tag: 'humaine-chatbot',
    styleUrl: 'humaine-chatbot.css',
    shadow: true,
    assetsDirs: ['assets']
})
export class HumaineChatbot {
    static EVENT_MESSAGE_ADDED = "messageAdded";
    static EVENT_MESSAGE_UPDATED = "messageUpdated";

    @Prop() baseUrl: string;
    @Prop() apiKey: string;
    @Prop() langCode: string;
    @Prop() assetsPath: string;

    @State() isVisible: boolean = false;
    @State() isActive: boolean = false;
    @State() messageHistory: Message[] = [];

    @Element() el: HTMLElement;

    private chatbotWindow: HTMLElement;

    private dialogueManager: DialogueManager;
    private activityMonitor: ActivityMonitor;

    componentWillLoad() {
        const config = new ChatServiceConfig(this.baseUrl, this.apiKey);

        this.dialogueManager = new DialogueManager(config, this.langCode, this.assetsPath);
        this.dialogueManager.addEventListener(HumaineChatbot.EVENT_MESSAGE_ADDED, this.handleNewMessage);
        this.dialogueManager.addEventListener(HumaineChatbot.EVENT_MESSAGE_UPDATED, this.handleUpdatedMessage);

        this.activityMonitor = new ActivityMonitor();
        this.activityMonitor.addEventListener(ActivityMonitor.EVENT_INACTIVITY_TIMEOUT, this.handleInactivityTimeout);
    }

    componentDidRender() {
        // Check if the chatbot window is visible and if the .chat-box element is rendered
        if (this.isVisible) {
            this.chatbotWindow = this.el.shadowRoot.querySelector('.chat-box');

            if (this.chatbotWindow) {
                this.chatbotWindow.addEventListener('mouseenter', this.handleMouseEnter.bind(this));
                this.chatbotWindow.addEventListener('mouseleave', this.handleMouseLeave.bind(this));
            }
        }
    }

    disconnectedCallback() {
        this.dialogueManager.removeEventListener(HumaineChatbot.EVENT_MESSAGE_ADDED, this.handleNewMessage);
        this.dialogueManager.removeEventListener(HumaineChatbot.EVENT_MESSAGE_UPDATED, this.handleUpdatedMessage);
    }

    @Listen('inputActionSubmitted')
    async inputActionSubmittedHandler(event: CustomEvent<UserInputAction>) {
        this.dialogueManager.sendUserMessage(new UserMessage(event.detail));
    }

    @Listen('chatFabPressed')
    chatFabPressed() {
        this.toggleWindow(!this.isVisible);
    }

    private toggleWindow(isVisible: boolean) {
        this.isVisible = isVisible;
        if (this.isVisible) {
            this.startSession();
        } else {
            this.endSession('userAction');

            if (this.chatbotWindow) {
                this.chatbotWindow.removeEventListener('mouseenter', this.handleMouseEnter.bind(this));
                this.chatbotWindow.removeEventListener('mouseleave', this.handleMouseLeave.bind(this));
            }
        }
    }
    private startSession() {
        this.isActive = true;
        this.dialogueManager.startSession();
    }
    private endSession(endType: SessionEndType) {
        this.isActive = false;
        this.messageHistory = [];
        this.dialogueManager.endSession(endType);
    }

    private handleNewMessage = (event: CustomEvent) => {
        // Append the new message to the existing message history, creating a new array to maintain immutability.
        const message = event.detail.message;
        this.messageHistory = [...this.messageHistory, message];
    }
    private handleUpdatedMessage = (event: CustomEvent) => {
        const updatedMessage = event.detail.message;
        const index = this.messageHistory.findIndex(message => message.id === updatedMessage.id);

        // Replace the message at the found index with a deep copy of the updated message to ensure reactivity.
        // Reassign messageHistory to a new array, preserving immutability for potential reactivity.
        this.messageHistory[index] = updatedMessage.deepCopy();
        this.messageHistory = [...this.messageHistory];
    }
    private handleFeedback(event: CustomEvent) {
        const botMessage = event.detail as BotMessage;
        this.dialogueManager.sendMessageFeedback(new Feedback(botMessage));
    }

    private handleInactivityTimeout = () => {
        this.endSession('inactivity');
    }

    private handleMouseEnter() {
        this.activityMonitor.stopInactivityTracking();

        this.chatbotWindow.classList.add('focused');
        this.chatbotWindow.classList.remove('unfocused');

        if (!this.isActive) {
            this.startSession();
        }
    }
    private handleMouseLeave() {
        this.activityMonitor.startInactivityTracking();

        this.chatbotWindow.classList.remove('focused');
        this.chatbotWindow.classList.add('unfocused');
    }

    render() {
        return (
            <host>
                <div>
                    {!this.isVisible ? (
                        <chat-fab></chat-fab>
                    ) : (
                        <div class="chat-box" tabindex="0">
                            <div class="chat-box-header">
                                <img class="logo" src={getAssetPath('./assets/logo.png')}></img>
                                <p>Human-Centric Chatbot</p>
                                <span class="chat-box-toggle" onClick={() => this.chatFabPressed()}>
                                    <img class="icon" src={getAssetPath('./assets/icon_close.svg')}></img>
                                </span>
                            </div>
                            <span class="status-message">
                                {this.isActive ? 'Session Started' : 'Session Ended'}
                            </span>
                            <div class="section-messages">
                                <chat-messages
                                    messages={this.messageHistory}
                                    onFeedbackReceived={(event) => this.handleFeedback(event)}
                                ></chat-messages>
                            </div>
                            <div class="section-input">
                                <chat-input></chat-input>
                            </div>
                        </div>
                    )}
                </div>
            </host>
        );
    }
}
