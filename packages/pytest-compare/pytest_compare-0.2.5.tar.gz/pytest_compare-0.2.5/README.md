# pytest-compare

[![PyPI Latest Release](https://img.shields.io/pypi/v/pytest_compare.svg)](https://pypi.org/project/pytest-compare/)
[![License](https://camo.githubusercontent.com/2439ed6934e5c87e17a7d562cfb92c91d2a673d8/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f726168756c646b6a61696e2f6769746875622d70726f66696c652d726561646d652d67656e657261746f723f7374796c653d666c61742d737175617265)](https://pytesty.github.io/pytest-compare/license/)
[![Documentation](https://readthedocs.org/projects/pytest/badge/?version=latest)](https://pytesty.github.io/pytest-compare/documentation/)
[![Downloads](https://static.pepy.tech/badge/pytest-compare/month)](https://pepy.tech/project/pytest-compare)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)x

# What is it?
The `pytest-compare` helps validate method call arguments when testing python code.

`pytest-compare` is designed to work with [assert methods](https://docs.python.org/3/library/unittest.mock.html#the-mock-class). While python native variables can be easily compared, a more complicated structures sometimes do not. For example validating a `pd.DataFrame` will raise an exception. This is where `pytest-compare` comes in. It allows this kind of structures to be easily compared.

# How to install
To install `pytest-compare` from PyPi, run the command:

```sh
pip install pytest-compare
```

## Optional dependencies
Some compare modules may require additional packages to be installed.

### Pandas
To compare [pandas](https://pandas.pydata.org/) module, add the `pandas` option to the installation:

```sh
pip install pytest-compare[pandas]
```

# How to use
The comparation modules are design to be used with [assert methods](https://docs.python.org/3/library/unittest.mock.html#the-mock-class). When validating patched method call arguments 

```python
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

with patch.object(ProductionClass, 'method', return_value=None) as mock_method:
    thing = ProductionClass()
    thing.method(df)
```

```python
# will raise an exception
mock_method.assert_called_once_with(df)

# the correct way
mock_method.assert_called_once_with(CompareDataFrame(df))
```

## Multiple arguments in a call
When a method is called using multiple arguments, all of them must be addressed in the test. while python native variables can be easily compared, `pytest-compare` is designed to compare a more complicated structures and do custom compares.

```python
with patch.object(ProductionClass, 'method', return_value=None) as mock_method:
    thing = ProductionClass()
    thing.method(1, "str", df1, df2)
    
# the correct way
mock_method.assert_called_once_with(1, "str", CompareDataFrame(df1), CompareDataFrame(df2))
```

## Args and Kwargs
When validating the call, the expected values must be passed in the exact same mix of args and kwargs as when they were called.

```python
with patch.object(ProductionClass, 'method', return_value=None) as mock_method:
    thing = ProductionClass()
    thing.method(df1, dataframe=df2)
    
# the correct way
mock_method.assert_called_once_with(CompareDataFrame(df1), dataframe=CompareDataFrame(df2))
```

### Actual and Expected convention
* actual: The values that the method was originally called with.
* expected: Test values to see if the method was called with.

For example here, `arg_actual` is the actual value while `arg_expected` is the expected value.

```python
mock_method = Mock()

mock_method(arg_actual)
mock_method.assert_called_once_with(arg_expected)
```

If `arg_actual` is not equal to `arg_expected`, an exception will be raised.


# Development

## Setup

### Virtual Environment

Create a virtual environment and install the dependencies:

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -e ".[pandas]" -r requirements-dev.txt -r requirements-quality.txt

### Pre-commit Hooks

Start by installing the pre-commit hooks which will run `black`, `mypy`, `flake8`, and `codespell` on every commit.:

    $ hooks/autohook.sh install

## Creating tests

### Running tests

To test the code, run the following command:

    $ pytest

### Writing tests

Tests are written using the `pytest` framework. To create a test for a new `Compare` module, create two files in the `tests` directory: `conftest.py` and the test file witch must start with `test_`.
The `conftest.py` file must implement the following fixtures:

```python
@pytest.fixture
def actual_call_args() -> Tuple[Any]:
    raise NotImplementedError("`actual_call_args` must be implemented")


@pytest.fixture
def actual_call_kwargs() -> Dict[str, Any]:
    raise NotImplementedError("`actual_call_kwargs` must be implemented")


@pytest.fixture
def expected_call_args() -> Tuple[Any]:
    raise NotImplementedError("`expected_call_args` must be implemented")


@pytest.fixture
def expected_call_kwargs() -> Dict[str, CompareBase]:
    raise NotImplementedError("`expected_call_kwargs` must be implemented")
```

The test file must implement a test class that inherits from `BaseTest`.

That way two base tests will be run for each `Compare` module that wil test the `args` and `kwargs` of the method call.
