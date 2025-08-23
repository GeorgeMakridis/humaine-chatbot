import { Component, Event, EventEmitter, State, getAssetPath, h } from '@stencil/core';
import { UserInputAction } from '../../models/userInputAction';

@Component({
    tag: 'chat-input',
    styleUrl: 'chat-input.css',
    shadow: true
})
export class ChatInput {
    @Event() inputActionSubmitted: EventEmitter<UserInputAction>;
    @Event() focusChanged: EventEmitter<boolean>;
    @State() userInput: string = '';

    private userInputAction?: UserInputAction;

    handleInputChange(event: Event) {
        const input = event.target as HTMLInputElement;

        // If the input value is empty clear the userInputAction.
        // Else create a new UserInputAction if it doesn't exist and
        // update the userInputAction with the current input value.
        if (input.value.trim() === '') {
            this.userInputAction = undefined;
        } else {

            if (!this.userInputAction) {
                this.userInputAction = new UserInputAction();
            }

            this.userInputAction.update(input.value);
            this.userInput = input.value;
        }
    }
    handleSend() {
        // If no text, do not sumit.
        // Else emit the event with the input action and clear.
        if (!this.userInputAction) return;

        this.inputActionSubmitted.emit(this.userInputAction);
        this.clearInput();
    }
    handleKeyDown(event: KeyboardEvent) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent default action (like form submission)
            this.handleSend(); // Call send function
        }
    }
    handleInputFocus() {
        this.focusChanged.emit(true);
    }
    handleInputBlur() {
        this.focusChanged.emit(false);
    }

    clearInput() {
        this.userInputAction = undefined;
        this.userInput = '';
    }

    render() {
        return (
            <div class="chat-input">
                <input
                    type="text"
                    value={this.userInput}
                    onInput={(event) => this.handleInputChange(event)}
                    onKeyDown={(event) => this.handleKeyDown(event)}
                    onFocus={() => this.handleInputFocus()}
                    onBlur={() => this.handleInputBlur()}
                    autoFocus
                    placeholder="Type your message..."
                />
                <button class="chat-submit" onClick={() => this.handleSend()}>
                    <img class="icon" src={getAssetPath('./assets/icon_send.svg')}></img>
                </button>
            </div>
        );
    }
}
