#!/usr/bin/env python3
"""
税务政策 URL 验证脚本
requests + verify=False 抓列表 API (绕过SSL封锁)
playwright HEAD 验证每条 URL (绕过 fgk WAF)
文号精确匹配数据库记录并更新 source_url

用法:
  python3 scripts/content/policy_url_verifier.py --dry-run
  python3 scripts/content/policy_url_verifier.py --run
"""

import json, re, sqlite3, sys, time, os
import warnings
warnings.filterwarnings('ignore')

import requests
requests.packages.urllib3.disable_warnings()

from playwright.sync_api import sync_playwright

# ===== 配置 =====
DB_PATH = "/Volumes/外接硬盘/vibe coding/网站/知识库/database/db/tax_knowledge.db"
CACHE_FILE = "/tmp/policy_verifier_index.json"

API_URL = "https://www.chinatax.gov.cn/getFileListByCodeId"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://fgk.chinatax.gov.cn/",
}
CHANNEL_ID = "29a88b67e4b149cfa9fac7919dfb08a5"


def fetch_list_page(page, size=50, retries=3):
    for attempt in range(retries):
        try:
            resp = requests.post(API_URL, data={
                "codeId": "",
                "channelId": CHANNEL_ID,
                "page": page,
                "size": size,
            }, headers=HEADERS, timeout=20, verify=False)
            j = resp.json()
            if j.get("code") == 200:
                results = j["results"]["data"]
                items = results.get("results", [])
                total = results.get("total", 0)
                return items, total
            raise Exception(f"API错误: {j}")
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise


def norm_doc(doc: str) -> str:
    if not doc:
        return ""
    return re.sub(r"[\s\u3000\xa0（）\(\)\[\]【】]", "", doc)


def extract_year_seq(doc: str):
    nums = re.findall(r"\d+", doc)
    if len(nums) >= 2:
        return nums[-2], nums[-1]
    return "", ""


def match_doc(doc_a: str, doc_b: str) -> bool:
    n_a, n_b = norm_doc(doc_a), norm_doc(doc_b)
    y_a, s_a = extract_year_seq(n_a)
    y_b, s_b = extract_year_seq(n_b)
    return bool(y_a and y_b and y_a == y_b and s_a and s_a == s_b)


def fix_url(url: str) -> str:
    if not url:
        return ""
    return url.replace("http://", "https://").replace("www.chinatax.gov.cn", "fgk.chinatax.gov.cn")


def make_browser():
    p = sync_playwright().__enter__()
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport={'width': 1280, 'height': 800}
    )
    page = context.new_page()
    page.set_default_timeout(20000)
    return p, browser, page


def verify_url(page, url, retries=2) -> int:
    for _ in range(retries):
        try:
            r = page.goto(url, wait_until='domcontentloaded', timeout=15000)
            return r.status if r else 0
        except Exception:
            time.sleep(1)
            continue
    return 0


