# Holes

This is a personal project to play around with making lambdas (kinda).

It introduces a new concept called a Hole (exported as `_`) which allows you to define
a lambda:

```python
from holes import _

double = _ * 2
assert double(5) == 10
```


# Limitations

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
