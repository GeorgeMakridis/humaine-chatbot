import { newSpecPage } from '@stencil/core/testing';
import { BotChatMessage } from '../bot-chat-message';

describe('bot-chat-message', () => {
  it('renders', async () => {
    const page = await newSpecPage({
      components: [BotChatMessage],
      html: `<bot-chat-message></bot-chat-message>`,
    });
    expect(page.root).toEqualHtml(`
      <bot-chat-message>
        <mock:shadow-root>
          <slot></slot>
        </mock:shadow-root>
      </bot-chat-message>
    `);
  });
});
