# flask_rest_api


### Blueprintを使ってアプリケーションのURLを分ける．
[Blueprintを使う](https://qiita.com/m-masaki72/items/b07f7dfe4c8965486af3)  
[Key毎に変える](https://qiita.com/tomson784/items/406281bef7a5b2eb3cd8)  
[APIサンプル](https://qiita.com/tchnkmr/items/26d271886b46c4e52dc1)

    /sampler/xxx
    /result
    /jobs
    /test

### 非同期にsamplerを処理する．

1. jobを投げる
2. jobを登録し，job_idを発行する．
3. job_idを返す．
4. jobをsampleする．
5. jobが終わる．
6. job_idでjobを取得する．
