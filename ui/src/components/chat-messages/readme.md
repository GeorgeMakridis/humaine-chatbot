# chat-messages



<!-- Auto Generated Below -->


## Properties

| Property   | Attribute | Description | Type        | Default     |
| ---------- | --------- | ----------- | ----------- | ----------- |
| `messages` | --        |             | `Message[]` | `undefined` |


## Events

| Event              | Description | Type                      |
| ------------------ | ----------- | ------------------------- |
| `feedbackReceived` |             | `CustomEvent<BotMessage>` |


## Dependencies

### Used by

 - [humaine-chatbot](../humaine-chatbot)

### Depends on

- [user-chat-message](../user-chat-message)
- [bot-chat-message](../bot-chat-message)
- [system-chat-message](../system-chat-message)

### Graph
```mermaid
graph TD;
  chat-messages --> user-chat-message
  chat-messages --> bot-chat-message
  chat-messages --> system-chat-message
  humaine-chatbot --> chat-messages
  style chat-messages fill:#f9f,stroke:#333,stroke-width:4px
```

----------------------------------------------

*Built with [StencilJS](https://stenciljs.com/)*
