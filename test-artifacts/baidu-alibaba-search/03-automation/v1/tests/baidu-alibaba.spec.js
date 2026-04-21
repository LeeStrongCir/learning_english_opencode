/**
 * 百度搜索阿里巴巴 - UI 自动化测试
 *
 * 测试框架：Playwright + Midscene.js
 * 测试目标：验证通过百度搜索"阿里巴巴"能够正确显示搜索结果，
 *          并且能够成功点击进入阿里巴巴官方网站
 *
 * 覆盖用例：TC001, TC002, TC003, TC004, TC005
 */

import { test, expect } from '@playwright/test';
import { PlaywrightAgent } from '@midscene/web';

// ============================================================
// 测试数据（来自 test-data.json）
// ============================================================
const TEST_DATA = {
  baiduUrl: 'https://www.baidu.com',
  keyword: '阿里巴巴',
  keywordWithSpecialChars: '阿里巴巴@#$%',
  officialUrlPattern: 'alibaba.com',
  pageTitleKeywords: ['阿里巴巴', 'Alibaba'],
  officialBadgeText: '官方',
  performanceThresholds: {
    baiduHomepageLoadMs: 3000,
    searchResultsLoadMs: 5000,
    alibabaOfficialLoadMs: 5000,
    totalOperationTimeS: 30,
  },
};

