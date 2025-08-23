import { newE2EPage } from '@stencil/core/testing';

describe('user-chat-message', () => {
  it('renders', async () => {
    const page = await newE2EPage();
    await page.setContent('<user-chat-message></user-chat-message>');

    const element = await page.find('user-chat-message');
    expect(element).toHaveClass('hydrated');
  });
});
