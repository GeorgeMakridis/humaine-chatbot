import { newSpecPage } from '@stencil/core/testing';
import { ChatMessages } from '../chat-messages';

describe('chat-messages', () => {
  it('renders', async () => {
    const page = await newSpecPage({
      components: [ChatMessages],
      html: `<chat-messages></chat-messages>`,
    });
    expect(page.root).toEqualHtml(`
      <chat-messages>
        <mock:shadow-root>
          <slot></slot>
        </mock:shadow-root>
      </chat-messages>
    `);
  });
});
