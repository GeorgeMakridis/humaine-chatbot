import { newE2EPage } from '@stencil/core/testing';

describe('chat-input', () => {
  it('renders', async () => {
    const page = await newE2EPage();
    await page.setContent('<chat-input></chat-input>');

    const element = await page.find('chat-input');
    expect(element).toHaveClass('hydrated');
  });
});
