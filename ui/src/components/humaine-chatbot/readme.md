# humaine-chatbot



<!-- Auto Generated Below -->


## Properties

| Property     | Attribute     | Description | Type     | Default     |
| ------------ | ------------- | ----------- | -------- | ----------- |
| `apiKey`     | `api-key`     |             | `string` | `undefined` |
| `assetsPath` | `assets-path` |             | `string` | `undefined` |
| `baseUrl`    | `base-url`    |             | `string` | `undefined` |
| `langCode`   | `lang-code`   |             | `string` | `undefined` |


## Dependencies

### Depends on

- [chat-fab](../chat-fab)
- [chat-messages](../chat-messages)
- [chat-input](../chat-input)

### Graph
```mermaid
graph TD;
  humaine-chatbot --> chat-fab
  humaine-chatbot --> chat-messages
  humaine-chatbot --> chat-input
  chat-messages --> user-chat-message
  chat-messages --> bot-chat-message
  chat-messages --> system-chat-message
  style humaine-chatbot fill:#f9f,stroke:#333,stroke-width:4px
```

----------------------------------------------

*Built with [StencilJS](https://stenciljs.com/)*
