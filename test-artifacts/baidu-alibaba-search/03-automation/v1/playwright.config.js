// @ts-check
import { defineConfig, devices } from '@playwright/test';
import dotenv from 'dotenv';

// 加载环境变量
dotenv.config();

/**
 * @see https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: './tests',

  /* 完全并行执行测试 */
  fullyParallel: true,

  /* 禁止单个测试文件中出现 .only，防止 CI 中遗漏 */
  forbidOnly: !!process.env.CI,

  /* 失败时重试次数 */
  retries: process.env.CI ? 2 : 1,

  /* 并行 worker 数量 */
  workers: process.env.CI ? 1 : undefined,

  /* 测试报告配置 */
  reporter: [
    ['html', { outputFolder: './playwright-report', open: 'never' }],
    ['json', { outputFile: './test-results/results.json' }],
    ['list'],
  ],

  /* Midscene.js 报告输出目录 */
  outputDir: './midscene_run',

  /* 全局超时（毫秒） */
  timeout: 120000,

  /* 每个测试用例的超时 */
  expect: {
    timeout: 15000,
  },

  /* 共享设置用于所有测试 */
  use: {
    /* 基础 URL（可选） */
    baseURL: 'https://www.baidu.com',

    /* 每次测试后保留浏览器上下文 */
    trace: 'retain-on-failure',

    /* 失败时截图 */
    screenshot: 'only-on-failure',

    /* 失败时录制视频 */
    video: 'retain-on-failure',

    /* 浏览器上下文选项 */
    viewport: { width: 1920, height: 1080 },

    /* 忽略 HTTPS 证书错误 */
    ignoreHTTPSErrors: true,

    /* 操作超时 */
    actionTimeout: 30000,
    navigationTimeout: 30000,
  },

  /* 针对不同浏览器的配置 */
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    // 如需 Firefox 测试，取消注释
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] },
    // },
    // 如需 WebKit 测试，取消注释
    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'] },
    // },
  ],

  /* 本地开发服务器配置（本项目不需要） */
  // webServer: {
  //   command: 'npm run start',
  //   url: 'http://127.0.0.1:3000',
  //   reuseExistingServer: !process.env.CI,
  // },
});
