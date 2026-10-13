const { test, expect } = require('@playwright/test');

test('homepage displays correct title', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/');

    await expect(page.getByRole('heading', {
        name: 'Local AI Studio'
    })).toBeVisible();
});