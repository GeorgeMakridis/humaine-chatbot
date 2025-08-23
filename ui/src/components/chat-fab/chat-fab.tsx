import { Component, Event, EventEmitter, getAssetPath, h } from '@stencil/core';

@Component({
    tag: 'chat-fab',
    styleUrl: 'chat-fab.css',
    shadow: true
})
export class ChatFab {
    @Event() chatFabPressed: EventEmitter;
    render() {
        return (
            <div id="chat-fab" onClick={() => this.chatFabPressed.emit()}>
                <img class="icon" src={getAssetPath('./assets/icon_chat.svg')}></img>
            </div >
        );
    }
}
