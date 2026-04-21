#!/usr/bin/env node

/**
 * UI 测试执行脚本
 *
 * 用法:
 *   node run-test.js <project-name> [test-file] [options]
 *
 * 示例:
 *   node run-test.js my-web-app                    # 运行所有测试
 *   node run-test.js my-web-app login.spec.js      # 运行指定测试
 *   node run-test.js my-web-app --headed           # 带界面运行
 *   node run-test.js my-web-app --report           # 仅查看报告
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const projectName = args[0];

if (!projectName) {
  console.error('用法: node run-test.js <project-name> [test-file] [options]');
  console.error('示例:');
  console.error('  node run-test.js my-web-app                    # 运行所有测试');
  console.error('  node run-test.js my-web-app login.spec.js      # 运行指定测试');
  console.error('  node run-test.js my-web-app --headed           # 带界面运行');
  console.error('  node run-test.js my-web-app --report           # 仅查看报告');
  process.exit(1);
}

// 定位测试目录
const testDir = path.resolve(
  __dirname,
  '../../../test-artifacts',
  projectName,
  '06-ui-tests',
  'v1',
);

if (!fs.existsSync(testDir)) {
  console.error(`❌ 测试目录不存在: ${testDir}`);
  console.error('请先运行初始化: node init-test.js <project-name>');
  process.exit(1);
}

// 解析参数
const testFile = args[1] && !args[1].startsWith('--') ? args[1] : null;
const options = args.filter(a => a.startsWith('--'));

const isHeaded = options.includes('--headed');
const isReport = options.includes('--report');
const isUI = options.includes('--ui');
const isDebug = options.includes('--debug');

// 仅查看报告
if (isReport) {
  const reportPath = path.join(testDir, 'midscene_run', 'html-report');
  const midsceneReport = path.join(testDir, 'midscene_run', 'report');

  if (fs.existsSync(reportPath)) {
    console.log(`📊 打开 Playwright 报告: ${reportPath}`);
    execSync(`npx playwright show-report --reporter html`, {
      cwd: testDir,
      stdio: 'inherit',
    });
  } else if (fs.existsSync(midsceneReport)) {
    console.log(`📊 打开 Midscene 报告: ${midsceneReport}`);
    console.log('请在浏览器中打开 index.html 文件查看');
  } else {
    console.error('❌ 未找到测试报告，请先运行测试');
  }
  process.exit(0);
}

// 构建命令
let command = 'npx playwright test';

if (testFile) {
  command += ` ${testFile}`;
}

if (isHeaded) command += ' --headed';
if (isUI) command += ' --ui';
if (isDebug) command += ' --debug';

// 检查依赖
console.log('🔍 检查环境...');

try {
  const pkgPath = path.join(testDir, 'package.json');
  if (!fs.existsSync(pkgPath)) {
    throw new Error('package.json 不存在');
  }

  const nodeModules = path.join(testDir, 'node_modules');
  if (!fs.existsSync(nodeModules)) {
    console.log('📦 安装依赖...');
    execSync('npm install', { cwd: testDir, stdio: 'inherit' });
  }
} catch (e) {
  console.error(`❌ 环境检查失败: ${e.message}`);
  console.error('请确保已运行初始化脚本');
  process.exit(1);
}

// 检查环境变量
const requiredEnvVars = ['MIDSCENE_MODEL_BASE_URL', 'MIDSCENE_MODEL_API_KEY', 'MIDSCENE_MODEL_NAME'];
const missingVars = requiredEnvVars.filter(v => !process.env[v]);

if (missingVars.length > 0) {
  const envFile = path.join(testDir, '.env');
  if (fs.existsSync(envFile)) {
    console.log('📋 从 .env 文件加载环境变量...');
    // 简单加载 .env 文件
    const envContent = fs.readFileSync(envFile, 'utf-8');
    envContent.split('\n').forEach(line => {
      line = line.trim();
      if (line && !line.startsWith('#')) {
        const [key, ...valueParts] = line.split('=');
        if (key && valueParts.length > 0) {
          process.env[key.trim()] = valueParts.join('=').trim();
        }
      }
    });
  } else {
    console.warn(`⚠️  缺少环境变量: ${missingVars.join(', ')}`);
    console.warn('请创建 .env 文件或设置环境变量后重试');
    console.warn('参考: .env.example');
  }
}

// 执行测试
console.log(`\n🚀 执行测试: ${projectName}`);
console.log(`📁 测试目录: ${testDir}`);
console.log(`🔧 命令: ${command}\n`);

try {
  execSync(command, {
    cwd: testDir,
    stdio: 'inherit',
    env: process.env,
  });
  console.log('\n✅ 测试执行完成！');

  // 提示报告位置
  const reportPath = path.join(testDir, 'midscene_run', 'html-report');
  const midsceneReport = path.join(testDir, 'midscene_run', 'report');

  if (fs.existsSync(reportPath)) {
    console.log(`📊 Playwright 报告: ${reportPath}/index.html`);
  }
  if (fs.existsSync(midsceneReport)) {
    const htmlFiles = fs.readdirSync(midsceneReport).filter(f => f.endsWith('.html'));
    if (htmlFiles.length > 0) {
      console.log(`📊 Midscene 报告: ${midsceneReport}/${htmlFiles[0]}`);
    }
  }
} catch (e) {
  console.error('\n❌ 测试执行失败');
  process.exit(1);
}
