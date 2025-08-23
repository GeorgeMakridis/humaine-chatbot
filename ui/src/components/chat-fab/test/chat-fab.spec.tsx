import { newSpecPage } from '@stencil/core/testing';
import { ChatFab } from '../chat-fab';

describe('chat-fab', () => {
  it('renders', async () => {
    const page = await newSpecPage({
      components: [ChatFab],
      html: `<chat-fab></chat-fab>`,
    });
    expect(page.root).toEqualHtml(`
      <chat-fab>
        <mock:shadow-root>
          <slot></slot>
        </mock:shadow-root>
      </chat-fab>
    `);
  });
});