def main():
    dry_run = "--dry-run" in sys.argv
    print(f"模式: {'预演' if dry_run else '执行'}")

    # ==== 1. 抓政策索引 ====
    print("\n▶ 从政策库 API 抓取索引...")
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            policy_index = json.load(f)
        print(f"  加载缓存: {len(policy_index)} 条")
    else:
        items, total = fetch_list_page(1, 50)
        total_pages = (total + 49) // 50
        print(f"  共 {total} 条, {total_pages} 页")

        policy_index = {}
        for page_num in range(1, total_pages + 1):
            if page_num > 1:
                items, _ = fetch_list_page(page_num, 50)

            for item in items:
                url_val = item.get("url", "")
                if not url_val:
                    continue
                doc_num = ""
                title = item.get("titleHtml", "") or item.get("title", "")
                for meta in item.get("domainMetaList", []):
                    for res in meta.get("resultList", []):
                        if res.get("key") == "writtentext":
                            doc_num = res.get("value", "").strip()
                if doc_num:
                    key = norm_doc(doc_num)
                    policy_index[key] = {
                        "url": fix_url(url_val),
                        "doc_num": doc_num,
                        "title": title,
                    }

            if page_num % 20 == 0:
                print(f"  Page {page_num}/{total_pages} ... (已收集 {len(policy_index)} 条)")
            time.sleep(0.1)

        with open(CACHE_FILE, "w") as f:
            json.dump(policy_index, f, ensure_ascii=False, indent=2)
        print(f"  索引已缓存: {len(policy_index)} 条")

    # ==== 2. 读取数据库 ====
    print("\n▶ 读取数据库...")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, policy_name, document_no, source_url, verification_status
        FROM policy_basis
        WHERE verification_status IN ('needs_update', 'source_pending', 'source_found')
          AND document_no IS NOT NULL AND document_no != ''
        ORDER BY id
    """)
    db_policies = cur.fetchall()
    conn.close()
    print(f"  共 {len(db_policies)} 条需要核验")

    # ==== 3. 文号匹配 ====
    print("\n▶ 文号匹配...")
    candidates = []
    for row in db_policies:
        pid, name, doc_no, old_url, status = row
        if not doc_no or len(doc_no.strip()) < 4:
            continue
        matched_entry = None
        for cache_key, entry in policy_index.items():
            if match_doc(doc_no, entry["doc_num"]):
                matched_entry = entry
                break
        if matched_entry:
            candidates.append({
                "id": pid,
                "name": name[:50],
                "doc_no": doc_no,
                "old_url": old_url or "",
                "new_url": matched_entry["url"],
                "cache_title": matched_entry["title"],
            })
        else:
            print(f"  ❌ 未匹配: [{doc_no}] {name[:40]}")

    print(f"\n  匹配成功: {len(candidates)} 条")

    if not candidates:
        print("没有匹配到任何政策")
        return

    # ==== 4. Playwright URL 验证 ====
    print("\n▶ 启动浏览器验证 URL...")
    pw, browser, page = make_browser()
    print("  浏览器已启动，开始验证...")

    verified = []
    failed = []

    for i, c in enumerate(candidates):
        code = verify_url(page, c["new_url"])
        c["http_code"] = code
        if code == 200:
            verified.append(c)
            print(f"  [{i+1}/{len(candidates)}] ✅ {code} | {c['doc_no']} | {c['new_url'][:60]}")
        else:
            failed.append(c)
            print(f"  [{i+1}/{len(candidates)}] ❌ {code} | {c['doc_no']} | {c['new_url'][:60]}")
        time.sleep(0.3)

    browser.close()
    pw.stop()

    # ==== 5. 报告 ====
    print(f"\n{'='*60}")
    print(f"验证结果:")
    print(f"  ✅ 有效可更新: {len(verified)} 条")
    print(f"  ❌ URL无效: {len(failed)} 条")

    if verified:
        print(f"\n--- 可更新条目 (前20) ---")
        for v in verified[:20]:
            print(f"  ID={v['id']} | {v['doc_no']} | {v['cache_title'][:40]}")
            print(f"    旧: {v['old_url'] or '(无)'}")
            print(f"    新: {v['new_url'][:80]}")

    if failed:
        print(f"\n--- URL无效 (需人工处理) ---")
        for f_item in failed[:10]:
            print(f"  ID={f_item['id']} | {f_item['doc_no']} | HTTP {f_item['http_code']}")

    if dry_run:
        print(f"\n[预演模式] 未写入数据库")
        return

    # ==== 6. 执行更新 ====
    if not verified:
        print("没有可更新的条目")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for v in verified:
        note = f"自动验证通过 | 原URL:{v['old_url'] or '无'}"
        cur.execute(
            "UPDATE policy_basis SET source_url=?, verification_status='verified', verification_note=? WHERE id=?",
            (v["new_url"], note, v["id"])
        )
    conn.commit()
    conn.close()
    print(f"\n✅ 已更新 {len(verified)} 条")


if __name__ == "__main__":
    main()
