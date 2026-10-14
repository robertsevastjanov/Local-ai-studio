const { test, expect } = require('@playwright/test');

test('GET /health returns status 200 and valid JSON', async ({ request }) => {

    const response = await request.get('http://127.0.0.1:8000/health');

    expect(response.status()).toBe(200);

    const body = await response.json();

    expect(body.status).toBe('ok');
});

test('POST /generate returns successful generation response', async ({ request }) => {

    const response = await request.post('http://127.0.0.1:8000/generate', {
        data: {
            prompt: 'A giant hornet flying over Riga',
            steps: 8,
            seed: 42
        }
    });

    expect(response.status()).toBe(200);

    const body = await response.json();

    expect(body.status).toBe('completed');
    expect(body.prompt).toBe('A giant hornet flying over Riga');
    expect(body.steps).toBe(8);
    expect(body.seed).toBe(42);

    expect(body.image_path).toMatch(
        /^images\/generated_42_[a-f0-9]{32}\.png$/
    );
});
test('POST /generate rejects steps above maximum with HTTP 422', async ({ request }) => {

    const response = await request.post('http://127.0.0.1:8000/generate', {
        data: {
            prompt: 'A giant hornet flying over Riga',
            steps: 31,
            seed: 42
        }
    });

    expect(response.status()).toBe(422);

    const body = await response.json();

    expect(body.detail[0].loc).toContain('steps');

    expect(body.detail[0].type).toBe('less_than_equal');
});

test('generation requests with the same seed use unique image paths', async ({ request }) => {

    const firstResponse = await request.post('http://127.0.0.1:8000/generate', {
        data: {
            prompt: 'A fluffy orange cat sitting on a sofa',
            steps: 8,
            seed: 42
        }
    });

    const secondResponse = await request.post('http://127.0.0.1:8000/generate', {
        data: {
            prompt: 'A giant hornet flying over a forest',
            steps: 8,
            seed: 42
        }
    });

    expect(firstResponse.status()).toBe(200);
    expect(secondResponse.status()).toBe(200);

    const firstBody = await firstResponse.json();
    const secondBody = await secondResponse.json();

    expect(firstBody.image_path).not.toBe(secondBody.image_path);

    console.log('First image:', firstBody.image_path);
    console.log('Second image:', secondBody.image_path);
});

test('GET /history returns saved generations as JSON', async ({ request }) => {

    const response = await request.get('http://127.0.0.1:8000/history');

    expect(response.status()).toBe(200);

    const body = await response.json();

    expect(body.status).toBe('ok');

    expect(Array.isArray(body.generations)).toBe(true);

    expect(body.count).toBe(body.generations.length);

    for (const generation of body.generations) {
        expect(typeof generation.id).toBe('number');
        expect(typeof generation.prompt).toBe('string');
        expect(typeof generation.steps).toBe('number');
        expect(typeof generation.seed).toBe('number');
        expect(typeof generation.image_path).toBe('string');
        expect(typeof generation.created_at).toBe('string');
    }
});

test('PHP statistics API returns valid generation statistics', async ({ request }) => {
  const response = await request.get('http://127.0.0.1:8001/stats.php');

  expect(response.status()).toBe(200);

  expect(response.headers()['content-type']).toContain('application/json');

  const body = await response.json();

  expect(body.status).toBe('ok');

  expect(Number.isInteger(body.stats.total_generations)).toBe(true);
  expect(body.stats.total_generations).toBeGreaterThanOrEqual(0);

  expect(Number.isInteger(body.stats.unique_seeds)).toBe(true);
  expect(body.stats.unique_seeds).toBeGreaterThanOrEqual(0);

  expect(Number.isInteger(body.stats.generations_today)).toBe(true);
  expect(body.stats.generations_today).toBeGreaterThanOrEqual(0);

  expect(body.stats.unique_seeds).toBeLessThanOrEqual(body.stats.total_generations);

  expect(body.stats.generations_today).toBeLessThanOrEqual(body.stats.total_generations);
});