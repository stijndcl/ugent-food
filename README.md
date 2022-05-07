# ugent-food
Command-line tool to get the current menu for Ghent University restaurants.

This application was made using [Zeus WPI](https://github.com/ZeusWPI)'s [Hydra API](https://github.com/ZeusWPI/hydra/blob/master/api-resto-02.md).

## Installation

The tool can be installed using `pip`:

```sh
pip3 install --user ugent-food
```

_Note: **do not forget the `--user`-flag, and don't install this in a Virtual Environment.**_

Next, you can add an alias to your `.bashrc` or `.zshrc` for your own convenience:

```sh
echo 'alias food="python3 -m ugent_food"' >> ~/.zshrc
```

## Usage

_To keep the examples short, they use `food` instead of `python3 -m ugent_food`._