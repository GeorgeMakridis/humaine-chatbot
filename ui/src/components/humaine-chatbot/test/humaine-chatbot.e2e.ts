import { newE2EPage } from '@stencil/core/testing';

describe('humaine-chatbot', () => {
  it('renders', async () => {
    const page = await newE2EPage();
    await page.setContent('<humaine-chatbot></humaine-chatbot>');

    const element = await page.find('humaine-chatbot');
    expect(element).toHaveClass('hydrated');
  });
});
