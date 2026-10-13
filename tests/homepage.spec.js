const { test, expect } = require('@playwright/test');

test('homepage displays correct title', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/');

    await expect(page.getByRole('heading', {
        name: 'Local AI Studio'
    })).toBeVisible();
});

test('shows validation error for short prompt', async ({ page }) => {

    await page.goto('http://127.0.0.1:8000/');

    await page.locator('#prompt').fill('cat');

    await page.getByRole('button', {
        name: 'Generate'
    }).click();

    await expect(page.locator('#errorMessage'))
        .toContainText('String should have at least 10 characters');
        
    await page.waitForTimeout(5000);
});