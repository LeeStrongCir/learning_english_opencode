#!/usr/bin/env node

/**
 * UI 测试项目初始化脚本
 *
 * 用法: node init-test.js <project-name>
 *
 * 功能:
 *   1. 在 test-artifacts/{project-name}/06-ui-tests/v1/ 创建目录结构
 *   2. 生成 package.json
 *   3. 生成 playwright.config.js
 *   4. 生成示例测试文件
 */

const fs = require('fs');
const path = require('path');

const projectName = process.argv[2];

if (!projectName) {
  console.error('用法: node init-test.js <project-name>');
  console.error('示例: node init-test.js my-web-app');
  process.exit(1);
}

// 项目根目录
const projectRoot = path.resolve(
  __dirname,
  '../../../test-artifacts',
  projectName,
  '06-ui-tests',
  'v1',
);

// 目录结构
const dirs = [
  'tests',
  'fixtures',
  'scenarios',
  'midscene_run/report',
];

function createDir(dir) {
  const fullPath = path.join(projectRoot, dir);
  if (!fs.existsSync(fullPath)) {
    fs.mkdirSync(fullPath, { recursive: true });
    console.log(`  ✅ 创建目录: ${dir}/`);
  } else {
    console.log(`  ⏭️  目录已存在: ${dir}/`);
  }
}

function writeFile(filePath, content) {
  const fullPath = path.join(projectRoot, filePath);
  if (!fs.existsSync(fullPath)) {
    fs.writeFileSync(fullPath, content, 'utf-8');
    console.log(`  ✅ 创建文件: ${filePath}`);
  } else {
    console.log(`  ⏭️  文件已存在: ${filePath}`);
  }
}

console.log(`\n🚀 初始化 UI 测试项目: ${projectName}`);
console.log(`📁 目标路径: ${projectRoot}\n`);

// 创建目录
console.log('📂 创建目录结构...');
dirs.forEach(createDir);

// 生成 package.json
console.log('\n📦 生成 package.json...');
writeFile('package.json', JSON.stringify({
  name: `${projectName}-ui-tests`,
  version: '1.0.0',
  description: `UI 自动化测试 - ${projectName}`,
  type: 'module',
  scripts: {
    test: 'npx playwright test',
    'test:ui': 'npx playwright test --ui',
    'test:report': 'npx playwright show-report',
    'test:headed': 'npx playwright test --headed',
  },
  devDependencies: {
    '@playwright/test': '^1.50.0',
    '@midscene/web': '^1.0.0',
    '@midscene/playwright': '^1.0.0',
  },
}, null, 2));

// 生成 playwright.config.js
console.log('\n⚙️  生成 playwright.config.js...');
writeFile('playwright.config.js', `import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 60000,
  expect: {
    timeout: 10000,
  },
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: [
    ['html', { outputFolder: './midscene_run/html-report' }],
    ['list'],
  ],
  use: {
    baseURL: 'https://example.com',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    viewport: { width: 1280, height: 720 },
  },
});
`);

// 生成示例测试文件
console.log('\n📝 生成示例测试文件...');
writeFile('tests/login.spec.js', `import { test, expect } from '@playwright/test';
import { PlaywrightAgent } from '@midscene/web';

/**
 * 示例：用户登录 UI 测试
 *
 * 运行: npx playwright test tests/login.spec.js
 * 带界面: npx playwright test tests/login.spec.js --headed
 */

test.describe('用户登录', () => {
  test('正常登录流程', async ({ page }) => {
    const agent = new PlaywrightAgent(page);

    // 导航到登录页
    await page.goto('/login');

    // 方式 A：AI 自动规划（适合简单流程）
    await agent.aiAct(
      '在用户名输入框输入 testuser，在密码输入框输入 testpass，点击登录按钮',
    );

    // 等待登录完成
    await agent.aiWaitFor('页面显示登录成功或跳转到首页', {
      timeoutMs: 15000,
    });

    // 断言验证
    await agent.aiAssert('页面显示用户已登录的状态');

    // 提取用户信息
    const userInfo = await agent.aiQuery(
      '{username: string, role: string}',
    );
    console.log('登录用户信息:', userInfo);
  });

  test('登录失败 - 错误密码', async ({ page }) => {
    const agent = new PlaywrightAgent(page);
    await page.goto('/login');

    // 方式 B：手动分步（精确控制）
    await agent.aiInput('用户名输入框', { value: 'testuser' });
    await agent.aiInput('密码输入框', { value: 'wrongpassword' });
    await agent.aiTap('登录按钮');

    // 等待错误提示
    await agent.aiWaitFor('页面显示错误提示', { timeoutMs: 10000 });

    // 验证错误提示
    await agent.aiAssert('页面显示密码错误或登录失败的提示');
  });

  test('登录失败 - 空字段', async ({ page }) => {
    const agent = new PlaywrightAgent(page);
    await page.goto('/login');

    // 直接点击登录（不填写任何内容）
    await agent.aiTap('登录按钮');

    // 验证表单验证提示
    await agent.aiAssert('页面显示必填字段不能为空的提示');
  });
});
`);

