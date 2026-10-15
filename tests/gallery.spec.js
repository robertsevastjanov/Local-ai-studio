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

test('gallery loads a real image successfully', async ({ page }) => {
  await page.goto(FRONTEND_URL);

  // Find the newest generated image.
  const image = page.locator('img').first();

  // Check that the image exists.
  await expect(image).toBeVisible();

  // Check that the browser actually loaded its pixels.
  await expect.poll(async () => {
    return image.evaluate((img) =>
      img.complete && img.naturalWidth > 0
    );
  }).toBe(true);
});