"""
Markdown to HTML converter with GitHub-style formatting
將 Markdown 文件轉換為 GitHub 風格的 HTML
然後可以用瀏覽器列印為 PDF
"""
import os
import sys
import subprocess
import re

def install_markdown():
    """安裝 markdown 套件"""
    try:
        import markdown
        return markdown
    except ImportError:
        print("正在安裝 markdown 套件...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'markdown'])
        import markdown
        return markdown

def convert_md_to_html(md_file, output_html=None):
    """將 Markdown 轉換為 GitHub 風格的 HTML"""
    markdown = install_markdown()
    
    # 讀取 Markdown 文件
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 轉換 Markdown 為 HTML
    md = markdown.Markdown(extensions=[
        'extra',
        'codehilite',
        'toc',
        'tables',
        'fenced_code',
        'nl2br',
        'sane_lists'
    ])
    html_content = md.convert(md_content)
    
    # 處理圖片路徑（相對路徑）
    md_dir = os.path.dirname(os.path.abspath(md_file))
    
    # GitHub 風格的完整 HTML
    github_css = """
    <style>
        @media print {
            @page {
                margin: 2cm;
                size: A4;
            }
            
            body {
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
            
            img {
                page-break-inside: avoid;
                max-width: 100% !important;
                height: auto !important;
            }
            
            h1, h2, h3, h4, h5, h6 {
                page-break-after: avoid;
            }
            
            pre, blockquote {
                page-break-inside: avoid;
            }
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", 
                         Helvetica, Arial, sans-serif, "Microsoft JhengHei", "微軟正黑體";
            font-size: 16px;
            line-height: 1.6;
            color: #24292e;
            background-color: #ffffff;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px;
        }
        
        h1 {
            font-size: 2em;
            font-weight: 600;
            border-bottom: 2px solid #eaecef;
            padding-bottom: 0.3em;
            margin-top: 24px;
            margin-bottom: 16px;
        }
        
        h2 {
            font-size: 1.5em;
            font-weight: 600;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
            margin-top: 24px;
            margin-bottom: 16px;
        }
        
        h3 {
            font-size: 1.25em;
            font-weight: 600;
            margin-top: 24px;
            margin-bottom: 16px;
        }
        
        h4 {
            font-size: 1em;
            font-weight: 600;
            margin-top: 16px;
            margin-bottom: 16px;
        }
        
        p {
            margin-top: 0;
            margin-bottom: 10px;
        }
        
        a {
            color: #0366d6;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        code {
            background-color: rgba(27,31,35,0.05);
            border-radius: 3px;
            font-size: 85%;
            margin: 0;
            padding: 0.2em 0.4em;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
        }
        
        pre {
            background-color: #f6f8fa;
            border-radius: 6px;
            padding: 16px;
            overflow: auto;
            font-size: 85%;
            line-height: 1.45;
            margin-bottom: 16px;
        }
        
        pre code {
            background-color: transparent;
            border: 0;
            display: inline;
            line-height: inherit;
            margin: 0;
            overflow: visible;
            padding: 0;
            word-wrap: normal;
        }
        
        table {
            border-collapse: collapse;
            border-spacing: 0;
            width: 100%;
            margin-bottom: 16px;
            display: table;
            overflow: auto;
        }
        
        table th {
            font-weight: 600;
            background-color: #f6f8fa;
            padding: 6px 13px;
            border: 1px solid #d0d7de;
        }
        
        table td {
            padding: 6px 13px;
            border: 1px solid #d0d7de;
        }
        
        table tr {
            background-color: #ffffff;
            border-top: 1px solid #d0d7de;
        }
        
        table tr:nth-child(2n) {
            background-color: #f6f8fa;
        }
        
        blockquote {
            padding: 0 1em;
            color: #57606a;
            border-left: 0.25em solid #d0d7de;
            margin: 0 0 16px 0;
        }
        
        ul, ol {
            padding-left: 2em;
            margin-top: 0;
            margin-bottom: 16px;
        }
        
        li + li {
            margin-top: 0.25em;
        }
        
        img {
            max-width: 100%;
            box-sizing: content-box;
            background-color: #ffffff;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            padding: 8px;
            margin: 10px 0;
            display: block;
        }
        
        hr {
            height: 2px;
            padding: 0;
            margin: 24px 0;
            background-color: #e1e4e8;
            border: 0;
        }
        
        strong {
            font-weight: 600;
        }
        
        em {
            font-style: italic;
        }
        
        .toc {
            background-color: #f6f8fa;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            padding: 16px;
            margin-bottom: 24px;
        }
    </style>
    """
    
    # 取得文件標題（從檔名）
    file_title = os.path.basename(md_file).rsplit('.', 1)[0]
    
    # 完整的 HTML 文檔
    full_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{file_title}</title>
    {github_css}
</head>
<body>
    {html_content}
</body>
</html>
"""
    
    # 設定輸出檔案名
    if output_html is None:
        output_html = md_file.rsplit('.', 1)[0] + '.html'
    
    # 寫入 HTML 文件
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✓ HTML 已生成: {output_html}")
    return output_html

if __name__ == '__main__':
    # 支持命令行參數
    if len(sys.argv) > 1:
        md_file = sys.argv[1]
    else:
        md_file = 'InfinityMind_AI_使用手冊.md'
    
    if not os.path.exists(md_file):
        print(f"錯誤：找不到文件 {md_file}")
        sys.exit(1)
    
    try:
        output_file = convert_md_to_html(md_file)
        abs_path = os.path.abspath(output_file)
        
        print(f"\n✓ 成功！HTML 文件已儲存至：{abs_path}")
        print("\n=== 如何轉換成 PDF ===")
        print("1. 在瀏覽器中開啟生成的 HTML 文件")
        print("2. 按 Ctrl+P 或選擇 檔案 > 列印")
        print("3. 選擇「另存新檔為 PDF」或「Microsoft Print to PDF」")
        print("4. 設定選項：")
        print("   - 紙張大小：A4")
        print("   - 邊界：預設或自訂 (建議 2cm)")
        print("   - 背景圖形：開啟 (保留顏色)")
        print("5. 儲存 PDF 文件")
        print("\n或者，您可以安裝 Pandoc 來自動轉換：")
        print("  下載：https://pandoc.org/installing.html")
        
    except Exception as e:
        print(f"轉換失敗：{str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
