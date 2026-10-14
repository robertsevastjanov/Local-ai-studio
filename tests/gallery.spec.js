const { test, expect } = require('@playwright/test');

// Nuxt frontend address.
const FRONTEND_URL = 'http://localhost:3000';

test('gallery displays generation history', async ({ page }) => {
  // Open the Nuxt gallery.
  await page.goto(FRONTEND_URL);

  // Verify that the gallery heading is visible.
  await expect(
    page.getByRole('heading', { name: 'Generation Gallery' })
  ).toBeVisible();

  // Verify that the generation counter is displayed.
  await expect(
    page.getByText(/Images generated: \d+/)
  ).toBeVisible();
});
test('gallery handles missing images', async ({ page }) => {
  // Simulate HTTP 404 for all generated images.
  await page.route('**/images/**', async (route) => {
    await route.fulfill({
      status: 404,
      contentType: 'text/plain',
      body: 'Image not found'
    });
  });

  // Open the Nuxt gallery.
  await page.goto(FRONTEND_URL);

  // Verify that the fallback message is visible.
  await expect(
    page.getByText('Image unavailable').first()
  ).toBeVisible();
});