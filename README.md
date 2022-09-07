# ugent-food

![PyPI](https://img.shields.io/pypi/v/ugent_food)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ugent_food)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/stijndcl/ugent-food/Python)

Command-line tool to get the current menu for Ghent University restaurants.

This application was made using [Zeus WPI](https://github.com/ZeusWPI)'
s [Hydra API](https://github.com/ZeusWPI/hydra/blob/master/api-resto-02.md).

## Installation

It's recommended to install the tool using [``pipx``](https://pypa.github.io/pipx/#install-pipx) to allow running the
command from anywhere on your PC, without having to invoke it using `python3 -m ugent_food`.

```sh
$ pipx install ugent-food
```

If you don't want to use `pipx`, it can also be installed using `pip`:

```sh
$ pip3 install --user ugent-food
```

_Note: **Don't install this in a Virtual Environment**, as you won't be able to run it from anywhere else._

Next, you can add an alias to your `.bashrc` or `.zshrc` for your own convenience:

```sh
# If you installed using pipx
$ echo 'alias food="ugent-food"' >> ~/.bashrc
$ echo 'alias food="ugent-food"' >> ~/.zshrc

# If you installed using pip
$ echo 'alias food="python3 -m ugent_food"' >> ~/.bashrc
$ echo 'alias food="python3 -m ugent_food"' >> ~/.zshrc
```

You can now simply use `food` to run the tool.

## Usage

_To keep the examples short, they use `food` instead of `python3 -m ugent_food` to invoke the tool._

### Menus

To get the menu for a given day, use the ``menu`` command. By default, not passing any arguments will fetch today's
menu:

```sh
$ food
```

For convenience, passing this command is **optional**. You can immediately pass a day (or subcommand) instead of having
to explicitly add this as well. The above line is equivalent to

```sh
$ food menu
```

#### Arguments

To fetch the menu for a specific day, an extra argument can be passed. This can either be a weekday, an offset (relative
to today), or a day in `DD/MM`-format:

```sh
$ food monday
$ food tomorrow
$ food 21/09
```

### Configuration

The tool has a couple of settings that you can configure using the `set` subcommand:

```sh
$ food config set skip_weekends true
```

You can list the current settings with `config ls`:

```sh
$ food config ls
```

#### Available settings

Note that `boolean` arguments can be supplied as any of `[true, false, t, f, 1, 0]`.

| Name          | Description                                                                                                                                                                                                                                                         | Type (choices)                                                 | Default |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------|---------|
| hidden        | A list of meal kinds that should be hidden when fetching menus. This can be useful for vegetarians and vegans who don't care about the meat dishes.                                                                                                                 | List\[String\] ("fish", "meat", "soup", "vegan", "vegetarian") | []      |
| language      | The language used to fetch the menus in.                                                                                                                                                                                                                            | String ("en" 🇬🇧 , "nl" 🇧🇪/🇳🇱)                            | "en"    |
| skip_weekends | Whether to automatically skip weekends when fetching menus without an explicit day argument. This defaults to true because the restaurants aren't usually open during weekends. For example: using the tool on a Saturday will show the menu for the coming Monday. | Boolean                                                        | True    |
