const { test, expect } = require('@playwright/test');

test('user can see signin page', async ({ page }) => {
  await page.goto('/signin.html');

  // Username field
  await expect(page.getByPlaceholder('Enter username')).toBeVisible();

  // Password field
  await expect(page.getByPlaceholder('Enter password')).toBeVisible();

  // Login button
  await expect(page.locator('#login-btn')).toBeVisible();
});

test('user can login and navigate to store page', async ({ page }) => {
  await page.goto('/signin.html');

  await page.getByPlaceholder('Enter username').fill('srinivas');
  await page.getByPlaceholder('Enter password').fill('password123');
  await page.locator('#login-btn').click();

  await expect(page).toHaveURL(/store\.html/);
});
