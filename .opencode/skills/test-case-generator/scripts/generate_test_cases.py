#!/usr/bin/env python3
"""
Test Case Excel Generator
将 JSON 格式的测试用例数据生成为多 Sheet 的 Excel 文件
使用纯 Python 实现，无需 openpyxl 依赖
"""

import json
import argparse
import zipfile
import os
from datetime import datetime
from xml.sax.saxutils import escape


# 列定义
COLUMNS = [
    '用例ID', '测试场景/模块', '用例标题', '前置条件',
    '测试步骤', '预期结果', '优先级', '测试类型',
    '实际结果', '状态', '测试数据', '备注'
]

COLUMN_WIDTHS = [18, 20, 35, 30, 50, 40, 12, 15, 30, 12, 30, 25]


def col_letter(idx):
    """列索引转字母 (1->A, 2->B, ...)"""
    result = ''
    while idx > 0:
        idx, remainder = divmod(idx - 1, 26)
        result = chr(65 + remainder) + result
    return result


def build_shared_strings(all_strings):
    """构建 sharedStrings.xml"""
    unique = list(dict.fromkeys(all_strings))  # 去重保序
    xml = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    xml += f'<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="{len(all_strings)}" uniqueCount="{len(unique)}">'
    for s in unique:
        xml += f'<si><t>{escape(s)}</t></si>'
    xml += '</sst>'
    return xml, {s: i for i, s in enumerate(unique)}


def build_worksheet(sheet_name, test_cases, case_id_counter, string_map):
    """构建单个 worksheet 的 XML"""
    
    # 列宽
    cols = '<cols>'
    for i, w in enumerate(COLUMN_WIDTHS, 1):
        cols += f'<col min="{i}" max="{i}" width="{w}" customWidth="1"/>'
    cols += '</cols>'
    
    # 数据
    rows = []
    
    # 表头行
    header_cells = ''
    for i, col in enumerate(COLUMNS, 1):
        idx = string_map.get(col, 0)
        header_cells += f'<c r="{col_letter(i)}1" t="s" s="1"><v>{idx}</v></c>'
    rows.append(f'<row r="1" spans="1:{len(COLUMNS)}">{header_cells}</row>')
    
    # 数据行
    for row_idx, case in enumerate(test_cases, 2):
        module = case.get('模块', 'COMMON')
        if module not in case_id_counter:
            case_id_counter[module] = 1
        case_id = f"TC-{module}-{case_id_counter[module]:03d}"
        case_id_counter[module] += 1
        
        values = [
            case_id,
            case.get('测试场景', ''),
            case.get('标题', ''),
            case.get('前置条件', ''),
            case.get('测试步骤', ''),
            case.get('预期结果', ''),
            case.get('优先级', 'P2'),
            case.get('测试类型', ''),
            '',
            'Not Run',
            case.get('测试数据', ''),
            case.get('备注', ''),
        ]
        
        cells = ''
        for i, val in enumerate(values, 1):
            if val:
                idx = string_map.get(val)
                if idx is not None:
                    cells += f'<c r="{col_letter(i)}{row_idx}" t="s" s="0"><v>{idx}</v></c>'
                else:
                    # 新增字符串
                    cells += f'<c r="{col_letter(i)}{row_idx}" t="str" s="0"><v>{escape(val)}</v></c>'
        
        rows.append(f'<row r="{row_idx}" spans="1:{len(COLUMNS)}">{cells}</row>')
    
    sheet_data = '<sheetData>' + ''.join(rows) + '</sheetData>'
    
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  {cols}
  {sheet_data}
