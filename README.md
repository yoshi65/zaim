# zaim
Visualize household accounts in [zaim](https://zaim.net/) as graphs and lists.

## Preparation
After authentication with OAuth with reference to [How to authorize](https://dev.zaim.net/home/api/authorize), please make `key.csv`.
```csv:key.csv
consumer_key,consumer_secret,access_token,access_secret
hoge,hoge,hoge,hoge
```

## Usage
```sh:zaim.py
usage: zaim.py [-h] [-p] [-m {payment,income,transfer}] [-n NUM] [-g YYYY-MM]

Visualize household accounts in zaim.net as graphs and lists.

optional arguments:
  -h, --help            show this help message and exit
  -p, --place           search for KEYWORD in place
  -m {payment,income,transfer}, --mode {payment,income,transfer}
                        choice kind of movement of money
  -n NUM, --num NUM     decide the number of movement to display
  -g YYYY-MM, --graph YYYY-MM
                        select category and draw graph in a month
```

### Attention
RelativePayment and MonthlyCategoryGraph function in graph.py is Japanese and a personal specifiction.

## Example
By default, the last 10 payment(amount, amount, date, mode, place, category) is displayed.
```sh
python3 zaim.py
```

You want to see daily expenditure in April 2018.
```sh
python3 zaim.py -g 2018-04
```
After you choice category or genre, draw graph and output in `./data`.
