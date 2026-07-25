# Candidate research questions

All scores were assigned before the selected pilot result was calculated. The full machine-readable assessment is `docs/candidates.json`.

| Rank | Candidate | Score | Feasibility | Principal failure mode |
|---:|---|---:|---|---|
| 1 | Root README install-to-first-use preflight | 89 | 可完成。 | 標註定義過度主觀或外部文件使根 README 指標失去意義。 |
| 2 | Environmental unit metadata completeness | 86 | 部分可完成；資料取得偏差較大。 | 資料入口阻擋下載、授權或 schema 過度異質。 |
| 3 | Notebook output freshness | 84 | 可完成。 | 代理指標不等於結果真的錯誤。 |
| 4 | Figure lineage gap | 83 | 可完成但人工標註重。 | 檔名搜尋可能漏掉動態產生與手工圖。 |
| 5 | Offline lesson pack external dependency | 82 | 可完成但瀏覽器自動化環境有限。 | 合法下載與內容包取得可能受限。 |
| 6 | Public dataset freshness contract | 81 | pilot 可完成，真正 drift 需時間。 | 沒有歷史 snapshot 時無法判定 drift。 |
| 7 | Release documentation artifact mismatch | 80 | 可完成。 | API rate limits 與不同封裝生態。 |
| 8 | GitHub Actions permission overbreadth | 79 | 可完成。 | 成熟工具可能已足夠或語意推斷不可靠。 |
| 9 | CITATION.cff package version drift | 78 | 已被現有 cff-drift-guard pilot探索，不重複。 | 可比較樣本太少。 |
| 10 | Research citation link rot | 77 | 可完成但即時網路狀況偏差大。 | 網路瞬時錯誤與反爬蟲。 |
| 11 | SBOM generator disagreement | 76 | 目前部分不可完成。 | 無 Docker/網路下載工具，當前環境受限。 |
| 12 | FAIR repository metadata quickcheck | 74 | 可完成。 | 重要性可能只是 compliance proxy。 |
| 13 | Open-data license metadata mesh | 73 | 可完成。 | 法務語意不可完全自動化。 |
| 14 | Public dataset downloadability | 72 | 瀏覽器能力部分可用。 | 反機器人機制可能誤判。 |
| 15 | Sensor calibration metadata minimum | 71 | 可完成但資料源選擇偏差。 | 跨感測器標準差異大。 |
| 16 | Example secret residue | 70 | 可完成但不優先。 | 問題可能已被成熟工具解決。 |
| 17 | Chart accessibility preflight | 69 | 部分可完成。 | 主觀標註與網站動態性。 |
| 18 | Research PDF accessibility preflight | 68 | 目前部分可完成。 | 缺完整 PDF/UA 工具與人工輔具測試。 |
| 19 | Agent completion evidence ledger | 67 | 目前被外部驗證阻擋。 | 資料不足與選樣偏差。 |
| 20 | Agent Skill performance benchmark | 66 | 當前無付費 API，不適合。 | 缺付費 API 與版本穩定性。 |
| 21 | RO-Crate minimal validator gap | 65 | 可完成但價值較低。 | 研究缺口可能已被現有工具覆蓋。 |

## Full assessments

### 1. Root README install-to-first-use preflight — 89/100

