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
});

test('rejects steps below minimum', async ({ page }) => {

    await page.goto('http://127.0.0.1:8000/');

    await page.locator('#prompt').fill('A giant hornet flying over Riga');

    await page.locator('#steps').fill('0');

    await page.getByRole('button', { name: 'Generate' }).click();

    await expect(page.locator('#errorMessage'))
        .toContainText('Input should be greater than or equal to 1');
});

test('rejects steps above maximum', async ({ page }) => {

    await page.goto('http://127.0.0.1:8000/');

    await page.locator('#prompt').fill('A giant hornet flying over Riga');

    await page.locator('#steps').fill('31');

    await page.getByRole('button', { name: 'Generate' }).click();

    await expect(page.locator('#errorMessage'))
        .toContainText('Input should be less than or equal to 30');
});

test('accepts minimum steps value', async ({ page }) => {

    await page.goto('http://127.0.0.1:8000/');

    await page.locator('#prompt').fill('A giant hornet flying over Riga');
    await page.locator('#steps').fill('1');

    await page.getByRole('button', { name: 'Generate' }).click();

    await expect(page.locator('#resultImage')).toBeVisible();

    await expect(page.locator('#errorMessage')).toBeEmpty();
});

test('accepts maximum steps value', async ({ page }) => {

    await page.goto('http://127.0.0.1:8000/');

    await page.locator('#prompt').fill('A giant hornet flying over Riga');

    await page.locator('#steps').fill('30');

    await page.getByRole('button', { name: 'Generate' }).click();

    await expect(page.locator('#resultImage')).toBeVisible();

    await expect(page.locator('#errorMessage')).toBeEmpty();
});