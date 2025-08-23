import { newE2EPage } from '@stencil/core/testing';

describe('system-chat-message', () => {
  it('renders', async () => {
    const page = await newE2EPage();
    await page.setContent('<system-chat-message></system-chat-message>');

    const element = await page.find('system-chat-message');
    expect(element).toHaveClass('hydrated');
  });
});