1. **Specific question:** 在近期經同儕審查的研究軟體中，根 README 是否提供安全、可複製的安裝到首次使用路徑，保守靜態規則能否辨識高信心失敗？
2. **Public-interest importance:** 首次接觸軟體時的文件失敗會浪費研究時間並阻礙重現。
3. **Affected parties:** 研究者、學生、RSE、維護者與審稿人。
4. **Existing solutions:** README 範本、Runme、pytest-codeblocks、文件網站與 CI。
5. **Specific insufficiency:** 現有工具多執行已標記區塊，較少區分缺少首次使用、外部文件委派與可靜態證明的壞路徑。
6. **Available data:** JOSS issue 122 的公開論文與 GitHub 根 README。
7. **Executable experiment:** 人工標註 20 篇固定樣本；比較樸素規則與保守 preflight；檢查四類硬錯誤。
8. **Quantitative metrics:** 嚴格/寬鬆自足率、precision、recall、FP/FN、Wilson CI、執行時間。
9. **Estimated time:** 1–2 天 pilot。
10. **Technical difficulty:** 中。
11. **Ethics and safety:** 低；只保存公開 metadata、短命令片段與 hashes。
12. **Largest failure reason:** 標註定義過度主觀或外部文件使根 README 指標失去意義。
13. **Reusable output if successful:** CLI、標註集、研究 protocol、CI。
14. **Knowledge if unsuccessful:** 即使 H1 失敗，也能量化外部文件委派並留下負面基準。
15. **Can be completed here:** 可完成。
**Score breakdown:** public_importance=14, gap_reality=13, testability=15, feasibility=15, reproducibility=10, reuse=9, novelty=7, growth=3, maintenance=3.

### 2. Environmental unit metadata completeness — 86/100

1. **Specific question:** 公開土壤、水質與空氣 CSV 中，可機械判定的欄位單位 metadata 缺漏率是否足以影響跨資料集比較？
2. **Public-interest importance:** 單位缺失可能導致錯誤比較、錯誤模型與政策判讀。
3. **Affected parties:** 環境科學家、政府資料使用者、學生與公民科技團隊。
4. **Existing solutions:** CF conventions、QUDT、UCUM、資料入口 schema。
5. **Specific insufficiency:** 跨入口資料常無統一欄位—單位連結，且現有驗證工具依賴完善 schema。
6. **Available data:** 政府公開資料 API 與下載檔。
7. **Executable experiment:** 抽樣多入口資料，對欄名、資料字典與值域建立單位可判定標註。
8. **Quantitative metrics:** 必要欄位缺漏率、單位歧義率、跨來源一致率。
9. **Estimated time:** 3–5 天。
10. **Technical difficulty:** 中高。
11. **Ethics and safety:** 低；避免個資欄位。
12. **Largest failure reason:** 資料入口阻擋下載、授權或 schema 過度異質。
13. **Reusable output if successful:** 單位 audit dataset、schema 與 CLI。
14. **Knowledge if unsuccessful:** 可記錄無法比較的具體原因。
15. **Can be completed here:** 部分可完成；資料取得偏差較大。
**Score breakdown:** public_importance=15, gap_reality=14, testability=14, feasibility=13, reproducibility=9, reuse=9, novelty=7, growth=3, maintenance=2.

### 3. Notebook output freshness — 84/100

1. **Specific question:** 已提交 Jupyter notebook 的輸出是否與最後執行順序、原始碼與 metadata 一致，能否以低成本 preflight 找出 stale output？
2. **Public-interest importance:** 過期輸出可讓讀者看到非目前程式碼產生的結果。
3. **Affected parties:** 研究者、審稿人、教學者與資料科學團隊。
4. **Existing solutions:** nbval、nbclient、Jupyter execution_count、pre-commit hooks。
5. **Specific insufficiency:** 完整重跑可能昂貴；現有工具較少提供不執行的保守 freshness 指標。
6. **Available data:** 公開研究 repository 的 ipynb。
7. **Executable experiment:** 固定樣本，人工標註 execution count、輸出存在性與 cell hash 漂移代理。
8. **Quantitative metrics:** stale proxy rate、precision/recall、處理時間。
9. **Estimated time:** 2–3 天。
10. **Technical difficulty:** 中。
11. **Ethics and safety:** 低。
12. **Largest failure reason:** 代理指標不等於結果真的錯誤。
13. **Reusable output if successful:** CLI、benchmark、pre-commit hook。
14. **Knowledge if unsuccessful:** 可證明哪些代理無效。
15. **Can be completed here:** 可完成。
**Score breakdown:** public_importance=13, gap_reality=13, testability=15, feasibility=14, reproducibility=10, reuse=9, novelty=7, growth=2, maintenance=1.

