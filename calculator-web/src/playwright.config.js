const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',

  // This reporter prints each test clearly in GitHub Actions logs
  reporter: [
    ['line']
  ],

  use: {
    baseURL: 'http://localhost:3000',
    headless: true,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure'
  }
});
