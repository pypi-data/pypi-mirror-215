# primary math
It's a Python's [library](https://pypi.org/project/primary-math/) for elementary math stuff, based on the book 
[Everything You Need to Ace Math](https://www.amazon.com/Everything-You-Need-Math-Notebook/dp/0761160965).

## Installation

```shell
$ python3 -m pip install primary-math
```

### Requirements

The only requirement is Python 3.11.

> It should work fine with Python 3.10, but I didn't test it. 

## Usage

```python
import primarymath as pmath

number = pmath.Number(4)

print(number.value())         # 4
print(number.is_even())       # True
print(number.is_positive())   # True
print(number.previous())      # 3
print(number.next())          # 5
```

## License
This repository is available under the [MIT License](LICENSE).
