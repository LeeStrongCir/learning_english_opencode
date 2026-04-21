import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 120000,
  use: {
    headless: true,
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'retain-on-failure',
  },
  reporter: [
    ['list'],
    ['json', { outputFile: '../04-execution/run-001/playwright-report.json' }],
    ['html', { outputFolder: '../04-execution/run-001/html-report', open: 'never' }],
  ],
});
