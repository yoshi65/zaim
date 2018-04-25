# zaim
Visualize household accounts in [zaim](https://zaim.net/) as graphs and lists.

## Usage
```sh
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
You want to see daily expenditure in April 2018.
```sh
python3 zaim.py -g 2018-04
```
After you choice category or genre, draw graph and output in `./data`.