### 4. Figure lineage gap — 83/100

1. **Specific question:** 研究 repository 中的最終圖檔能否追溯到產生它的 script/notebook 與輸入資料？
2. **Public-interest importance:** 無 lineage 會阻礙修正、審查與重新產圖。
3. **Affected parties:** 作者、審稿人、資料管理員。
4. **Existing solutions:** Make/Snakemake、RO-Crate、manifests、notebook workflows。
5. **Specific insufficiency:** 小型專案常缺少圖檔—程式—資料對應；現有標準採用成本較高。
6. **Available data:** JOSS 或 replication repositories。
7. **Executable experiment:** 抽樣圖檔，搜尋同名輸出、程式引用與 workflow dependency。
8. **Quantitative metrics:** 可追溯率、歧義率、人工步驟。
9. **Estimated time:** 3–4 天。
10. **Technical difficulty:** 中高。
11. **Ethics and safety:** 低。
12. **Largest failure reason:** 檔名搜尋可能漏掉動態產生與手工圖。
13. **Reusable output if successful:** lineage manifest schema、scanner、dataset。
14. **Knowledge if unsuccessful:** 量化靜態追溯的上限。
15. **Can be completed here:** 可完成但人工標註重。
**Score breakdown:** public_importance=14, gap_reality=14, testability=13, feasibility=13, reproducibility=9, reuse=9, novelty=8, growth=2, maintenance=1.

### 5. Offline lesson pack external dependency — 82/100

1. **Specific question:** 宣稱可離線使用的開放教材包，在斷網環境是否仍依賴外部字型、腳本、影片或 API？
2. **Public-interest importance:** 低頻寬與災害環境會因隱性外部依賴失去教育可及性。
3. **Affected parties:** 偏鄉學生、教師、圖書館與人道教育團隊。
4. **Existing solutions:** PWA offline audits、service workers、web archiving。
5. **Specific insufficiency:** 一般 Lighthouse 測試不等於完整教材流程自給自足。
6. **Available data:** 公開 OER HTML/ZIP/PWA。
7. **Executable experiment:** 下載教材、封鎖網路、記錄失敗請求與缺失資源。
8. **Quantitative metrics:** 離線成功率、外部請求數、關鍵資源缺失率。
9. **Estimated time:** 2–4 天。
10. **Technical difficulty:** 中。
11. **Ethics and safety:** 低。
12. **Largest failure reason:** 合法下載與內容包取得可能受限。
13. **Reusable output if successful:** 離線 validator、fixture、protocol。
14. **Knowledge if unsuccessful:** 可產生依賴分類與負面案例。
15. **Can be completed here:** 可完成但瀏覽器自動化環境有限。
**Score breakdown:** public_importance=14, gap_reality=12, testability=14, feasibility=14, reproducibility=9, reuse=9, novelty=7, growth=2, maintenance=1.

### 6. Public dataset freshness contract — 81/100

1. **Specific question:** 標示定期更新的政府資料集，其實際更新間隔與 schema 是否違反可自動建立的 freshness contract？
2. **Public-interest importance:** 中斷或無預警 drift 會破壞公共監測與下游分析。
3. **Affected parties:** 公民科技、研究者、新聞工作者與政府團隊。
4. **Existing solutions:** 資料入口 metadata、ETag、schema registries、monitoring。
5. **Specific insufficiency:** 更新頻率常是文字承諾，缺乏機器可檢驗合約。
6. **Available data:** 政府 open data APIs。
7. **Executable experiment:** 建立 10–20 資料集 snapshot，重播歷史 metadata 或立即基線。
8. **Quantitative metrics:** 延遲天數、schema drift、下載成功率。
9. **Estimated time:** 需要歷史資料時 1–2 週；單次基線 2 天。
10. **Technical difficulty:** 中。
11. **Ethics and safety:** 低。
12. **Largest failure reason:** 沒有歷史 snapshot 時無法判定 drift。
13. **Reusable output if successful:** contract schema、GitHub Action、snapshot dataset。
14. **Knowledge if unsuccessful:** 建立未來可累積基線。
15. **Can be completed here:** pilot 可完成，真正 drift 需時間。
**Score breakdown:** public_importance=15, gap_reality=13, testability=14, feasibility=13, reproducibility=9, reuse=9, novelty=6, growth=1, maintenance=1.

