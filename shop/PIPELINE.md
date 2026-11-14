# NOIRXU 自動賺錢流程（runbook）

```
IG 貼文（每週 3 則，Metricool 草稿）
   │  每則最後一張／文案：「主頁連結」
   ▼
銷售頁 https://noirxu-shop.vercel.app
   │  免費試算 → 免費速查表（換 Email）→ 複利帳本 NT$290
   ▼
收款平台（Portaly 或 Gumroad）：付款、自動寄檔、名單
```

## 各部分在哪

| 部分 | 位置 |
|---|---|
| 付費商品 | `NOIRXU_複利帳本.xlsx`（不放公開 repo；上傳到收款平台） |
| 免費速查表 | `shop/lead_magnet.py` 產生 PDF（2 頁） |
| 銷售頁原始碼 | `shop/site/index.html`，部署在 Vercel 專案 `noirxu-shop`（team `team_sy9Jx2kMkne8QI7xkDDt00Wa`） |
| 銷售頁圖片 | `shop/img/`（raw.githubusercontent.com 直接引用） |
| 題材庫 | `shop/topics.md` |
| 每週貼文腳本 | `posts/weekNN_shop.py`，輸出到 `v2/shop/weekNN/` |
| 排程 | Metricool brand `7435546`（yoru_stocklab），一律 `draft: true`，人工確認後才發 |

## 每週自動流程（排程任務每週日晚上執行）

1. 從 `shop/topics.md` 取 3 個未用題材（2 輪播＋1 單圖）。
2. 參考 `posts/week2_feed.py` 與 `posts/shop_launch.py` 寫 `posts/weekNN_shop.py`，用 `style/feed_lib.py`（v2 黑白灰）。
3. 數字全部程式計算，並在腳本內 `assert` 一次獨立驗算；基準 974.5 萬必須對上。
4. 產圖、逐張看過（版面不重疊、字不出界），push 到 `main`。
5. 在 Metricool 建草稿：週一／週三／週五 10:00（Asia/Taipei），圖片用 raw GitHub 網址。
6. 更新 `topics.md`，回報：本週 3 則草稿連結、上週各貼文成效、銷售頁是否已接上結帳連結。

## 你每週要做的（約 10–20 分鐘）

- 打開 Metricool 草稿，抽查一個數字（用銷售頁的試算器），沒問題就把草稿改成排程。
- 看一眼收款平台的訂單與名單。

## 結帳連結接上的方法

把 `shop/site/index.html` 最下面的 `CONFIG.checkout`（付費）和 `CONFIG.free`（免費速查表）填上，重新部署 `noirxu-shop`。或直接把兩個連結傳給 Claude，請它更新。
