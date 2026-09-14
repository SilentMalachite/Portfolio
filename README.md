# SilentMalachite Portfolio

福祉×IT・アクセシビリティを軸にした、転職向けポートフォリオです。HTML/CSSによる静的サイトとして実装しています。

## ローカル表示

プロジェクトのルートで次を実行します。Python 3が必要です。

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory site
```

[ローカルプレビュー](http://127.0.0.1:8765/)を開きます。サーバーの終了は `Ctrl+C`。この簡易プレビューはドメインルートで表示します。実際の公開先は `/Portfolio/` 配下で、今回のブラウザ検証ではその配置も確認しています。

## 構成と編集箇所

| ファイル | 役割 |
| --- | --- |
| `site/index.html` | 日本語版。自己紹介、主要4事例、補足3件、関連2件、採用案内 |
| `site/en/index.html` | 同じ事例・状態注記を含む英語版 |
| `site/assets/styles.css` | 配色・レイアウト・レスポンシブ・フォーカス・印刷表示 |
| `site/assets/favicon.svg` | 2つの経路をつなぐ独自のモノグラム。ヘッダー・フッターでも使用 |
| `site/assets/paths.svg` | 「理解と技術をつなぐ」ことを表すヒーロー用の図版 |
| `site/assets/ogp.svg` / `ogp.png` | SNS共有用の原稿と1200×630の配信用画像 |
| `site/assets/ogp-en.svg` / `ogp-en.png` | 英語版SNS共有用の原稿と配信用画像 |
| `site/404.html` | 日英両方の公開トップに戻れる共通404ページ |
| `scripts/check_site.py` | 公開ファイル、リンク・アンカー、メタデータ、サイズの静的検査 |
| `.github/workflows/pages.yml` | 静的検査後に `site/` だけをGitHub Pagesへ公開 |
| `AGENTS.md` / `SPEC.md` | 作業規約と製品仕様・受け入れ条件 |

クライアントJavaScript、フレームワーク、Webフォント、トラッカー、外部画像、ビルド用の依存インストールは不要です。作品の色付き図版はこのポートフォリオ用の装飾で、実際のアプリ画面や各作品の既存公式ロゴではありません。

OGPのPNGはSVGから生成済みです。変更時は、SVGの日本語フォントが正しく表示される環境で1200×630のPNGへ書き出し、文字欠けを目視確認してください。今回の生成にはローカルのSharpを使用しましたが、閲覧・公開時の依存には含まれません。

## 確認コマンド

```sh
python3 scripts/check_site.py
```

標準ライブラリのみを使用します。ページ内リンク・画像参照、A11yLabの直リンク2箇所、OGP、404の戻り先、公開ファイルの合計1MB以内などを検査します。外部リンク先の可用性、見た目、読み上げの品質を保証するものではありません。

## GitHub Pagesへの公開

公開先は [日本語版](https://silentmalachite.github.io/Portfolio/) と [English](https://silentmalachite.github.io/Portfolio/en/) です。公開リポジトリは [SilentMalachite/Portfolio](https://github.com/SilentMalachite/Portfolio)、公開ブランチは `main`、PagesのSourceはGitHub Actionsです。

公開設定・更新時は次を確認します。

1. 公開リポジトリ名を `SilentMalachite/Portfolio`、公開ブランチを `main` とする。別名にする場合はHTMLのcanonical・OGP、404のリンク、検査スクリプトの `BASE` と仕様を同時に変更する。
2. GitHubの Settings → Pages → Build and deployment → Source で **GitHub Actions** を選ぶ。
3. 公開用原稿と実際の連絡方法を確認したうえで `main` にpushする。
4. `Publish portfolio to GitHub Pages` の成功後、公開URLでトップ、画像・CSS、A11yLabへのリンク、存在しないパスの404を確認する。

以後の `main` へのpushは自動公開を伴います。ワークフローは手動起動にも対応しますが、deployは `main` のみに限定しています。公開権限はdeployジョブに限定し、公式Actionsは確認したcommit SHAに固定しています。旧状態へ戻す際は対象の変更をrevertして `main` へ反映し、再公開結果を確認します。

公開artifactの対象は `site/` です。README・SPEC・検査スクリプト・作業記録はWebサイトのartifactには含めません。ただし公開GitHubリポジトリにコミットしたファイルはGitHub上では閲覧可能です。応募者の私的事情・秘密情報を管理文書へ追記しないでください。

## 原稿の出典

確認日: **2026-09-10**。公開資料に書かれた用途・設計を紹介するもので、各アプリの動作をこのサイト作業で検証したという意味ではありません。

| 対象 | 確認した公開資料 |
| --- | --- |
| A11yLab | [サイト](https://silentmalachite.github.io/A11yLab/)、[要約筆記と制作背景](https://silentmalachite.github.io/A11yLab/hearing/2026-01-03-summaryapp/)、[キーボード操作](https://silentmalachite.github.io/A11yLab/physical/2026-01-02-keyboard-nav/)、[字幕](https://silentmalachite.github.io/A11yLab/hearing/2026-01-01-captions/)、[コントラスト](https://silentmalachite.github.io/A11yLab/visual/2026-01-01-color-contrast/) |
| SummaryTalk | [README](https://github.com/SilentMalachite/SummaryTalk#readme) |
| AlchemIIIF | [README](https://github.com/SilentMalachite/AlchemIIIF#readme)。考古学の専門性と福祉をつなぐ掲載意図は本人の指定 |
| OmniArchive | [README](https://github.com/SilentMalachite/OmniArchive#readme) |
| Soujo（層序） | [日本語README](https://github.com/SilentMalachite/Soujo/blob/main/README.ja.md)、[英語README](https://github.com/SilentMalachite/Soujo#readme)、[仕様書](https://github.com/SilentMalachite/Soujo/blob/main/SPEC.ja.md)。2026-09-14確認 |
| Tsumugi | [README](https://github.com/SilentMalachite/Tsumugi#readme)。記録・工賃計算と請求機能の未完成範囲を確認 |
| Ayumi | [README](https://github.com/SilentMalachite/Ayumi#readme)。個別支援計画・支援記録、PC1台とLANの構成、請求機能は対象外と確認 |
| BudgetTracker | [README](https://github.com/SilentMalachite/BudgetTracker#readme) |
| MonoOto | [README](https://github.com/SilentMalachite/MonoOto#readme) |

## 今後本人が具体化できる項目

現状は公開情報で分かる制作物と設計を説明しています。2026-09-11の本人指定に基づき、日英の採用欄に略歴（考古学 → 高校講師 → 身体障がい者施設主任支援員 → 病院検査業務 → 就労継続支援B型職業指導員）と保有資格「産業カウンセラー」を掲載しています。各作品の詳細な担当分担、在職期間、希望職種は未提供であり、架空の情報は入れていません。具体的な経験・役割を追記する場合は、本人の確認とWeb公開の意向を反映してください。

採用案内には、本人が公開用として指定したX・Facebookのリンクと、「@」を「[at]」に置き換えたメールアドレスを掲載しています。

## 検証記録

確認日: 2026-09-10。

- `python3 scripts/check_site.py`: 成功。公開ファイル7件、約117KB。公開用tarにも管理文書が含まれないことを確認。
- Chrome / Playwright WebKit 26.5: 幅1440・768・390・320pxで横方向のはみ出しなし、全画像を読み込み。JavaScriptを無効化した状態で確認。
- 全32リンクをキーボードで巡回し、3pxのフォーカス表示を確認。WebKitはmacOSのリンク移動に合わせOption+Tabを使用。ページ内16リンクは、スキップリンクをキーボード、残りをクリックして到達先を確認。
- 計算済みフォントサイズを2倍にする文字拡大検査でも、320px幅で横方向のはみ出しなし。400%ズームに相当する320 CSS pxのリフローを確認。ただしブラウザUIのズーム操作そのものは未実施。
- 装飾を除く表示テキストについて、計算済み色と背景からコントラストを検査。通常文字4.5:1、大きな文字3:1の目標を確認。採用パネルのフォーカス色は明色に修正済み。
- ヘッダーのロゴは文字拡大時に折り返すよう修正。PC・モバイルの画面キャプチャ、各セクションとOGP画像を目視確認。
- 外部リンク14件はHTTP 200。ネットワーク状態やリンク先の変更によって将来の到達性は変わり得る。
- ChromeのA4印刷PDFを確認。本文・主要事例・採用案内を含み、テキスト領域がページ外へはみ出さないことを検査。
- 独立した静的レビューでコピー、主要導線、公開artifact範囲を再確認。

**初版検証時に未実施（公開検証は後述）**: GitHub Actions本番実行、GitHub Pagesでの実公開・任意パスの404、Safariアプリ本体、VoiceOverによる実際の読み上げ、実機スマートフォンでの操作。WebKitの検証はSafariアプリ本体の検証ではありません。WCAG全体への適合を宣言するものではありません。

主要事例の細かな制作分担は本人の確認待ちであり、現状は公開資料から分かる取り組みの紹介です（SPEC C12の担当詳細）。サイト本体は公開済みです。応募用プロフィールの具体化は今後の更新事項です。

### AlchemIIIFへの主要事例差し替え（2026-09-10）

本人の指定により、TsumugiをAlchemIIIFへ差し替えました。考古学の専門家として文化財のデジタル化と就労継続支援の仕事づくりをつなぐ試みを明記し、関連アンカー・図版・紹介文・出典を更新しています。上記の全体検証は初版実装時の記録です。

差し替え後は静的検査を再実行し、Chrome・WebKitの1440 / 768 / 320pxと320pxでの文字200％拡大で横方向のはみ出しがないことを確認しました。新しい内部リンク2件の移動、外部リンクの配置、旧リンクの除去を検査し、PC・モバイルの事例カードを目視確認しています。AlchemIIIFの公開リポジトリとローカルプレビューはHTTP 200でした。実公開と支援技術による検証は未実施です。

### GitHub Pages初回公開（2026-09-10）

本人の公開指示によりGitと公開リポジトリを新規作成し、完成版をmainに初回コミット・pushしました。既存ブランチがないためマージ操作は不要でした。

- [初回公開Actions](https://github.com/SilentMalachite/Portfolio/actions/runs/34438611665): build / deploy成功。
- HTTPSの公開URLをローカルのChrome（headless）で表示し、JavaScript無効・幅1440 / 768 / 320pxで横方向のはみ出しがないこと、画像読込、ページ内アンカー、A11yLabの直リンク2件、AlchemIIIFの掲載を確認。トップ画面を目視確認。
- 存在しない階層のURLでHTTP 404と独自404ページのトップへのリンクを確認。
- 実際のActions artifactをダウンロード・展開一覧で確認し、公開ファイル7件のみで管理文書が含まれないことを確認。
- 公開ファイル7件はHTTPSで取得した内容とローカルファイルが完全一致。サイトからの外部リンク14件はいずれもHTTP 200。
- Safariアプリ本体、VoiceOver、実機スマートフォンでの操作は未検証。

### 英語版の追加（2026-09-10）

英語版は `site/en/index.html` に配置し、日本語版と共通CSS・図版を使います。ヘッダーとフッターの言語リンクで往復でき、ブラウザ言語による自動転送はしません。日英それぞれのcanonical・hreflang・OGPを設定し、英語用OGP画像と日英併記の404を用意しています。日本語原稿の更新時は、英語版の事例・状態注記・リンクも同時に確認してください。

追加時のローカル検証: `python3 scripts/check_site.py` 成功（HTML3ページ、公開ファイル10件、約200KB）。未追加の英語ページ・画像・言語リンクを検査が検出することも先に確認しました。ChromeとWebKitで日英両版の1440 / 768 / 320px、320pxで文字200％拡大、画像読込、通常アンカー、ヘッダー・フッターからの言語切替、キーボードによるスキップリンクを確認。英語版全体・PCとモバイルのトップ・英語OGPを目視確認しました。日英のIDと外部リンク先も一致しています。英語版のVoiceOver・実機スマートフォン・印刷表示は未検証です。公開処理はmainへのpushで実行し、結果はGitHub Actionsの履歴で確認できます。

### 福祉現場に近い制作物への差し替え（2026-09-10）

Hirundo・KappanをTsumugi・Ayumiへ日英同時に差し替え、両方に開発中の表示を追加。上記2件の公開READMEを再確認し、Tsumugiの請求機能の未完成範囲とAyumiの請求対象外を紹介文に反映しました。静的検査成功、Chrome・WebKitの日英両版で1440 / 768 / 320pxと文字200％拡大の横方向のはみ出しなし、新リンク・状態表示・旧リンク除去を確認。PCとモバイルの対象セクションを目視確認しました。各アプリ自体の動作・導入効果を検証した記録ではありません。

### ヒーローアニメーション（2026-09-11）

M字を構成する2つのアーチが、0.45秒の時間差で、それぞれ2.4秒かけて40px下から元の位置へ戻りながら表示されます。続いて通路の2本の線が合流し、到達点の色の変化まで含め4.8秒で一度だけ再生して停止します。閲覧にはJavaScriptを必要としません。任意の再生・停止ボタンだけに小さなローカルスクリプトを使用し、ライブラリは追加していません。動きを減らす設定では初めから完成状態を表示し、再生中に設定を変更した場合も完成状態へ切り替わります。印刷時は従来どおり図版を非表示にします。

Safariで外部SVGのグループをuseで参照するとグラデーション面が欠けたため、図形と色・影の定義を日英HTML内の装飾SVGに直接埋め込んでいます。図形原稿 `site/assets/paths.svg` を変更する際は、日英HTMLの埋め込みも同期してください。古いCSSのキャッシュを避けるため、日英のCSS参照に更新識別子 `?v=20260911-replay2` を付けています。

公開前の再検証: 静的検査と差分検査に成功（HTML3ページ、公開ファイル合計208,948 bytes）。日英のヒーローSVG、原稿SVGの図形・定義の一致、紹介文に変更がないことを確認しました。ローカルの `/Portfolio/` 配下で、ChromeのJavaScript無効・日英両版について、描画途中と終了後の静止、1440 / 768 / 320px、320pxで文字200％拡大、キーボードのスキップリンク、言語切替、動きを減らす設定での初期表示と再生中の切替、印刷時の図版非表示を確認しました。独立した差分レビューでも公開を妨げる確定不具合は見つかりませんでした。

MacのSafari実機では修正後の完成図を確認しました。このMacの「動きを減らす」設定は有効なため、通常再生はリポジトリ外の一時複製ページに限りCSSのメディア条件を変更して確認しました。400ms・1500msのアーチの進行、3200msの経路描画途中、5300msの完成状態を確認しています。OS設定と公開用CSSのメディア条件は変更していません。Codex内プレビューでも「動きを減らす」が有効だったため、静止表示になります。今回のiPhone／iPad、VoiceOverは未検証です。公開結果は [GitHub Actions](https://github.com/SilentMalachite/Portfolio/actions/workflows/pages.yml) と公開ページで確認できます。

### アニメーションの手動再生・停止（2026-09-11）

日英ページに「アニメーションを再生」／「Play animation」ボタンを追加しました。動きを減らす設定でもボタン操作時だけ一度再生し、再生中は「アニメーションを停止」／「Stop animation」に切り替わります。停止時と終了時は完成図に戻り、ボタンのフォーカスを保持して繰り返し再生できます。JavaScript無効時はボタンを隠し、本文と完成図を表示します。静的検査で許可するスクリプトは、このローカルのdefer付き拡張のみです。

検証: Chromeで日英両版の再生・停止・再再生、Enter／Space操作、終了後のフォーカス保持、動きを減らす設定の初期表示と途中変更、通常設定での自動再生、JavaScript無効時の完成図、1440／768／320px幅、320pxで文字200％拡大、印刷時の非表示を確認しました。MacのSafari実機でも、OSの動きを減らす設定を有効にしたまま、ボタンからの再生と終了後の完成図を確認しました。説明文とボタンは通常の文書フローに置き、拡大時の重なりを防いでいます。静的検査と差分検査に成功しています。iPhone／iPad、VoiceOverは今回未検証です。

### 略歴・資格の追加確認（2026-09-11）

- 日英の採用欄に、本人指定の略歴と産業カウンセラー資格を追加。
- ローカルHTTP配信をCodex内蔵ブラウザで確認。幅1440px・320pxで略歴と資格の折り返し・表示を目視確認し、横方向のはみ出しなし。
- `python3 scripts/check_site.py` と `git diff --check` が成功。今回の確認ではSafari・実機スマートフォン・VoiceOverは未実施。

### Soujoへの差し替え（2026-09-14）

本人の指定により、日英のagent-review-ts紹介をSoujo（層序）へ差し替え、開発姿勢の説明も「特性を設計に変える」に更新。公開README・仕様書で確認した、小さな作業単位と記録による中断・再開の設計を紹介しています。

検証: `python3 scripts/check_site.py` と `git diff --check` が成功。ローカルHTTPの `/Portfolio/` 配下をCodex内蔵ブラウザで確認し、日英両版の1440／768／320px幅で横方向のはみ出しなし。PC・モバイルの紹介文を目視確認し、開発姿勢欄からSoujo紹介への内部リンクの移動も確認しました。旧作品の名称・URLが公開HTMLに残っていないことと、日英のID・外部リンクの一致を確認しました。

上記は公開前のローカル検証記録です。Safari・実機スマートフォン・VoiceOver・文字200％拡大・JavaScript無効時の表示は今回未検証です。Soujo自体の動作や効果をこのサイト作業で検証した記録ではありません。
