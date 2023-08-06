<div align="center">

# Cron Library

------ A libary by RainyDais ------

</div>

<div align="center">
    <img src="docs/div.png" alt="divider"/>
</div>

<div align="center">
  
# How it works

The cron Library provides a simple and efficient way to automate tasks based on specified time intervals.

# How to use

</div>

<div align="left">
<div align="center">
    <img src="docs/1.png" alt="divider"/>
</div>

* Import the module to use the cron library

This can be done by using:

```python
import cron
```

<div align="center">
    <img src="docs/2.png" alt="divider"/>
</div>

* Define a function

This can be done using:

```python
def your_function():
    print("your_text")
```

The `def your_function():` is what you use to make a function, this function will say `your_text`.

Example:

```python
def Hello_Function():
    print("Hello World")
```

<div align="center">
    <img src="docs/3.png" alt="divider"/>
</div>

* Define a function that will tell you when it runs, this will be told every `x` seconds

This can be done using:

```python
def time_alert_function(seconds):
    print("I run every {0} seconds!".format(seconds))
```


<div align="center">
    <img src="docs/4.png" alt="divider"/>
</div>

* Create a function to run every `x` amount of times 

Make a first example function to run every 5 seconds

```python
cron.addJob(example_function, 5)
```

Create a second example function to run every 1 second

```python
cron.addJob(time_alert_function, 1, 1)
```

Currently the `addJob` parameters are; `function, timeout/cron delay, args` (only 1 supported currently)

<div align="center">
    <img src="docs/5.png" alt="divider"/>
</div>

* How to call your Cron jobs

You can use this function:

```python
cron.start()
```

Option: pass `True` into the function call to make it non-thread blocking

Example:

```python
cron.start(True)
```
Default is False or thread blocking.

This will start your timer fyunction, that will then execute your cron jobs.

<div align="center">
    <img src="docs/6.png" alt="divider"/>
</div> 

* To prevent your program from ending whilst using `non-thread blocking mode`

You can use:

```python
input("\n   Hello, this is the end of the file!\n\n")
```

This will also act as a test to prove `cron.start()` isn't blocking the thread
It contains newline characters so it doesn't get put on the same line as
other print messages that will come in from the threaded cron jobs.
</div>
