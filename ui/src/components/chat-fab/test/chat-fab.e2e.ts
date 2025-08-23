import { newE2EPage } from '@stencil/core/testing';

describe('chat-fab', () => {
  it('renders', async () => {
    const page = await newE2EPage();
    await page.setContent('<chat-fab></chat-fab>');

    const element = await page.find('chat-fab');
    expect(element).toHaveClass('hydrated');
  });
});
