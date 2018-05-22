# zaim
Visualize household accounts in [zaim](https://zaim.net/) as graphs and lists.
And, add household account book on the command line.

## Preparation
After authentication with OAuth with reference to [How to authorize](https://dev.zaim.net/home/api/authorize), please make `key.csv`.
```csv:key.csv
consumer_key,consumer_secret,access_token,access_secret
hoge,hoge,hoge,hoge
```

## Usage
```sh:zaim.py
usage: zaim.py [-h] [-p] [-i] [-d [NUM]] [-m {payment,income,transfer}]
               [-g [YYYY-MM]]

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
```

### Attention
RelativePayment and MonthlyCategoryGraph function in graph.py is Japanese and a personal specifiction.

## Example
By default, The current remaining balance is displayed.
If results differ from the actual balance, please write the difference in `balance_diff.csv`.
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
After you choice category or genre, draw graph and output in `./data`.

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
