# Holes

(THIS IS VERY WIP)

This is a personal project to play around with making short callables (e.g lambdas)
by only defining the body.

It introduces a new Hole object (exported as `_`) which can be used in arithmetic
expressions to build a callable e.g.

```python
from holes import _

double = _ * 2
assert double(5) == 10
```

In this case, `_ * 2` is *roughly* equivalent to `lambda _: _ * 2`.

A hole can be used multiple times in the same expression just like a parameter.
For example, the above example could be rewritten as

```python
from holes import _

double = _ + _
assert double(5) == 10
```


```python
assert list(map(_ * 2, [1, 2, 3])) == [2, 4, 6]
```

# Limitations and Differences

The `lambda` keyword introduces a new scope which means the entirety of the body is
executed when it is called. 

Lambdas created using Holes do not create a new scope and so care must be taken with
how they are built

```python
from holes import _

f = lambda _: print(_)
f(5)   # Prints "5"

f = print(_)  # Eagerly prints the Hole object `_`
f(5)  # Raises an attribute error as f is None (the result of print)
```
