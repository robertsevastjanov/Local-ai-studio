const { test, expect } = require('@playwright/test');

const URL = process.env.CI
  ? 'http://127.0.0.1:3000/'
  : 'http://[::1]:3000/';

test('homepage displays correct title', async ({ page }) => {
    await page.goto(URL);

    await expect(
        page.getByRole('heading', {
        name: 'Create without limits.'})
    ).toBeVisible();
});

test('disables generation for short prompt', async ({ page }) => {

    await page.goto(URL);

    await page.locator('#prompt').fill('cat');

    await expect(
        page.getByRole('button', { name: /Generate Image/ })
    ).toBeDisabled();
});

test('rejects steps below minimum', async ({ page }) => {

    await page.goto(URL);

    await page.locator('#prompt').fill('A giant hornet flying over Riga');

    await page.locator('#steps').fill('0');

    expect(
        await page.locator('#steps').evaluate(el => el.validity.rangeUnderflow)
    ).toBe(true);
});

test('rejects steps above maximum', async ({ page }) => {

    await page.goto(URL);

    await page.locator('#prompt').fill('A giant hornet flying over Riga');

    await page.locator('#steps').fill('31');

    expect(
    await page.locator('#steps').evaluate(el => el.validity.rangeOverflow)
  ).toBe(true);
});

test('accepts minimum steps value', async ({ page }) => {

    await page.goto(URL);

    await page.locator('#prompt').fill('A giant hornet flying over Riga');
    await page.locator('#steps').fill('1');

    expect(
    await page.locator('#steps').evaluate(el => el.validity.valid)
  ).toBe(true);
});

test('accepts maximum steps value', async ({ page }) => {

    await page.goto(URL);

    await page.locator('#prompt').fill('A giant hornet flying over Riga');

    await page.locator('#steps').fill('30');

      expect(
    await page.locator('#steps').evaluate(el => el.validity.valid)
  ).toBe(true);
});