### 7. Release documentation artifact mismatch — 80/100

1. **Specific question:** 開源研究軟體 release 的文件版本、tag、wheel/sdist metadata 與下載 artifact 是否一致？
2. **Public-interest importance:** 不一致會造成錯誤引用、安裝與重現。
3. **Affected parties:** 研究軟體使用者、封裝維護者與 archivists。
4. **Existing solutions:** twine check、package metadata、release CI、reproducible builds。
5. **Specific insufficiency:** 工具各自驗證單一 artifact，較少跨 release 頁面、tag 與 docs 對照。
6. **Available data:** GitHub releases、PyPI、package manifests。
7. **Executable experiment:** 固定樣本抓取 release metadata，建立一致性矩陣。
8. **Quantitative metrics:** 不一致率、可判定率、FP/FN。
9. **Estimated time:** 2–3 天。
10. **Technical difficulty:** 中。
11. **Ethics and safety:** 低。
12. **Largest failure reason:** API rate limits 與不同封裝生態。
13. **Reusable output if successful:** release auditor、dataset。
14. **Knowledge if unsuccessful:** 可證明哪些欄位不可比較。
15. **Can be completed here:** 可完成。
**Score breakdown:** public_importance=13, gap_reality=13, testability=14, feasibility=14, reproducibility=9, reuse=9, novelty=7, growth=1, maintenance=0.

### 8. GitHub Actions permission overbreadth — 79/100

1. **Specific question:** 研究軟體 CI workflow 的 permissions 是否超過 job 實際需要，保守規則能否找出明顯 overbreadth？
2. **Public-interest importance:** 過寬 token 權限增加供應鏈風險。
3. **Affected parties:** 開源維護者、依賴使用者與資安團隊。
4. **Existing solutions:** GitHub permission guidance、CodeQL、actionlint、security scanners。
5. **Specific insufficiency:** 靜態推斷實際需求困難，容易誤報；研究軟體族群實證有限。
6. **Available data:** 公開 workflow YAML。
7. **Executable experiment:** 解析 permissions 與 action usage，人工審查高風險 cases。
8. **Quantitative metrics:** 高信心發現數、precision、不可判定率。
9. **Estimated time:** 2–3 天。
10. **Technical difficulty:** 中高。
11. **Ethics and safety:** 中；不得執行不可信 workflow。
12. **Largest failure reason:** 成熟工具可能已足夠或語意推斷不可靠。
13. **Reusable output if successful:** linter rules、benchmark。
14. **Knowledge if unsuccessful:** 記錄不可安全推斷的邊界。
15. **Can be completed here:** 可完成。
**Score breakdown:** public_importance=14, gap_reality=11, testability=14, feasibility=13, reproducibility=9, reuse=9, novelty=7, growth=1, maintenance=1.

### 9. CITATION.cff package version drift — 78/100

1. **Specific question:** CITATION.cff 版本與 package manifest 的靜態版本是否漂移？
2. **Public-interest importance:** 錯誤版本會污染引用與 archive metadata。
3. **Affected parties:** 研究軟體作者、使用者與資料庫。
4. **Existing solutions:** cffconvert、CFF schema、package validators。
5. **Specific insufficiency:** schema validation不檢查跨檔案一致性。
6. **Available data:** JOSS repositories。
7. **Executable experiment:** 比對 same-scope static versions，排除動態/monorepo歧義。
8. **Quantitative metrics:** eligible率、drift率、誤判率。
9. **Estimated time:** 已完成先前 pilot。
10. **Technical difficulty:** 中。
11. **Ethics and safety:** 低。
12. **Largest failure reason:** 可比較樣本太少。
13. **Reusable output if successful:** CLI、dataset、protocol。
14. **Knowledge if unsuccessful:** 負面可行性與 eligibility 證據。
15. **Can be completed here:** 已被現有 cff-drift-guard pilot探索，不重複。
**Score breakdown:** public_importance=12, gap_reality=12, testability=14, feasibility=14, reproducibility=10, reuse=8, novelty=6, growth=1, maintenance=1.