</worksheet>'''


def build_summary_sheet(stats, string_map):
    """构建 Summary sheet"""
    
    cols = '<cols><col min="1" max="6" width="20" customWidth="1"/></cols>'
    
    # 标题
    title_idx = string_map.get('测试用例统计摘要')
    time_label_idx = string_map.get('生成时间:')
    total_label_idx = string_map.get('测试用例总数:')
    type_label_idx = string_map.get('测试类型')
    total_label_row_idx = string_map.get('总计')
    
    rows = []
    
    # 标题行
    if title_idx is not None:
        rows.append(f'<row r="1"><c r="A1" t="s" s="2"><v>{title_idx}</v></c></row>')
    
    # 生成时间
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rows.append(f'<row r="3"><c r="A3" t="s" s="3"><v>{time_label_idx}</v></c><c r="B3" t="str"><v>{now}</v></c></row>')
    
    # 总数
    total = sum(s['total'] for s in stats.values())
    rows.append(f'<row r="4"><c r="A4" t="s" s="3"><v>{total_label_idx}</v></c><c r="B4" t="str"><v>{total}</v></c></row>')
    
    # 表头
    headers = ['测试类型', 'P0', 'P1', 'P2', 'P3', '合计']
    header_cells = ''
    for i, h in enumerate(headers, 1):
        idx = string_map.get(h, 0)
        header_cells += f'<c r="{col_letter(i)}6" t="s" s="1"><v>{idx}</v></c>'
    rows.append(f'<row r="6" spans="1:6">{header_cells}</row>')
    
    # 数据行
    row = 7
    for sheet_name, s in stats.items():
        cells = f'<c r="A{row}" t="str"><v>{escape(sheet_name)}</v></c>'
        cells += f'<c r="B{row}" t="str"><v>{s["p0"]}</v></c>'
        cells += f'<c r="C{row}" t="str"><v>{s["p1"]}</v></c>'
        cells += f'<c r="D{row}" t="str"><v>{s["p2"]}</v></c>'
        cells += f'<c r="E{row}" t="str"><v>{s["p3"]}</v></c>'
        cells += f'<c r="F{row}" t="str"><v>{s["total"]}</v></c>'
        rows.append(f'<row r="{row}" spans="1:6">{cells}</row>')
        row += 1
    
    # 总计行
    cells = f'<c r="A{row}" t="s" s="3"><v>{total_label_row_idx}</v></c>'
    cells += f'<c r="F{row}" t="str" s="3"><v>{total}</v></c>'
    rows.append(f'<row r="{row}" spans="1:6">{cells}</row>')
    
    sheet_data = '<sheetData>' + ''.join(rows) + '</sheetData>'
    
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  {cols}
  {sheet_data}
</worksheet>'''


