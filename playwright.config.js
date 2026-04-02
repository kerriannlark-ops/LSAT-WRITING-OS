const { defineConfig, devices } = require('@playwright/test');

const port = process.env.PLAYWRIGHT_PORT || 4173;
const baseURL = process.env.PLAYWRIGHT_BASE_URL || `http://127.0.0.1:${port}`;
const useExternalBaseUrl = Boolean(process.env.PLAYWRIGHT_BASE_URL);

module.exports = defineConfig({
  testDir: './tests',
  fullyParallel: false,
  timeout: 90_000,
  expect: {
    timeout: 10_000
  },
  retries: process.env.CI ? 2 : 1,
  reporter: [
    ['list'],
    ['html', { open: 'never', outputFolder: 'playwright-report' }]
  ],
  use: {
    baseURL,
    viewport: { width: 1440, height: 1024 },
    actionTimeout: 15_000,
    navigationTimeout: 20_000,
    screenshot: 'only-on-failure',
    trace: 'on-first-retry',
    video: 'off',
    serviceWorkers: 'block'
  },
  webServer: useExternalBaseUrl ? undefined : {
    command: `python3 -m http.server ${port} --directory .`,
    cwd: __dirname,
    url: baseURL,
    reuseExistingServer: true,
    timeout: 30_000
  },
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome']
      }
    },
    {
      name: 'webkit',
      use: {
        ...devices['Desktop Safari']
      }
    }
  ]
});
