import sys
import json
import jieba

# 从标准输入读取 JXA 脚本的输出
raw_json = sys.stdin.read()
raw_tabs = json.loads(raw_json)
alfred_items = []

for tab in raw_tabs["items"]:
    title = tab.get('title', '')
    url = tab.get('url', '')
    
    # 使用 jieba 的搜索模式进行分词
    # 例如："如何实现分词器" -> ['如何', '实现', '分词', '分词器']
    tokenized_title = " ".join(jieba.cut_for_search(title))
    
    # 清理 URL 用于匹配
    match_url = url.replace("https://", "").replace("http://", "").replace("www.", "")
    
    # 构建 match 字段：包含原始标题、分词后标题、清理后的URL
    # 这样既可以搜 "分词器"，也可以搜 "如何实现"，还可以搜 "github"
    match_string = f"{title} {tokenized_title} {match_url}"
    
    alfred_items.append({
        "title": title,
        "subtitle": url,
        "arg": f"{tab.get('windowIndex')},{tab.get('tabIndex')},{url}",
        "match": match_string,
        "quicklookurl": url,
    })

# 输出最终的、符合 Alfred 格式的 JSON
print(json.dumps({"items": alfred_items}))
