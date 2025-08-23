import { newE2EPage } from '@stencil/core/testing';

describe('chat-messages', () => {
  it('renders', async () => {
    const page = await newE2EPage();
    await page.setContent('<chat-messages></chat-messages>');

    const element = await page.find('chat-messages');
    expect(element).toHaveClass('hydrated');
  });
});