### 10. Research citation link rot — 77/100

1. **Specific question:** 研究軟體 README 與論文中的資料、文件及 archive 連結有多少已失效或轉向非等價資源？
2. **Public-interest importance:** 失效引用造成知識與證據鏈斷裂。
3. **Affected parties:** 研究者、學生、圖書館與 archivists。
4. **Existing solutions:** link checkers、DOI、web archives。
5. **Specific insufficiency:** HTTP 200 不代表內容等價，動態網站也造成誤判。
6. **Available data:** 公開 READMEs、papers、DOIs。
7. **Executable experiment:** 抽樣 URL，分類解析、redirect、內容型別與 archive 可用性。
8. **Quantitative metrics:** 失效率、redirect率、誤判率。
9. **Estimated time:** 2–4 天。
10. **Technical difficulty:** 中。
11. **Ethics and safety:** 低；尊重 robots 與 rate limits。
12. **Largest failure reason:** 網路瞬時錯誤與反爬蟲。
13. **Reusable output if successful:** link audit dataset、checker。
14. **Knowledge if unsuccessful:** 建立時間戳記 snapshot。
15. **Can be completed here:** 可完成但即時網路狀況偏差大。
**Score breakdown:** public_importance=13, gap_reality=11, testability=13, feasibility=14, reproducibility=9, reuse=8, novelty=6, growth=2, maintenance=1.

### 11. SBOM generator disagreement — 76/100

1. **Specific question:** 對同一小型專案，不同免費 SBOM 工具產生的元件集合與版本差異有多大？
2. **Public-interest importance:** 缺漏影響漏洞管理與供應鏈透明度。
3. **Affected parties:** 維護者、資安團隊與採購者。
4. **Existing solutions:** Syft、CycloneDX、SPDX tooling。
5. **Specific insufficiency:** 工具解析策略不同，使用者難判讀差異。
6. **Available data:** 合成與公開小型多語言 fixtures。
7. **Executable experiment:** 用固定容器跑多工具，建立 gold components。
8. **Quantitative metrics:** precision/recall、集合 Jaccard、執行時間。
9. **Estimated time:** 3–5 天。
10. **Technical difficulty:** 高。
11. **Ethics and safety:** 低。
12. **Largest failure reason:** 無 Docker/網路下載工具，當前環境受限。
13. **Reusable output if successful:** benchmark、fixtures、comparison schema。
14. **Knowledge if unsuccessful:** 可形成阻礙報告。
15. **Can be completed here:** 目前部分不可完成。
**Score breakdown:** public_importance=13, gap_reality=12, testability=14, feasibility=11, reproducibility=9, reuse=8, novelty=7, growth=1, maintenance=1.

### 12. FAIR repository metadata quickcheck — 74/100

1. **Specific question:** 小型研究軟體 repository 的最低 FAIR/metadata 元件能否用低誤報 quickcheck 檢查？
2. **Public-interest importance:** 缺 metadata 降低發現、引用與重用。
3. **Affected parties:** 研究軟體作者與資料管理員。
4. **Existing solutions:** FAIR4RS、CodeMeta、CFF、RO-Crate。
5. **Specific insufficiency:** 完整標準複雜；簡化檢查易淪為 checklist。
6. **Available data:** 公開 repositories。
7. **Executable experiment:** 定義最小 profile，人工標註後比較規則。
8. **Quantitative metrics:** coverage、precision、完成時間。
9. **Estimated time:** 2–3 天。
10. **Technical difficulty:** 中。
11. **Ethics and safety:** 低。
12. **Largest failure reason:** 重要性可能只是 compliance proxy。
13. **Reusable output if successful:** profile、CLI、dataset。
14. **Knowledge if unsuccessful:** 指出哪些欄位無實際價值。
15. **Can be completed here:** 可完成。
**Score breakdown:** public_importance=12, gap_reality=10, testability=13, feasibility=14, reproducibility=9, reuse=9, novelty=5, growth=1, maintenance=1.

