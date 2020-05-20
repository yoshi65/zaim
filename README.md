# zaim
Visualize household accounts in [zaim](https://zaim.net/) as graphs and lists.
And, add household account book on the command line.

## Preparation
After authentication with OAuth with reference to [How to authorize](https://dev.zaim.net/home/api/authorize), please make `input/key.csv`.
```csv:key.csv
consumer_key,consumer_secret,access_token,access_secret
hoge,hoge,hoge,hoge
```

### Support to authorization
1. `https://dev.zaim.net/`に登録して、アプリケーションを作る
1. 得られたアプリケーションのコンシューマ ID, コンシューマシークレットを以下のフォーマットで`key.csv`に書き込む (access_token,access_secretの値はスクリプト実行後に記入される)
    ```
    consumer_key,consumer_secret,access_token,access_secret
    hoge,hoge,hoge,hoge
    ```
1. スクリプトを実行
    - `python auth.py`
1. zaimアカウントの認証
    - 実行結果に出力されたURLにアクセス
      ```
      auth link
      https://auth.zaim.net/users/auth?oauth_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      ```
    - ログインして認証
1. 認証完了後、以下のメッセージが表示され、ページが遷移しない
    ```
    認証が完了

    お待ちください…しばらく待って画面が変わらない場合は、一つ前に戻って「ログイン」ボタンをタップするか info@zaim.net までご報告ください。
    ```
1. htmlを開き、`callback`を探す
    ```
    <div class="callback">https://www.zaim.net/?oauth_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&oauth_verifier=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<div class="callback_end"></div></div>
    ```
1. oauth_verifierを取得
    ```
    % grep "callback" tmp.html | sed "s/.*oauth_verifier=\(.*\)\<div.*callback.*/\1/g"
    ```
1. What is the PIN? 以下にoauth_verifierを入力すると、`key_tmp.csv`が出力される
    ```
    {'oauth_token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'oauth_token_secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}
    ```

## Usage
```sh:zaim.py
usage: zaim.py [-h] [-p] [-i] [-d [NUM]] [-m {payment,income,transfer}]
               [-g [YYYY-MM]] [-b]

Visualize household accounts in zaim.net as graphs and lists.

optional arguments:
  -h, --help            show this help message and exit
  -p, --place           search for KEYWORD in place
  -i, --input           Input data
  -d [NUM], --display [NUM]
                        Display latest household accounts(NUM is the number of
                        data)
  -m {payment,income,transfer}, --mode {payment,income,transfer}
                        choice kind of movement of money
  -g [YYYY-MM], --graph [YYYY-MM]
                        select category and draw graph in a month
  -b, --balance-make    make balance difference between actual and calculated
                        balance
```

### Attention
RelativePayment and MonthlyCategoryGraph function in graph.py is Japanese and a personal specifiction.

## Example
By default, The current remaining balance is displayed.
If results differ from the actual balance, please use `-b` option to generate the difference in `input/balance_diff.csv`.
```sh
% python3 zaim.py
```

If you want to display the last 10 payment(amount, amount, date, mode, place, category, genre).
```sh
% python3 zaim.py -d
```

If you want to see daily expenditure in April 2018.
```sh
% python3 zaim.py -g 2018-04
```
After you choice category or genre, draw graph and output in `output`.

If you want to add household account book.
```sh
% python3 zaim.py -i
How much?
1000

When?
Format:YYYY-MM-DD
2018-05-10

Which is Mode?
payment or income or transfer
payment

Account LIST
hoge geho foo bar
What is from Account?
hoge

payment category LIST
hoge geho foo bar
What is Category?
bar

bar genre LIST
hoge geho foo bar
What is Genre?
foo

success!
```