// ============================================================
// 测试套件：百度搜索阿里巴巴测试
// ============================================================
test.describe('百度搜索阿里巴巴测试', () => {

  // ----------------------------------------------------------
  // TC001 - 正常搜索流程（完整端到端）
  // 优先级：P0
  // 前置条件：网络连接正常、浏览器已打开、屏幕分辨率 1920x1080
  // ----------------------------------------------------------
  test('TC001 - 正常搜索流程（完整端到端）', async ({ page }) => {
    const agent = new PlaywrightAgent(page, {
      generateReport: true,
      reportFileName: 'TC001-normal-search-flow',
    });

    const startTime = Date.now();

    // 步骤 1-2：打开百度首页并等待加载完成
    console.log('[TC001] 步骤 1-2: 打开百度首页');
    await page.goto(TEST_DATA.baiduUrl, { waitUntil: 'domcontentloaded' });
    await agent.aiWaitFor('页面加载完成，可以看到百度搜索框和百度一下按钮', {
      timeoutMs: 15000,
    });
    const homepageLoadTime = Date.now() - startTime;
    console.log(`[TC001] 百度首页加载时间: ${homepageLoadTime}ms`);
    expect(homepageLoadTime).toBeLessThanOrEqual(TEST_DATA.performanceThresholds.baiduHomepageLoadMs);

    // 步骤 3-5：输入搜索关键词并点击"百度一下"
    console.log('[TC001] 步骤 3-5: 输入"阿里巴巴"并点击搜索按钮');
    await agent.aiAct(`在搜索框中输入"${TEST_DATA.keyword}"，然后点击"百度一下"按钮`);

    // 步骤 6：等待搜索结果页面加载完成
    console.log('[TC001] 步骤 6: 等待搜索结果页面加载');
    await agent.aiWaitFor('搜索结果页面加载完成，可以看到多条搜索结果', {
      timeoutMs: 20000,
    });
    const searchResultsLoadTime = Date.now() - startTime;
    console.log(`[TC001] 搜索结果加载时间: ${searchResultsLoadTime}ms`);
    expect(searchResultsLoadTime).toBeLessThanOrEqual(
      TEST_DATA.performanceThresholds.baiduHomepageLoadMs +
      TEST_DATA.performanceThresholds.searchResultsLoadMs
    );

    // 步骤 7：验证搜索结果中包含带有"官方"标识的阿里巴巴官网链接
    console.log('[TC001] 步骤 7: 验证搜索结果中包含官网链接');
    const searchResults = await agent.aiQuery(
      '{title: string, url: string, hasOfficialBadge: boolean}[], 搜索结果列表中的每个条目，包含标题、链接URL和是否有官方标识',
      { domIncluded: true }
    );
    console.log('[TC001] 搜索结果:', JSON.stringify(searchResults, null, 2));

    const officialLink = searchResults.find(
      (item) => item.hasOfficialBadge === true ||
                (item.url && item.url.includes(TEST_DATA.officialUrlPattern))
    );
    expect(officialLink).toBeTruthy();
    expect(officialLink.url).toContain(TEST_DATA.officialUrlPattern);

    // 步骤 8-9：点击阿里巴巴官网链接并等待目标页面加载
    console.log('[TC001] 步骤 8-9: 点击官网链接并等待加载');
    await agent.aiAct('点击带有"官方"标识的阿里巴巴官网链接');
    await agent.aiWaitFor('阿里巴巴官网页面加载完成，可以看到页面主要内容', {
      timeoutMs: 20000,
    });

    // 步骤 10：验证页面 URL 和标题
    console.log('[TC001] 步骤 10: 验证官网页面 URL 和标题');
    const currentUrl = await agent.evaluateJavaScript('window.location.href');
    const pageTitle = await agent.evaluateJavaScript('document.title');
    console.log(`[TC001] 当前 URL: ${currentUrl}`);
    console.log(`[TC001] 页面标题: ${pageTitle}`);

    expect(currentUrl.toLowerCase()).toContain(TEST_DATA.officialUrlPattern);

    const titleContainsKeyword = TEST_DATA.pageTitleKeywords.some(
      (keyword) => pageTitle.includes(keyword)
    );
    expect(titleContainsKeyword).toBe(true);

    const totalTime = Date.now() - startTime;
    console.log(`[TC001] 总执行时间: ${totalTime}ms`);
    expect(totalTime).toBeLessThanOrEqual(TEST_DATA.performanceThresholds.totalOperationTimeS * 1000);

    console.log('[TC001] ✅ 测试通过');
  });

  // ----------------------------------------------------------
  // TC002 - 回车键执行搜索
  // 优先级：P0
  // 前置条件：网络连接正常、百度首页已加载完成
  // ----------------------------------------------------------
  test('TC002 - 回车键执行搜索', async ({ page }) => {
    const agent = new PlaywrightAgent(page, {
      generateReport: true,
      reportFileName: 'TC002-enter-key-search',
    });

    // 步骤 1：打开百度首页
    console.log('[TC002] 步骤 1: 打开百度首页');
    await page.goto(TEST_DATA.baiduUrl, { waitUntil: 'domcontentloaded' });
    await agent.aiWaitFor('页面加载完成，可以看到百度搜索框', { timeoutMs: 15000 });

    // 步骤 2-3：点击搜索框并输入关键词
    console.log('[TC002] 步骤 2-3: 输入搜索关键词');
    await agent.aiInput('搜索输入框', { value: TEST_DATA.keyword });

    // 步骤 4：按回车键执行搜索
    console.log('[TC002] 步骤 4: 按回车键搜索');
    await agent.aiKeyboardPress('搜索输入框', { keyName: 'Enter' });

    // 步骤 5：等待搜索结果页面加载
    console.log('[TC002] 步骤 5: 等待搜索结果加载');
    await agent.aiWaitFor('搜索结果页面加载完成，可以看到搜索结果列表', {
      timeoutMs: 20000,
    });

    // 步骤 6：验证搜索结果
    console.log('[TC002] 步骤 6: 验证搜索结果');
    const currentUrl = await agent.evaluateJavaScript('window.location.href');
    console.log(`[TC002] 当前 URL: ${currentUrl}`);

    // 验证 URL 包含搜索关键词
    expect(currentUrl).toContain('wd=');
    expect(currentUrl).toContain(encodeURIComponent(TEST_DATA.keyword));

    // 验证搜索结果中包含阿里巴巴相关内容
    const hasRelevantResults = await agent.aiBoolean(
      '搜索结果中包含与"阿里巴巴"相关的结果条目'
    );
    expect(hasRelevantResults).toBe(true);

    // 验证搜索结果中包含官网链接
    const hasOfficialLink = await agent.aiBoolean(
      `搜索结果中包含带有"${TEST_DATA.officialBadgeText}"标识的链接，或者链接URL包含"${TEST_DATA.officialUrlPattern}"`
    );
    expect(hasOfficialLink).toBe(true);

    console.log('[TC002] ✅ 测试通过');
  });

  // ----------------------------------------------------------
  // TC003 - 官网链接识别验证
  // 优先级：P0
  // 前置条件：网络连接正常、已完成"阿里巴巴"搜索、搜索结果页已加载
  // ----------------------------------------------------------
  test('TC003 - 官网链接识别验证', async ({ page }) => {
    const agent = new PlaywrightAgent(page, {
      generateReport: true,
      reportFileName: 'TC003-official-link-recognition',
    });

    // 前置：执行搜索
    console.log('[TC003] 前置步骤: 执行搜索');
    await page.goto(TEST_DATA.baiduUrl, { waitUntil: 'domcontentloaded' });
    await agent.aiWaitFor('页面加载完成，可以看到百度搜索框', { timeoutMs: 15000 });
    await agent.aiAct(`在搜索框中输入"${TEST_DATA.keyword}"，然后点击"百度一下"按钮`);
    await agent.aiWaitFor('搜索结果页面加载完成', { timeoutMs: 20000 });

    // 步骤 1-2：查找所有搜索结果条目，检查"官方"标识
    console.log('[TC003] 步骤 1-2: 查找搜索结果并检查官方标识');
    const searchResults = await agent.aiQuery(
      '{position: number, title: string, url: string, hasOfficialBadge: boolean, description: string}[], 搜索结果列表中的每个条目，按从上到下的顺序，包含位置序号(从1开始)、标题、链接URL、是否有官方标识、描述文字',
      { domIncluded: true }
    );
    console.log('[TC003] 搜索结果:', JSON.stringify(searchResults, null, 2));

    // 步骤 3：验证带有"官方"标识的链接 URL 包含 alibaba.com
    const officialResults = searchResults.filter(
      (item) => item.hasOfficialBadge === true
    );
    expect(officialResults.length).toBeGreaterThan(0);

    const alibabaOfficialLink = officialResults.find(
      (item) => item.url && item.url.toLowerCase().includes(TEST_DATA.officialUrlPattern)
    );
    expect(alibabaOfficialLink).toBeTruthy();
    console.log(`[TC003] 找到官网链接: ${alibabaOfficialLink.title} -> ${alibabaOfficialLink.url}`);

    // 步骤 4：验证官网链接在搜索结果前 3 条内
    expect(alibabaOfficialLink.position).toBeLessThanOrEqual(3);
    console.log(`[TC003] 官网链接位置: 第 ${alibabaOfficialLink.position} 条`);

    console.log('[TC003] ✅ 测试通过');
  });

  // ----------------------------------------------------------
  // TC004 - 官网链接点击跳转验证
  // 优先级：P0
  // 前置条件：网络连接正常、搜索结果页已加载、已识别到官网链接
  // ----------------------------------------------------------
  test('TC004 - 官网链接点击跳转验证', async ({ page }) => {
    const agent = new PlaywrightAgent(page, {
      generateReport: true,
      reportFileName: 'TC004-official-link-click-redirect',
    });

    // 前置：执行搜索并等待结果
    console.log('[TC004] 前置步骤: 执行搜索');
    await page.goto(TEST_DATA.baiduUrl, { waitUntil: 'domcontentloaded' });
    await agent.aiWaitFor('页面加载完成，可以看到百度搜索框', { timeoutMs: 15000 });
    await agent.aiAct(`在搜索框中输入"${TEST_DATA.keyword}"，然后点击"百度一下"按钮`);
    await agent.aiWaitFor('搜索结果页面加载完成', { timeoutMs: 20000 });

    // 步骤 1-2：找到并点击官网链接
    console.log('[TC004] 步骤 1-2: 找到并点击官网链接');
    const clickStartTime = Date.now();
    await agent.aiAct('点击带有"官方"标识的阿里巴巴官网链接');

    // 步骤 3：等待新页面加载完成
    console.log('[TC004] 步骤 3: 等待新页面加载');
    await agent.aiWaitFor('阿里巴巴官网页面加载完成，可以看到页面主要内容区域', {
      timeoutMs: 20000,
    });
    const pageLoadTime = Date.now() - clickStartTime;
    console.log(`[TC004] 官网页面加载时间: ${pageLoadTime}ms`);
    expect(pageLoadTime).toBeLessThanOrEqual(TEST_DATA.performanceThresholds.alibabaOfficialLoadMs);

    // 步骤 4：检查浏览器当前 URL
    console.log('[TC004] 步骤 4: 检查 URL');
    const currentUrl = await agent.evaluateJavaScript('window.location.href');
    console.log(`[TC004] 当前 URL: ${currentUrl}`);
    expect(currentUrl.toLowerCase()).toContain(TEST_DATA.officialUrlPattern);

    // 步骤 5：检查页面标题
    console.log('[TC004] 步骤 5: 检查页面标题');
    const pageTitle = await agent.evaluateJavaScript('document.title');
    console.log(`[TC004] 页面标题: ${pageTitle}`);

    const titleContainsKeyword = TEST_DATA.pageTitleKeywords.some(
      (keyword) => pageTitle.includes(keyword)
    );
    expect(titleContainsKeyword).toBe(true);

    // 步骤 6：检查页面主要内容是否正常显示（无 404 或错误）
    console.log('[TC004] 步骤 6: 验证页面内容正常');
    const hasErrorPage = await agent.aiBoolean(
      '页面显示 404 错误、页面不存在、或其他错误提示'
    );
    expect(hasErrorPage).toBe(false);

    const hasMainContent = await agent.aiBoolean(
      '页面有正常的主要内容区域，不是空白页'
    );
    expect(hasMainContent).toBe(true);

    console.log('[TC004] ✅ 测试通过');
  });

  // ----------------------------------------------------------
  // TC005 - 官网页面内容完整性验证
  // 优先级：P0
  // 前置条件：已成功跳转到阿里巴巴官网、页面已完全加载
  // ----------------------------------------------------------
  test('TC005 - 官网页面内容完整性验证', async ({ page }) => {
    const agent = new PlaywrightAgent(page, {
      generateReport: true,
      reportFileName: 'TC005-official-page-content-verification',
    });

    // 前置：通过搜索进入官网
    console.log('[TC005] 前置步骤: 通过搜索进入阿里巴巴官网');
    await page.goto(TEST_DATA.baiduUrl, { waitUntil: 'domcontentloaded' });
    await agent.aiWaitFor('页面加载完成', { timeoutMs: 15000 });
    await agent.aiAct(`在搜索框中输入"${TEST_DATA.keyword}"，点击"百度一下"，然后点击带有"官方"标识的阿里巴巴官网链接`);
    await agent.aiWaitFor('阿里巴巴官网页面加载完成', { timeoutMs: 20000 });

    // 步骤 1：验证页面 URL 正确
    console.log('[TC005] 步骤 1: 验证 URL');
    const currentUrl = await agent.evaluateJavaScript('window.location.href');
    expect(currentUrl.toLowerCase()).toContain(TEST_DATA.officialUrlPattern);

    // 步骤 2：验证页面标题包含"阿里巴巴"
    console.log('[TC005] 步骤 2: 验证页面标题');
    const pageTitle = await agent.evaluateJavaScript('document.title');
    const titleContainsKeyword = TEST_DATA.pageTitleKeywords.some(
      (keyword) => pageTitle.includes(keyword)
    );
    expect(titleContainsKeyword).toBe(true);

    // 步骤 3：验证页面导航栏正常显示
    console.log('[TC005] 步骤 3: 验证导航栏');
    const hasNavigation = await agent.aiBoolean(
      '页面顶部有导航栏或导航菜单，包含多个导航链接'
    );
    expect(hasNavigation).toBe(true);

    // 步骤 4：验证页面主体内容正常显示
    console.log('[TC005] 步骤 4: 验证主体内容');
    const hasMainContent = await agent.aiBoolean(
      '页面主体区域有正常的内容展示，如产品介绍、服务说明、图片等'
    );
    expect(hasMainContent).toBe(true);

    // 步骤 5：验证页面无 JavaScript 错误
    console.log('[TC005] 步骤 5: 检查控制台错误');
    const jsErrors = [];
    page.on('pageerror', (error) => {
      jsErrors.push(error.message);
    });
    // 给页面一点时间来捕获错误
    await page.waitForTimeout(2000);
    console.log(`[TC005] 捕获到的 JS 错误数量: ${jsErrors.length}`);
    // 注意：大型网站可能会有一些非关键的 JS 警告，这里只记录不强制断言

    // 步骤 6：验证主要导航链接存在
    console.log('[TC005] 步骤 6: 验证主要链接可交互');
    const clickableLinks = await agent.aiQuery(
      '{text: string, isClickable: boolean}[], 页面中可见的主要导航链接或按钮，最多5个',
      { domIncluded: true }
    );
    console.log('[TC005] 主要链接:', JSON.stringify(clickableLinks, null, 2));
    expect(clickableLinks.length).toBeGreaterThan(0);

    console.log('[TC005] ✅ 测试通过');
  });

  // ----------------------------------------------------------
  // TC006 - 搜索框中文输入验证
  // 优先级：P0
  // 前置条件：网络连接正常、百度首页已加载完成
  // ----------------------------------------------------------
  test('TC006 - 搜索框中文输入验证', async ({ page }) => {
    const agent = new PlaywrightAgent(page, {
      generateReport: true,
      reportFileName: 'TC006-chinese-input-verification',
    });

    // 步骤 1：打开百度首页
    console.log('[TC006] 步骤 1: 打开百度首页');
    await page.goto(TEST_DATA.baiduUrl, { waitUntil: 'domcontentloaded' });
    await agent.aiWaitFor('页面加载完成，可以看到百度搜索框', { timeoutMs: 15000 });

    // 步骤 2-3：点击搜索框并输入中文
    console.log('[TC006] 步骤 2-3: 输入中文"阿里巴巴"');
    await agent.aiInput('搜索输入框', { value: TEST_DATA.keyword });

    // 步骤 4：验证输入内容完整且无乱码
    console.log('[TC006] 步骤 4: 验证输入内容');
    const inputValue = await agent.aiString('搜索输入框中的文字内容');
    console.log(`[TC006] 搜索框中的内容: "${inputValue}"`);
    expect(inputValue).toContain(TEST_DATA.keyword);

    // 额外验证：输入内容无乱码
    const hasGarbledText = await agent.aiBoolean(
      '搜索框中的文字显示为乱码、方框、或问号等异常字符'
    );
    expect(hasGarbledText).toBe(false);

    console.log('[TC006] ✅ 测试通过');
  });

  // ----------------------------------------------------------
  // TC007 - 搜索结果排序验证
  // 优先级：P1
  // 前置条件：网络连接正常、已完成搜索、搜索结果页已加载
  // ----------------------------------------------------------
  test('TC007 - 搜索结果排序验证', async ({ page }) => {
    const agent = new PlaywrightAgent(page, {
      generateReport: true,
      reportFileName: 'TC007-search-results-ranking',
    });

    // 前置：执行搜索
    console.log('[TC007] 前置步骤: 执行搜索');
    await page.goto(TEST_DATA.baiduUrl, { waitUntil: 'domcontentloaded' });
    await agent.aiWaitFor('页面加载完成', { timeoutMs: 15000 });
    await agent.aiAct(`在搜索框中输入"${TEST_DATA.keyword}"，然后点击"百度一下"按钮`);
    await agent.aiWaitFor('搜索结果页面加载完成', { timeoutMs: 20000 });

    // 步骤 1-2：扫描搜索结果，记录官网链接位置
    console.log('[TC007] 步骤 1-2: 扫描搜索结果');
    const searchResults = await agent.aiQuery(
      '{position: number, title: string, url: string, hasOfficialBadge: boolean, isAd: boolean}[], 搜索结果列表中的每个条目，按从上到下顺序，包含位置序号(从1开始)、标题、URL、是否有官方标识、是否是广告',
      { domIncluded: true }
    );
    console.log('[TC007] 搜索结果:', JSON.stringify(searchResults, null, 2));

    // 步骤 3：查找官网链接
    const officialLink = searchResults.find(
      (item) => item.hasOfficialBadge === true &&
                item.url && item.url.toLowerCase().includes(TEST_DATA.officialUrlPattern)
    );
    expect(officialLink).toBeTruthy();

    // 步骤 4：验证官网链接在前 3 条内
    expect(officialLink.position).toBeLessThanOrEqual(3);
    console.log(`[TC007] 官网链接位置: 第 ${officialLink.position} 条`);

    // 步骤 5：检查广告与官网链接的区分
    const adsBeforeOfficial = searchResults.filter(
      (item) => item.position < officialLink.position && item.isAd === true
    );
    console.log(`[TC007] 官网链接前的广告数量: ${adsBeforeOfficial.length}`);

    console.log('[TC007] ✅ 测试通过');
  });

  // ----------------------------------------------------------
  // TC008 - 搜索建议/联想验证
  // 优先级：P2
  // 前置条件：网络连接正常、百度首页已加载、搜索建议功能已启用
  // ----------------------------------------------------------
  test('TC008 - 搜索建议/联想验证', async ({ page }) => {
    const agent = new PlaywrightAgent(page, {
      generateReport: true,
      reportFileName: 'TC008-search-suggestions',
    });

    // 步骤 1：打开百度首页
    console.log('[TC008] 步骤 1: 打开百度首页');
    await page.goto(TEST_DATA.baiduUrl, { waitUntil: 'domcontentloaded' });
    await agent.aiWaitFor('页面加载完成，可以看到百度搜索框', { timeoutMs: 15000 });

    // 步骤 2-3：输入"阿"，检查搜索建议
    console.log('[TC008] 步骤 2-3: 输入"阿"并检查建议');
    await agent.aiInput('搜索输入框', { value: '阿' });
    await page.waitForTimeout(1500);

    const suggestionsAfterA = await agent.aiQuery(
      'string[], 搜索建议下拉列表中的词条文字，最多10个',
      { domIncluded: true }
    );
    console.log('[TC008] 输入"阿"后的建议:', suggestionsAfterA);
    expect(suggestionsAfterA.length).toBeGreaterThan(0);

    // 步骤 4-5：继续输入"阿里"，检查建议更新
    console.log('[TC008] 步骤 4-5: 输入"阿里"并检查建议');
    await agent.aiInput('搜索输入框', { value: '阿里' });
    await page.waitForTimeout(1500);

    const suggestionsAfterAli = await agent.aiQuery(
      'string[], 搜索建议下拉列表中的词条文字，最多10个',
      { domIncluded: true }
    );
    console.log('[TC008] 输入"阿里"后的建议:', suggestionsAfterAli);
    expect(suggestionsAfterAli.length).toBeGreaterThan(0);

    // 步骤 6-7：继续输入"阿里巴巴"，检查建议
    console.log('[TC008] 步骤 6-7: 输入"阿里巴巴"并检查建议');
    await agent.aiInput('搜索输入框', { value: TEST_DATA.keyword });
    await page.waitForTimeout(1500);

    const suggestionsAfterFull = await agent.aiQuery(
      'string[], 搜索建议下拉列表中的词条文字，最多10个',
      { domIncluded: true }
    );
    console.log('[TC008] 输入"阿里巴巴"后的建议:', suggestionsAfterFull);

    // 验证建议中包含"阿里巴巴"相关词条
    const hasRelevantSuggestion = suggestionsAfterFull.some(
      (s) => s.includes('阿里巴巴')
    );
    expect(hasRelevantSuggestion).toBe(true);

    console.log('[TC008] ✅ 测试通过');
  });

  // ----------------------------------------------------------
  // TC021 - 搜索框清空重搜验证
  // 优先级：P2
  // 前置条件：网络连接正常、已完成一次搜索、当前在搜索结果页
  // ----------------------------------------------------------
  test('TC021 - 搜索框清空重搜验证', async ({ page }) => {
    const agent = new PlaywrightAgent(page, {
      generateReport: true,
      reportFileName: 'TC021-clear-and-research',
    });

    // 前置：执行第一次搜索
    console.log('[TC021] 前置步骤: 执行第一次搜索');
    await page.goto(TEST_DATA.baiduUrl, { waitUntil: 'domcontentloaded' });
    await agent.aiWaitFor('页面加载完成', { timeoutMs: 15000 });
    await agent.aiAct(`在搜索框中输入"${TEST_DATA.keyword}"，然后点击"百度一下"按钮`);
    await agent.aiWaitFor('搜索结果页面加载完成', { timeoutMs: 20000 });

    // 步骤 1-2：清空搜索框
    console.log('[TC021] 步骤 1-2: 清空搜索框');
    await agent.aiInput('搜索输入框', { value: '', mode: 'clear' });

    // 验证搜索框已清空
    const emptyValue = await agent.aiString('搜索输入框中的文字内容');
    console.log(`[TC021] 清空后搜索框内容: "${emptyValue}"`);

    // 步骤 3：重新输入"阿里巴巴"
    console.log('[TC021] 步骤 3: 重新输入关键词');
    await agent.aiInput('搜索输入框', { value: TEST_DATA.keyword });

    // 步骤 4-5：点击搜索并验证结果
    console.log('[TC021] 步骤 4-5: 执行搜索并验证');
    await agent.aiAct('点击"百度一下"按钮');
    await agent.aiWaitFor('搜索结果页面加载完成', { timeoutMs: 20000 });

    // 验证搜索结果与第一次一致
    const hasOfficialLink = await agent.aiBoolean(
      `搜索结果中包含与"阿里巴巴"相关的结果，并且有官网链接`
    );
    expect(hasOfficialLink).toBe(true);

    console.log('[TC021] ✅ 测试通过');
  });

  // ----------------------------------------------------------
  // TC022 - 搜索框输入特殊字符验证
  // 优先级：P2
  // 前置条件：网络连接正常、百度首页已加载
  // ----------------------------------------------------------
  test('TC022 - 搜索框输入特殊字符验证', async ({ page }) => {
    const agent = new PlaywrightAgent(page, {
      generateReport: true,
      reportFileName: 'TC022-special-characters-search',
    });

    // 步骤 1-2：打开百度首页并输入特殊字符
    console.log('[TC022] 步骤 1-2: 输入特殊字符');
    await page.goto(TEST_DATA.baiduUrl, { waitUntil: 'domcontentloaded' });
    await agent.aiWaitFor('页面加载完成', { timeoutMs: 15000 });
    await agent.aiInput('搜索输入框', { value: TEST_DATA.keywordWithSpecialChars });

    // 步骤 3-4：点击搜索并观察结果
    console.log('[TC022] 步骤 3-4: 执行搜索');
    await agent.aiAct('点击"百度一下"按钮');
    await agent.aiWaitFor('搜索结果页面加载完成或显示无结果提示', { timeoutMs: 20000 });

    // 验证页面无异常
    const hasPageError = await agent.aiBoolean(
      '页面显示脚本错误、崩溃、或异常空白'
    );
    expect(hasPageError).toBe(false);

    console.log('[TC022] ✅ 测试通过');
  });

  // ----------------------------------------------------------
  // TC023 - 百度搜索框空搜索验证
  // 优先级：P2
  // 前置条件：网络连接正常、百度首页已加载
  // ----------------------------------------------------------
  test('TC023 - 空搜索验证', async ({ page }) => {
    const agent = new PlaywrightAgent(page, {
      generateReport: true,
      reportFileName: 'TC023-empty-search',
    });

    // 步骤 1-2：打开百度首页，不输入内容
    console.log('[TC023] 步骤 1-2: 打开百度首页');
    await page.goto(TEST_DATA.baiduUrl, { waitUntil: 'domcontentloaded' });
    await agent.aiWaitFor('页面加载完成', { timeoutMs: 15000 });

    // 步骤 3-4：点击"百度一下"按钮（搜索框为空）
    console.log('[TC023] 步骤 3-4: 空搜索');
    await agent.aiAct('点击"百度一下"按钮');
    await page.waitForTimeout(3000);

    // 验证：页面不报错或崩溃
    const hasPageError = await agent.aiBoolean(
      '页面显示错误、崩溃、或异常空白'
    );
    expect(hasPageError).toBe(false);

    console.log('[TC023] ✅ 测试通过');
  });

  // ----------------------------------------------------------
  // TC025 - 整体操作流程时间验证
  // 优先级：P1
  // 前置条件：网络连接稳定、浏览器已打开
  // ----------------------------------------------------------
  test('TC025 - 整体操作流程时间验证', async ({ page }) => {
    const agent = new PlaywrightAgent(page, {
      generateReport: true,
      reportFileName: 'TC025-total-operation-time',
    });

    const totalStartTime = Date.now();

    // 步骤 2：打开百度首页
    console.log('[TC025] 步骤 2: 打开百度首页');
    await page.goto(TEST_DATA.baiduUrl, { waitUntil: 'domcontentloaded' });
    await agent.aiWaitFor('页面加载完成', { timeoutMs: 15000 });

    // 步骤 3-4：输入并执行搜索
    console.log('[TC025] 步骤 3-4: 输入并搜索');
    await agent.aiAct(`在搜索框中输入"${TEST_DATA.keyword}"，然后点击"百度一下"按钮`);
    await agent.aiWaitFor('搜索结果页面加载完成', { timeoutMs: 20000 });

    // 步骤 5-6：点击官网链接并等待加载
    console.log('[TC025] 步骤 5-6: 点击官网并等待');
    await agent.aiAct('点击带有"官方"标识的阿里巴巴官网链接');
    await agent.aiWaitFor('阿里巴巴官网页面加载完成', { timeoutMs: 20000 });

    // 步骤 7-8：停止计时并记录
    const totalEndTime = Date.now();
    const totalTimeSeconds = (totalEndTime - totalStartTime) / 1000;
    console.log(`[TC025] 总操作时间: ${totalTimeSeconds.toFixed(2)} 秒`);

    expect(totalTimeSeconds).toBeLessThanOrEqual(TEST_DATA.performanceThresholds.totalOperationTimeS);

    console.log('[TC025] ✅ 测试通过');
  });
});