### 13. Open-data license metadata mesh — 73/100

1. **Specific question:** 同一政府資料集頁面、API metadata 與下載檔內的 license 宣告是否一致？
2. **Public-interest importance:** license 歧義阻礙合法重用。
3. **Affected parties:** 公民科技、研究者、企業與政府。
4. **Existing solutions:** DCAT、data portals、SPDX。
5. **Specific insufficiency:** license 分散在多層且文字不一致。
6. **Available data:** 政府資料入口。
7. **Executable experiment:** 抽樣資料集，擷取三層 license 並標準化。
8. **Quantitative metrics:** 缺失率、一致率、不可判定率。
9. **Estimated time:** 2–4 天。
10. **Technical difficulty:** 中。
11. **Ethics and safety:** 低。
12. **Largest failure reason:** 法務語意不可完全自動化。
13. **Reusable output if successful:** license mesh schema、dataset。
14. **Knowledge if unsuccessful:** 量化不可判定情況。
15. **Can be completed here:** 可完成。
**Score breakdown:** public_importance=13, gap_reality=11, testability=12, feasibility=13, reproducibility=9, reuse=8, novelty=5, growth=1, maintenance=1.

### 14. Public dataset downloadability — 72/100

1. **Specific question:** 標示為公開下載的資料資源中，有多少實際需要登入、JavaScript、短效 token 或人工操作？
2. **Public-interest importance:** 名義開放但不可機器取得會降低透明度與重現。
3. **Affected parties:** 研究者、記者、公民科技。
4. **Existing solutions:** link checkers、portal APIs。
5. **Specific insufficiency:** HTTP 與瀏覽器行為差距，且授權常不清楚。
6. **Available data:** open data catalogs。
7. **Executable experiment:** 抽樣資源，以匿名 HTTP 與瀏覽器雙路徑測試。
8. **Quantitative metrics:** 直接下載率、阻擋類型、步驟數。
9. **Estimated time:** 2–3 天。
10. **Technical difficulty:** 中。
11. **Ethics and safety:** 低。
12. **Largest failure reason:** 反機器人機制可能誤判。
13. **Reusable output if successful:** downloadability benchmark。
14. **Knowledge if unsuccessful:** 分類實務障礙。
15. **Can be completed here:** 瀏覽器能力部分可用。
**Score breakdown:** public_importance=14, gap_reality=9, testability=13, feasibility=14, reproducibility=8, reuse=8, novelty=4, growth=1, maintenance=1.

### 15. Sensor calibration metadata minimum — 71/100

1. **Specific question:** 公開低成本環境感測資料是否提供足以解讀數值的校正、感測器型號與維護 metadata？
2. **Public-interest importance:** 缺校正資訊會讓數值比較失真。
3. **Affected parties:** 環境研究者、社區監測與政策分析者。
4. **Existing solutions:** SensorThings API、OGC metadata、校正 protocols。
5. **Specific insufficiency:** 欄位存在不代表可追溯校正。
6. **Available data:** 公開 sensor networks。
7. **Executable experiment:** 抽樣資料源，依最低 metadata profile 評分。
8. **Quantitative metrics:** 完整率、追溯率、不可判定率。
9. **Estimated time:** 3–5 天。
10. **Technical difficulty:** 中高。
11. **Ethics and safety:** 低。
12. **Largest failure reason:** 跨感測器標準差異大。
13. **Reusable output if successful:** profile、audit dataset。
14. **Knowledge if unsuccessful:** 形成缺口 taxonomy。
15. **Can be completed here:** 可完成但資料源選擇偏差。
**Score breakdown:** public_importance=14, gap_reality=10, testability=12, feasibility=11, reproducibility=8, reuse=8, novelty=5, growth=1, maintenance=2.

