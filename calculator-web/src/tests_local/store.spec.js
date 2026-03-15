const { test, expect } = require('@playwright/test');

test('store page loads', async ({ page }) => {
  await page.goto('/store.html');

  // Example: check a heading or button
  const heading = page.locator('h1');
  await expect(heading).toContainText(/Store/i);
});
