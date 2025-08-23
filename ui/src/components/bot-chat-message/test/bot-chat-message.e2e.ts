import { newE2EPage } from '@stencil/core/testing';

describe('bot-chat-message', () => {
  it('renders', async () => {
    const page = await newE2EPage();
    await page.setContent('<bot-chat-message></bot-chat-message>');

    const element = await page.find('bot-chat-message');
    expect(element).toHaveClass('hydrated');
  });
});