### 16. Example secret residue — 70/100

1. **Specific question:** 公開研究軟體的 examples/docs 是否含看似真實的 token、password 或 private endpoint？
2. **Public-interest importance:** 範例憑證可能造成安全事件。
3. **Affected parties:** 維護者、機構與下游使用者。
4. **Existing solutions:** gitleaks、trufflehog、secret scanners。
5. **Specific insufficiency:** 成熟工具已涵蓋多數模式，研究創新有限。
6. **Available data:** 公開 repositories。
7. **Executable experiment:** 對 sample repos 跑規則並人工確認。
8. **Quantitative metrics:** 真陽性數、precision、敏感內容處理。
9. **Estimated time:** 1–2 天。
10. **Technical difficulty:** 低中。
11. **Ethics and safety:** 中；不可公開有效秘密。
12. **Largest failure reason:** 問題可能已被成熟工具解決。
13. **Reusable output if successful:** 安全披露 protocol、benchmark。
14. **Knowledge if unsuccessful:** 負面證據仍可證明工具足夠。
15. **Can be completed here:** 可完成但不優先。
**Score breakdown:** public_importance=14, gap_reality=8, testability=13, feasibility=14, reproducibility=8, reuse=8, novelty=4, growth=1, maintenance=0.

### 17. Chart accessibility preflight — 69/100

1. **Specific question:** 研究 repository 的 HTML/SVG 圖表是否提供文字替代、鍵盤操作與非色彩編碼？
2. **Public-interest importance:** 視覺障礙者可能無法取得研究結果。
3. **Affected parties:** 身心障礙研究者、學生與公眾。
4. **Existing solutions:** WCAG、axe、chart accessibility guidelines。
5. **Specific insufficiency:** 自動檢查難判斷文字替代是否具資訊等價。
6. **Available data:** 公開 docs sites 與 SVG/HTML。
7. **Executable experiment:** 抽樣圖表，跑 axe 並人工標註關鍵等價性。
8. **Quantitative metrics:** 缺失率、precision、人工時間。
9. **Estimated time:** 3–5 天。
10. **Technical difficulty:** 中高。
11. **Ethics and safety:** 低。
12. **Largest failure reason:** 主觀標註與網站動態性。
13. **Reusable output if successful:** preflight、audit protocol。
14. **Knowledge if unsuccessful:** 量化自動化上限。
15. **Can be completed here:** 部分可完成。
**Score breakdown:** public_importance=13, gap_reality=10, testability=12, feasibility=13, reproducibility=8, reuse=8, novelty=3, growth=1, maintenance=1.

### 18. Research PDF accessibility preflight — 68/100

1. **Specific question:** 公開研究報告 PDF 的可抽取文字、標題結構、替代文字與閱讀順序可否由低成本 preflight 找出高風險文件？
2. **Public-interest importance:** 不可及 PDF 排除讀者且妨礙文字探勘。
3. **Affected parties:** 視障者、學生、研究者與檔案館。
4. **Existing solutions:** PAC、veraPDF、PDF/UA。
5. **Specific insufficiency:** 完整工具部署重，且自動結果不等於實際閱讀品質。
6. **Available data:** 公開報告 PDF。
7. **Executable experiment:** 抽樣 PDF，以結構與人工頁面檢查建立標註。
8. **Quantitative metrics:** 高風險率、precision、處理時間。
9. **Estimated time:** 3–5 天。
10. **Technical difficulty:** 中高。
11. **Ethics and safety:** 低。
12. **Largest failure reason:** 缺完整 PDF/UA 工具與人工輔具測試。
13. **Reusable output if successful:** preflight、dataset。
14. **Knowledge if unsuccessful:** 負面可行性。
15. **Can be completed here:** 目前部分可完成。
**Score breakdown:** public_importance=13, gap_reality=9, testability=12, feasibility=13, reproducibility=8, reuse=8, novelty=3, growth=1, maintenance=1.

