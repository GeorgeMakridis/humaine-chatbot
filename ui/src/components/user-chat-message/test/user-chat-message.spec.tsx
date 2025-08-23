import { newSpecPage } from '@stencil/core/testing';
import { UserChatMessage } from '../user-chat-message';

describe('user-chat-message', () => {
  it('renders', async () => {
    const page = await newSpecPage({
      components: [UserChatMessage],
      html: `<user-chat-message></user-chat-message>`,
    });
    expect(page.root).toEqualHtml(`
      <user-chat-message>
        <mock:shadow-root>
          <slot></slot>
        </mock:shadow-root>
      </user-chat-message>
    `);
  });
});