def generate_excel(test_cases_json, output_path):
    """主函数：生成 Excel 文件"""
    
    with open(test_cases_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    test_cases = data.get('test_cases', [])
    
    # 按类型分组
    cases_by_type = {
        '功能测试': [],
        '边界测试': [],
        '异常测试': [],
        '用户旅程': [],
        'API测试': [],
    }
    
    type_mapping = {
        '功能': '功能测试', 'boundary': '边界测试', '边界': '边界测试',
        'exception': '异常测试', '异常': '异常测试',
        'user_journey': '用户旅程', '用户旅程': '用户旅程',
        'api': 'API测试', 'API': 'API测试',
    }
    
    for case in test_cases:
        test_type = case.get('测试类型', '功能')
        sheet_name = type_mapping.get(test_type, '功能测试')
        if sheet_name in cases_by_type:
            cases_by_type[sheet_name].append(case)
    
    # 收集所有字符串
    all_strings = list(COLUMNS)
    all_strings.extend([
        '测试用例统计摘要', '生成时间:', '测试用例总数:',
        '测试类型', 'P0', 'P1', 'P2', 'P3', '合计', '总计'
    ])
    for case in test_cases:
        for key in ['测试场景', '标题', '前置条件', '测试步骤', '预期结果', '测试类型', '测试数据', '备注', '模块']:
            val = case.get(key, '')
            if val:
                all_strings.append(val)
    
    shared_xml, string_map = build_shared_strings(all_strings)
    
    # 构建 sheets
    sheets_info = []
    worksheet_xmls = {}
    case_id_counter = {}
    
    # Summary
    stats = {}
    for name, cases in cases_by_type.items():
        if cases:
            stats[name] = {
                'p0': sum(1 for c in cases if c.get('优先级') == 'P0'),
                'p1': sum(1 for c in cases if c.get('优先级') == 'P1'),
                'p2': sum(1 for c in cases if c.get('优先级') == 'P2'),
                'p3': sum(1 for c in cases if c.get('优先级') == 'P3'),
                'total': len(cases),
            }
    
    summary_xml = build_summary_sheet(stats, string_map)
    sheets_info.append(('Summary', summary_xml))
    
    # 各测试类型 sheet
    for sheet_name, cases in cases_by_type.items():
        if cases:
            xml = build_worksheet(sheet_name, cases, case_id_counter, string_map)
            sheets_info.append((sheet_name, xml))
            worksheet_xmls[sheet_name] = xml
    
    # 创建 xlsx
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # [Content_Types].xml
        types_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        types_xml += '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        types_xml += '<Default Extension="xml" ContentType="application/xml"/>'
        types_xml += '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        types_xml += '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
        types_xml += '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
        for i, (name, _) in enumerate(sheets_info, 1):
            types_xml += f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        types_xml += '</Types>'
        zf.writestr('[Content_Types].xml', types_xml)
        
        # _rels/.rels
        zf.writestr('_rels/.rels',
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '</Relationships>')
        
        # xl/workbook.xml
        sheets_xml = '<sheets>'
        for i, (name, _) in enumerate(sheets_info, 1):
            sheets_xml += f'<sheet name="{escape(name)}" sheetId="{i}" r:id="rId{i}"/>'
        sheets_xml += '</sheets>'
        zf.writestr('xl/workbook.xml',
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            f'<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">{sheets_xml}</workbook>')
        
        # xl/_rels/workbook.xml.rels
        rels_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        for i in range(1, len(sheets_info) + 1):
            rels_xml += f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
        rels_xml += f'<Relationship Id="rId{len(sheets_info)+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        rels_xml += f'<Relationship Id="rId{len(sheets_info)+2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>'
        rels_xml += '</Relationships>'
        zf.writestr('xl/_rels/workbook.xml.rels', rels_xml)
        
        # xl/styles.xml
        zf.writestr('xl/styles.xml',
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<fonts count="4">'
            '<font><sz val="11"/><name val="Calibri"/></font>'
            '<font><b/><color rgb="FFFFFFFF"/><sz val="11"/><name val="Microsoft YaHei"/></font>'
            '<font><b/><sz val="14"/><name val="Microsoft YaHei"/></font>'
            '<font><b/><sz val="11"/><name val="Microsoft YaHei"/></font>'
            '</fonts>'
            '<fills count="2">'
            '<fill><patternFill patternType="none"/></fill>'
            '<fill><patternFill patternType="solid"><fgColor rgb="FF4472C4"/></patternFill></fill>'
            '</fills>'
            '<borders count="1">'
            '<border><left/><right/><top/><bottom/><diagonal/></border>'
            '</borders>'
            '<cellStyleXfs count="1">'
            '<xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>'
            '</cellStyleXfs>'
            '<cellXfs count="4">'
            '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>'
            '<xf numFmtId="0" fontId="1" fillId="1" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment wrapText="1" horizontal="center" vertical="center"/></xf>'
            '<xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>'
            '<xf numFmtId="0" fontId="3" fillId="0" borderId="0" xfId="0" applyFont="1" applyAlignment="1"><alignment vertical="center"/></xf>'
            '</cellXfs>'
            '</styleSheet>')
        
        # sharedStrings.xml
        zf.writestr('xl/sharedStrings.xml', shared_xml)
        
        # worksheets
        for i, (_, xml) in enumerate(sheets_info, 1):
            zf.writestr(f'xl/worksheets/sheet{i}.xml', xml)
    
    # 统计输出
    total = sum(len(cases) for cases in cases_by_type.values())
    print(f"Excel 文件已生成: {output_path}")
    print(f"共生成 {total} 条测试用例")
    for name, cases in cases_by_type.items():
        if cases:
            print(f"  - {name}: {len(cases)} 条")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='生成测试用例 Excel 文件')
    parser.add_argument('--test-cases', required=True, help='测试用例 JSON 文件路径')
    parser.add_argument('--output', required=True, help='输出 Excel 文件路径')
    
    args = parser.parse_args()
    generate_excel(args.test_cases, args.output)