### 19. Agent completion evidence ledger — 67/100

1. **Specific question:** Coding agent 宣稱完成的任務，是否具備可驗證 tests/build/diff/CI 證據？
2. **Public-interest importance:** 無證據完成宣稱會造成錯誤合併與信任損失。
3. **Affected parties:** 開發者、維護者與組織。
4. **Existing solutions:** CI、attestations、agent logs、existing agent-completion-ledger。
5. **Specific insufficiency:** 真實 agent runs 與獨立 ground truth 難取得。
6. **Available data:** 公開 agent PRs 或合成任務。
7. **Executable experiment:** 比較 claim 與 CI/test evidence。
8. **Quantitative metrics:** unsupported claim rate、precision、漏判。
9. **Estimated time:** 需外部參與者。
10. **Technical difficulty:** 高。
11. **Ethics and safety:** 中；避免公開敏感 logs。
12. **Largest failure reason:** 資料不足與選樣偏差。
13. **Reusable output if successful:** protocol、ledger schema。
14. **Knowledge if unsuccessful:** 可形成招募與負面證據。
15. **Can be completed here:** 目前被外部驗證阻擋。
**Score breakdown:** public_importance=12, gap_reality=9, testability=13, feasibility=12, reproducibility=8, reuse=8, novelty=4, growth=1, maintenance=0.

### 20. Agent Skill performance benchmark — 66/100

1. **Specific question:** 加入 Agent Skill 是否在固定任務上提高成功率、降低步驟或錯誤？
2. **Public-interest importance:** 避免用不可驗證宣傳取代實際效能。
3. **Affected parties:** AI 工具使用者與 Skill 作者。
4. **Existing solutions:** agent eval frameworks、task benchmarks。
5. **Specific insufficiency:** 跨平台模型版本、成本與隨機性難控制。
6. **Available data:** 合成與公開任務集。
7. **Executable experiment:** 同模型同 prompt，skill/no-skill 重複實驗。
8. **Quantitative metrics:** 成功率、token、時間、錯誤類型。
9. **Estimated time:** 5–10 天。
10. **Technical difficulty:** 高。
11. **Ethics and safety:** 低中。
12. **Largest failure reason:** 缺付費 API 與版本穩定性。
13. **Reusable output if successful:** benchmark、task pack。
14. **Knowledge if unsuccessful:** 可記錄不可比較因素。
15. **Can be completed here:** 當前無付費 API，不適合。
**Score breakdown:** public_importance=11, gap_reality=9, testability=13, feasibility=10, reproducibility=8, reuse=8, novelty=6, growth=1, maintenance=0.

### 21. RO-Crate minimal validator gap — 65/100

1. **Specific question:** 小型研究包的 RO-Crate 是否符合少數關鍵可重現關係，而不只是 JSON-LD schema 可解析？
2. **Public-interest importance:** 形式有效但語意缺失會造成假 FAIR。
3. **Affected parties:** 研究資料管理員與 RSE。
4. **Existing solutions:** ro-crate-py、SHACL、profiles。
5. **Specific insufficiency:** 已有成熟 validators，新增工具差異可能不足。
6. **Available data:** 公開 RO-Crates 與合成 fixtures。
7. **Executable experiment:** 定義最低 profile，和既有 validator 比較。
8. **Quantitative metrics:** 新增真陽性、誤報、可用性。
9. **Estimated time:** 2–3 天。
10. **Technical difficulty:** 中。
11. **Ethics and safety:** 低。
12. **Largest failure reason:** 研究缺口可能已被現有工具覆蓋。
13. **Reusable output if successful:** profile tests、fixtures。
14. **Knowledge if unsuccessful:** 證明無需新工具。
15. **Can be completed here:** 可完成但價值較低。
**Score breakdown:** public_importance=11, gap_reality=8, testability=13, feasibility=13, reproducibility=8, reuse=8, novelty=4, growth=0, maintenance=0.
