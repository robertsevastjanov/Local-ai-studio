const { test, expect } = require('@playwright/test');
const { execFileSync } = require('node:child_process');
test('full generation flow', async ({ request, page }) => {
  // Create a unique prompt for this test run.
  const prompt = `E2E test image ${Date.now()}`;

  // Send a generation request to FastAPI.
  const response = await request.post('http://127.0.0.1:8000/generate', {
    data: {
      prompt: prompt,
      steps: 8,
      seed: 42
    }
  });

  // Verify that the API successfully generated an image.
  expect(response.status()).toBe(200);

  const generation = await response.json();

  expect(generation.status).toBe('completed');
  expect(generation.prompt).toBe(prompt);
  expect(generation.image_path).toMatch(/^images\/generated_42_[a-f0-9]{32}\.png$/);
    // Retrieve generation history from PostgreSQL.
  const historyResponse = await request.get('http://127.0.0.1:8000/history');

  expect(historyResponse.status()).toBe(200);

  const history = await historyResponse.json();

  // Find the exact generation created by this test.
  const savedGeneration = history.generations.find(
    item => item.image_path === generation.image_path
  );

  // Verify that the generated image was saved.
  expect(savedGeneration).toBeDefined();
  expect(savedGeneration.prompt).toBe(prompt);
  expect(savedGeneration.steps).toBe(8);
  expect(savedGeneration.seed).toBe(42);
  // Check that the same generation exists in SQLite.
  const sqliteResult = execFileSync(
    'python',
    ['tests/check_sqlite.py',
      generation.image_path,
      prompt,
      String(generation.steps),
      String(generation.seed)
    ],
    { encoding: 'utf8' }
  );

  expect(sqliteResult).toContain('Generation found:');
    // Open the Nuxt frontend in a real browser.
  await page.goto('http://localhost:3000');

  // Verify that the gallery heading is visible.
  await expect(
    page.getByRole('heading', { name: 'Generation Gallery' })
  ).toBeVisible();
    // Verify that this test's generation appears in the gallery.
  await expect(
    page.getByText(prompt, { exact: true })
  ).toBeVisible();
    // Verify that the generated PNG can be downloaded.
  const imageResponse = await request.get(
    `http://127.0.0.1:8000/${generation.image_path}`
  );

  expect(imageResponse.status()).toBe(200);
  expect(imageResponse.headers()['content-type']).toContain('image/png');
    // Find the image created by this test.
  const galleryImage = page.getByRole('img', { name: prompt });

  // Verify that the browser displays the image.
  await expect(galleryImage).toBeVisible();

  // Verify that the image was successfully loaded.
  await expect(galleryImage).toHaveJSProperty('complete', true);

  const imageWidth = await galleryImage.evaluate(
    image => image.naturalWidth
  );

  expect(imageWidth).toBeGreaterThan(0);
});