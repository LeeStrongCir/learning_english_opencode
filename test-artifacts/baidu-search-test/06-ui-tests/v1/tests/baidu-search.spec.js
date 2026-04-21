/**
 * 百度搜索阿里巴巴 - UI 自动化测试
 * 
 * 测试场景：打开百度搜索阿里巴巴，进入阿里巴巴官网
 * 
 * 测试步骤：
 * 1. 打开百度首页 (https://www.baidu.com)
 * 2. 在搜索框输入"阿里巴巴"
 * 3. 点击搜索按钮
 * 4. 等待搜索结果加载
 * 5. 在搜索结果中找到并点击"阿里巴巴"官网链接
 * 6. 验证成功进入阿里巴巴官网页面
 * 
 * 技术栈：Playwright + Midscene.js
 * 模型：qwen3-vl-plus
 */

import { test, expect } from '@playwright/test';
import { PlaywrightAgent } from '@midscene/web';

// 测试配置
const CONFIG = {
  BAIDU_URL: 'https://www.baidu.com',
  SEARCH_KEYWORD: '阿里巴巴',
  ALIBABA_OFFICIAL_URL: 'alibaba.com',
  TIMEOUT_MS: 30000,
};

test.describe('百度搜索阿里巴巴测试', () => {

  test('打开百度搜索阿里巴巴，进入阿里巴巴官网', async ({ page }) => {
    // 创建 Midscene Agent 实例
    const agent = new PlaywrightAgent(page);

    // 步骤 1：打开百度首页
    console.log('步骤 1：打开百度首页');
    await page.goto(CONFIG.BAIDU_URL, { 
      waitUntil: 'domcontentloaded',
      timeout: CONFIG.TIMEOUT_MS 
    });

    // 等待页面完全加载，确认百度首页已打开
    await agent.aiWaitFor('百度首页加载完成，可以看到搜索框和百度一下按钮', {
      timeoutMs: CONFIG.TIMEOUT_MS,
    });

    // 步骤 2-4：输入搜索关键词并点击搜索，等待结果加载
    console.log('步骤 2-4：输入"阿里巴巴"并搜索');
    await agent.aiAct(`在搜索框中输入"${CONFIG.SEARCH_KEYWORD}"，然后点击"百度一下"搜索按钮，等待搜索结果页面加载完成`);

    // 验证搜索结果页面已加载
    await agent.aiWaitFor('页面显示搜索结果列表，包含多个相关链接', {
      timeoutMs: CONFIG.TIMEOUT_MS,
    });

    // 步骤 5：在搜索结果中找到并点击阿里巴巴官网链接
    console.log('步骤 5：点击阿里巴巴官网链接');
    await agent.aiAct('在搜索结果中找到"阿里巴巴"官方网站的链接并点击它');

    // 等待新页面加载完成
    await agent.aiWaitFor('页面加载完成，显示阿里巴巴官方网站的内容', {
      timeoutMs: CONFIG.TIMEOUT_MS,
    });

    // 步骤 6：验证成功进入阿里巴巴官网页面
    console.log('步骤 6：验证进入阿里巴巴官网');
    
    // 使用 AI 断言验证页面是否为阿里巴巴官网
    await agent.aiAssert('当前页面是阿里巴巴官方网站，页面标题或内容包含"阿里巴巴"或"Alibaba"');

    // 额外验证：检查 URL 是否包含 alibaba.com
    const currentUrl = page.url();
    console.log(`当前页面 URL: ${currentUrl}`);
    expect(currentUrl.toLowerCase()).toContain(CONFIG.ALIBABA_OFFICIAL_URL.toLowerCase());

    // 提取并打印页面标题用于验证
    const pageTitle = await page.title();
    console.log(`页面标题: ${pageTitle}`);
    expect(pageTitle).toBeTruthy();
    expect(pageTitle.length).toBeGreaterThan(0);
  });
});
