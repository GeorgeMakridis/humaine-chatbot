import { newSpecPage } from '@stencil/core/testing';
import { SystemChatMessage } from '../system-chat-message';

describe('system-chat-message', () => {
  it('renders', async () => {
    const page = await newSpecPage({
      components: [SystemChatMessage],
      html: `<system-chat-message></system-chat-message>`,
    });
    expect(page.root).toEqualHtml(`
      <system-chat-message>
        <mock:shadow-root>
          <slot></slot>
        </mock:shadow-root>
      </system-chat-message>
    `);
  });
});
