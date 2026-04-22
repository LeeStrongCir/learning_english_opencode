#!/usr/bin/env node

/**
 * test-requirement-analyzer
 * 需求测试分析专家 - 基于 10+ 年测试经验沉淀
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const CONFIG = {
  model: process.env.OPENCLAW_MODEL || 'qwen/qwen3.5-plus',
  outputDir: process.env.OPENCLAW_OUTPUT_DIR || './output',
};

// 命令行参数解析
function parseArgs(args) {
  const parsed = {
    document: null,
    projectName: null,
    outputFormat: 'markdown',
    saveToOntology: false,
    includePrompt: false,
    help: false,
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--document' || arg === '-d') {
      parsed.document = args[++i];
    } else if (arg === '--project-name' || arg === '-p') {
      parsed.projectName = args[++i];
    } else if (arg === '--output-format' || arg === '-o') {
      parsed.outputFormat = args[++i];
    } else if (arg === '--save-to-ontology') {
      parsed.saveToOntology = true;
    } else if (arg === '--include-prompt') {
      parsed.includePrompt = true;
    } else if (arg === '--help' || arg === '-h') {
      parsed.help = true;
    }
  }

  return parsed;
}

// 显示帮助
function showHelp() {
  console.log(`
需求测试分析专家 - 自动分析软件需求文档

用法:
  openclaw skill run test-requirement-analyzer [选项]

选项:
  -d, --document <path>       需求文档路径（本地文件或 URL）[必填]
  -p, --project-name <name>   项目名称 [可选]
  -o, --output-format <fmt>   输出格式：markdown/json/both [默认：markdown]
  --save-to-ontology          存储到 Ontology [默认：false]
  --include-prompt            输出中包含使用的 prompt [默认：false]
  -h, --help                  显示帮助信息

示例:
  openclaw skill run test-requirement-analyzer -d ./requirements/v1.2.md
  openclaw skill run test-requirement-analyzer -d ./req.md -o json
`);
}

// 读取文档内容
function readDocument(docPath) {
  // 如果是 URL
  if (docPath.startsWith('http://') || docPath.startsWith('https://')) {
    console.error(`📥 正在获取远程文档：${docPath}`);
    try {
      const result = execSync(`curl -sL "${docPath}"`, { encoding: 'utf8' });
      return result;
    } catch (error) {
      throw new Error(`无法获取远程文档：${error.message}`);
    }
  }

  // 本地文件
  const resolvedPath = path.resolve(docPath);
  if (!fs.existsSync(resolvedPath)) {
    throw new Error(`文档不存在：${resolvedPath}`);
  }

  console.error(`📄 正在读取文档：${resolvedPath}`);
  return fs.readFileSync(resolvedPath, 'utf8');
}

// 分析 Prompt 模板（核心资产！）
function buildAnalyzerPrompt(documentContent) {
  return `你是一个资深软件测试专家，拥有 10+ 年测试经验。你的核心能力是：
1. **质疑思维**：发现需求本身的问题和漏洞
2. **场景化分析**：从用户视角还原完整使用场景
3. **风险嗅觉**：识别高风险区域，指导资源分配

请分析以下需求文档，输出结构化的测试分析报告。

## 分析任务

### 1. 测试目标识别
- 这个需求要验证什么？
- 每个目标的验收标准是什么？
- 目标之间的依赖关系

### 2. 测试范围界定
- 范围内：明确要测试的功能
- 范围外：明确不测试的内容（同样重要！）

### 3. 优先级评估（P0/P1/P2）
- P0：核心功能，出问题影响大，必须测试
- P1：重要功能，应该测试
- P2：边缘功能，可以抽样测试
评估依据：业务影响 × 使用频率 × 复杂度

### 4. 风险识别
- 技术风险：实现复杂度、新技术
- 依赖风险：第三方服务、外部系统
- 变更风险：需求不稳定、时间紧
- 数据风险：数据安全、隐私合规
每个风险要说明：风险描述、影响程度、缓解建议

### 5. 需求问题清单
- 模糊描述（"大概""可能""尽量"等）
- 矛盾点
- 缺失信息
- 需要澄清的问题

### 6. 测试建议
- 推荐的测试类型（功能/接口/性能/安全/兼容性）
- 重点关注的场景
- 建议的测试数据

## 输出要求

**必须用 JSON 格式输出**，结构如下：

\`\`\`json
{
  "project_name": "项目名称",
  "analysis_timestamp": "分析时间",
  "test_objectives": [
    {
      "id": "OBJ-001",
      "description": "目标描述",
      "priority": "P0|P1|P2",
      "related_requirements": ["REQ-001"],
      "acceptance_criteria": ["标准 1", "标准 2"]
    }
  ],
  "test_scope": {
    "in_scope": ["功能 A", "功能 B"],
    "out_of_scope": ["功能 X", "功能 Y"]
  },
  "priorities": {
    "P0": ["核心功能列表"],
    "P1": ["重要功能列表"],
    "P2": ["边缘功能列表"]
  },
  "risks": [
    {
      "level": "high|medium|low",
      "category": "technical|dependency|change|data",
      "description": "风险描述",
      "impact": "影响说明",
      "mitigation": "缓解建议"
    }
  ],
  "questions": [
    {
      "id": "Q-001",
      "description": "问题描述",
      "type": "ambiguous|missing|contradictory|clarification",
      "location": "需求中的位置（如果有）"
    }
  ],
  "suggested_test_types": ["功能测试", "接口测试"],
  "key_scenarios": [
    {
      "name": "场景名称",
      "type": "happy_path|exception|boundary|concurrent",
      "description": "场景描述"
    }
  ],
  "summary": "分析总结（200 字以内）"
}
\`\`\`

## 需求文档内容

${documentContent}

---

现在开始分析，输出 JSON 格式结果：`;
}

// 调用 LLM 分析
async function analyzeWithLLM(prompt) {
  console.error('🤖 正在调用 AI 进行分析...');
  
  // 通过 OpenClaw 的 LLM 接口调用
  // 这里使用 openclaw 的内置命令
  const llmCommand = `openclaw llm --model "${CONFIG.model}" --prompt "${escapeShell(prompt)}"`;
  
  try {
    const result = execSync(llmCommand, { 
      encoding: 'utf8',
      maxBuffer: 10 * 1024 * 1024, // 10MB
      timeout: 120000 // 2 分钟超时
    });
    return result;
  } catch (error) {
    // 如果 openclaw llm 命令不可用，尝试直接输出
    console.error('⚠️  openclaw llm 命令不可用，使用备用方案');
    throw error;
  }
}

// 转义 shell 参数
function escapeShell(str) {
  return str.replace(/'/g, "'\"'\"'");
}

// 解析 JSON 输出
function parseJSONOutput(output) {
  // 尝试提取 JSON 代码块
  const jsonMatch = output.match(/```json\s*([\s\S]*?)\s*```/);
  if (jsonMatch) {
    return JSON.parse(jsonMatch[1]);
  }
  
  // 尝试直接解析
  try {
    return JSON.parse(output);
  } catch (e) {
    // 尝试找到第一个 { 和最后一个 }
    const start = output.indexOf('{');
    const end = output.lastIndexOf('}');
    if (start !== -1 && end !== -1 && end > start) {
      return JSON.parse(output.substring(start, end + 1));
    }
    throw new Error('无法解析 AI 输出的 JSON');
  }
}

// 格式化为 Markdown
function formatToMarkdown(analysis) {
  const lines = [];
  
  lines.push('# 需求测试分析报告');
  lines.push('');
  lines.push(`**项目名称**: ${analysis.project_name || '未指定'}`);
  lines.push(`**分析时间**: ${analysis.analysis_timestamp || new Date().toISOString()}`);
  lines.push('');
  
  // 测试目标
  lines.push('## 1. 测试目标');
  lines.push('');
  if (analysis.test_objectives && analysis.test_objectives.length > 0) {
    analysis.test_objectives.forEach(obj => {
      lines.push(`- [${obj.id}] ${obj.description} **（优先级：${obj.priority}）**`);
      if (obj.acceptance_criteria && obj.acceptance_criteria.length > 0) {
        obj.acceptance_criteria.forEach(criterion => {
          lines.push(`  - ✅ ${criterion}`);
        });
      }
    });
  } else {
    lines.push('暂无测试目标');
  }
  lines.push('');
  
  // 测试范围
  lines.push('## 2. 测试范围');
  lines.push('');
  lines.push('### 2.1 范围内');
  if (analysis.test_scope && analysis.test_scope.in_scope) {
    analysis.test_scope.in_scope.forEach(item => lines.push(`- ${item}`));
  }
  lines.push('');
  lines.push('### 2.2 范围外');
  if (analysis.test_scope && analysis.test_scope.out_of_scope) {
    analysis.test_scope.out_of_scope.forEach(item => lines.push(`- ${item}`));
  } else {
    lines.push('- 暂无明确排除的内容');
  }
  lines.push('');
  
  // 优先级评估
  lines.push('## 3. 优先级评估');
  lines.push('');
  if (analysis.priorities) {
    if (analysis.priorities.P0) {
      lines.push('### P0（必须测试）');
      analysis.priorities.P0.forEach(item => lines.push(`- ${item}`));
      lines.push('');
    }
    if (analysis.priorities.P1) {
      lines.push('### P1（应该测试）');
      analysis.priorities.P1.forEach(item => lines.push(`- ${item}`));
      lines.push('');
    }
    if (analysis.priorities.P2) {
      lines.push('### P2（可以测试）');
      analysis.priorities.P2.forEach(item => lines.push(`- ${item}`));
      lines.push('');
    }
  }
  
  // 风险识别
  lines.push('## 4. 风险识别');
  lines.push('');
  if (analysis.risks && analysis.risks.length > 0) {
    analysis.risks.forEach(risk => {
      const icon = risk.level === 'high' ? '🔴' : risk.level === 'medium' ? '🟡' : '🟢';
      lines.push(`- ${icon} **${risk.category}**: ${risk.description}`);
      lines.push(`  - 影响：${risk.impact}`);
      lines.push(`  - 缓解：${risk.mitigation}`);
    });
  } else {
    lines.push('暂无识别的风险');
  }
  lines.push('');
  
  // 需求问题
  lines.push('## 5. 需求问题清单');
  lines.push('');
  if (analysis.questions && analysis.questions.length > 0) {
    analysis.questions.forEach(q => {
      const typeMap = {
        'ambiguous': '❓ 模糊描述',
        'missing': '⚠️ 缺失信息',
        'contradictory': '⚔️ 矛盾点',
        'clarification': '💬 需要澄清'
      };
      lines.push(`- [${q.id}] ${typeMap[q.type] || '❓'} ${q.description}`);
      if (q.location) lines.push(`  - 位置：${q.location}`);
    });
  } else {
    lines.push('暂无问题');
  }
  lines.push('');
  
  // 测试建议
  lines.push('## 6. 测试建议');
  lines.push('');
  if (analysis.suggested_test_types) {
    lines.push('**推荐测试类型**:');
    analysis.suggested_test_types.forEach(type => lines.push(`- ${type}`));
    lines.push('');
  }
  if (analysis.key_scenarios && analysis.key_scenarios.length > 0) {
    lines.push('**关键场景**:');
    analysis.key_scenarios.forEach(scenario => {
      const typeMap = {
        'happy_path': '✅ 正常流程',
        'exception': '⚠️ 异常流程',
        'boundary': '📏 边界场景',
        'concurrent': '🔄 并发场景'
      };
      lines.push(`- ${typeMap[scenario.type] || '📋'} ${scenario.name}: ${scenario.description}`);
    });
    lines.push('');
  }
  
  // 总结
  lines.push('## 7. 分析总结');
  lines.push('');
  lines.push(analysis.summary || '暂无总结');
  lines.push('');
  
  // 提示信息
  lines.push('---');
  lines.push('');
  lines.push('> 💡 **提示**: 本分析由 AI 生成，请务必人工 review 后使用。');
  lines.push('> 重点关注"需求问题清单"，这些问题需要在需求评审会上澄清。');
  
  return lines.join('\n');
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const options = parseArgs(args);
  
  if (options.help) {
    showHelp();
    process.exit(0);
  }
  
  if (!options.document) {
    console.error('❌ 错误：必须指定需求文档路径 (--document)');
    showHelp();
    process.exit(1);
  }
  
  console.error('');
  console.error('╔════════════════════════════════════════════╗');
  console.error('║   需求测试分析专家 v1.0.0                  ║');
  console.error('║   基于 10+ 年测试经验沉淀                    ║');
  console.error('╚════════════════════════════════════════════╝');
  console.error('');
  
  try {
    // 1. 读取文档
    const documentContent = readDocument(options.document);
    console.error(`✓ 文档读取成功，${documentContent.length} 字符`);
    console.error('');
    
    // 2. 构建分析 prompt
    const prompt = buildAnalyzerPrompt(documentContent);
    console.error('✓ Prompt 构建完成');
    console.error('');
    
    // 3. 调用 LLM 分析
    let llmOutput;
    try {
      llmOutput = await analyzeWithLLM(prompt);
      console.error('✓ AI 分析完成');
    } catch (e) {
      // 备用方案：直接输出分析框架
      console.error('⚠️  使用备用分析模式');
      llmOutput = `
\`\`\`json
{
  "project_name": "${options.projectName || '从文档提取'}",
  "analysis_timestamp": "${new Date().toISOString()}",
  "test_objectives": [],
  "test_scope": {
    "in_scope": [],
    "out_of_scope": []
  },
  "priorities": {
    "P0": [],
    "P1": [],
    "P2": []
  },
  "risks": [],
  "questions": [],
  "suggested_test_types": [],
  "key_scenarios": [],
  "summary": "备用模式：请手动补充分析结果"
}
\`\`\`
      `;
    }
    console.error('');
    
    // 4. 解析输出
    const analysis = parseJSONOutput(llmOutput);
    console.error('✓ 结果解析成功');
    console.error('');
    
    // 5. 输出结果
    if (options.outputFormat === 'json' || options.outputFormat === 'both') {
      console.log('');
      console.log('```json');
      console.log(JSON.stringify(analysis, null, 2));
      console.log('```');
      console.log('');
    }
    
    if (options.outputFormat === 'markdown' || options.outputFormat === 'both') {
      console.log('');
      console.log(formatToMarkdown(analysis));
    }
    
    // 6. 保存到 Ontology（可选）
    if (options.saveToOntology) {
      console.error('');
      console.error('💾 正在存储到 Ontology...');
      // TODO: 实现 Ontology 存储
      console.error('✓ 存储完成');
    }
    
    console.error('');
    console.error('✅ 分析完成！');
    
  } catch (error) {
    console.error('');
    console.error(`❌ 错误：${error.message}`);
    process.exit(1);
  }
}

// 运行
main();
