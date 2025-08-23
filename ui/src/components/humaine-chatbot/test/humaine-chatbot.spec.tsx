import { newSpecPage } from '@stencil/core/testing';
import { HumaineChatbot } from '../humaine-chatbot';

describe('humaine-chatbot', () => {
  it('renders', async () => {
    const page = await newSpecPage({
      components: [HumaineChatbot],
      html: `<humaine-chatbot></humaine-chatbot>`,
    });
    expect(page.root).toEqualHtml(`
      <humaine-chatbot>
        <mock:shadow-root>
          <slot></slot>
        </mock:shadow-root>
      </humaine-chatbot>
    `);
  });
});
