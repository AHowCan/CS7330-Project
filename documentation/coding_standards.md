# Coding Standards for CS7330-Project

## Non-python files

No naming convention, just try to be consistent with files of same type

## Python

- Simplified version of the official python style guide [PEP8](https://www.python.org/dev/peps/pep-0008/)
- These are only general guidelines, don't be afraid to break them if there are specific justifications

### Naming

- Naming things is very important, give your variables meaningful names

    ```python
    # Wrong:
    vdas = 15
    # Correct:
    average_employee_salary = 10
    ```

- Avoid abbreviations unless you think most people on the team will instantly know what they mean.

    ```python
    # OK:
    my_db = SomeDB()
    # Hard to decipher:
    avg_nb_qlty = 10
    ```

- File names
  - `some_python_file.py`
- Class names
  - `SomeClass`
- Functions, methods and variables
  - `some_function()`
  - `some_class_object.some_method()`
  - `some_variable`
- Global config variables
  - Only defined in `config.py` and `local_config.py`
  - `ALL_CAPS_CONFIG_VAR`
- Private/internal variables
  - Python does not have private variables, but use leading underscore to communicate intention
  - `_private_var`

### Imports

- Do not use `from somemodule import *`
  - Instead either import each used item individually or just use `import somemodule` and call each item from the module `somemodule.somefunc`
  - You will write more code but it will make code cleaner for easy bug tracking

### Coding style

- Indentation
  - 4 spaces per level
  - match brackets and braces

    ```python
    foo = long_function_name(var_one, var_two,
                            var_three, var_four)
    ```

- Maximum Line Length
  - Limit all lines to a maximum of 79 characters.
  - Use \ for line continuation


- Use spaces around operators to signify priority

    ```python
    # Correct:
    i = i + 1
    submitted += 1
    x = x*2 - 1
    hypot2 = x*x + y*y
    c = (a+b) * (a-b)

    # Wrong:
    i=i+1
    submitted +=1
    x = x * 2 - 1
    hypot2 = x * x + y * y
    c = (a + b) * (a - b)
    ```

### Comments

- Comments that contradict code are worse than no comments. Prioritize keeping comments up-to-date.
- Don't use comments that state the obvious, python code itself is very readable

    ```python
    # Useless:
    x = x + 1                 # Increment x
    # Useful:
    x = x + 1                 # Compensate for border
    ```
