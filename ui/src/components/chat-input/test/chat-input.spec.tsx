import { newSpecPage } from '@stencil/core/testing';
import { ChatInput } from '../chat-input';

describe('chat-input', () => {
  it('renders', async () => {
    const page = await newSpecPage({
      components: [ChatInput],
      html: `<chat-input></chat-input>`,
    });
    expect(page.root).toEqualHtml(`
      <chat-input>
        <mock:shadow-root>
          <slot></slot>
        </mock:shadow-root>
      </chat-input>
    `);
  });
});