// 生成场景定义示例
console.log('\n📋 生成场景定义示例...');
writeFile('scenarios/smoke-test.yaml', `# 冒烟测试场景定义
# 可通过 agent.runYaml() 执行

name: 冒烟测试
url: /
tasks:
  - name: 首页加载
    flow:
      - ai: 访问首页
      - sleep: 2000
      - aiAssert: 页面正常加载，显示主要内容

  - name: 搜索功能
    flow:
      - ai: 在搜索框输入测试关键词，点击搜索
      - sleep: 3000
      - aiAssert: 页面显示搜索结果

  - name: 提取数据
    flow:
      - aiQuery: "页面标题和描述文字，{title: string, description: string}"
`);

// 生成 .env.example
console.log('\n🔑 生成 .env.example...');
writeFile('.env.example', `# AI 模型配置（通过环境变量）
MIDSCENE_MODEL_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MIDSCENE_MODEL_API_KEY=sk-your-api-key-here
MIDSCENE_MODEL_NAME=qwen3-vl-plus
MIDSCENE_MODEL_FAMILY=qwen3-vl
`);

// 生成 README
console.log('\n📖 生成 README.md...');
writeFile('README.md', `# ${projectName} - UI 自动化测试

## 快速开始

### 1. 安装依赖

\`\`\`bash
npm install
npx playwright install chromium
\`\`\`

### 2. 配置模型

复制 .env.example 为 .env 并填入 API Key：

\`\`\`bash
cp .env.example .env
\`\`\`

### 3. 运行测试

\`\`\`bash
# 运行所有测试
npm test

# 带浏览器界面运行
npm run test:headed

# 运行特定测试
npx playwright test tests/login.spec.js

# 查看 HTML 报告
npm run test:report
\`\`\`

## 目录结构

\`\`\`
├── tests/          # 测试脚本
├── fixtures/       # 测试数据
├── scenarios/      # YAML 场景定义
├── midscene_run/   # 执行产物（自动生成）
│   └── report/     # Midscene HTML 报告
└── playwright.config.js
\`\`\`

## 编写测试

参考 Skill 文档：\`.opencode/skills/ui-test-midscene/SKILL.md\`
`);

// 创建 latest 软链接
const latestPath = path.resolve(
  __dirname,
  '../../../test-artifacts',
  projectName,
  '06-ui-tests',
  'latest',
);

if (!fs.existsSync(latestPath)) {
  try {
    fs.symlinkSync('v1', latestPath, 'dir');
    console.log('\n🔗 创建 latest 软链接 → v1/');
  } catch (e) {
    console.log('\n⚠️  创建 latest 软链接失败（可能已存在）');
  }
}

console.log(`\n✅ 项目初始化完成！`);
console.log(`\n📋 下一步:`);
console.log(`  1. cd ${projectRoot}`);
console.log(`  2. npm install`);
console.log(`  3. npx playwright install chromium`);
console.log(`  4. cp .env.example .env  # 填入 API Key`);
console.log(`  5. npm test`);
console.log('');
