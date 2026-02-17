# Largest One-Line Number Puzzle

## Task Description

The goal of this task is to build the largest one-line number puzzle.
You need to connect number fragments into one long sequence.
The connection rule is simple:

- You can connect fragments if the last two digits of one number are the same as the first two digits of another number.

- The puzzle must be one line only (numbers placed one after another).

- Each fragment can be used only one time.

The input file contains only digits.
Your program must find the longest possible sequence from the given fragments.


## Example
Input fragments:
```
608017
248460
962282
994725
177092
```

### Analysis

We check the first two and last two digits of each number.
Possible chain:
```
248460 → 608017 → 177092
```

### Explanation:

- 248460 ends with 60
- 608017 starts with 60 and ends with 17
- 177092 starts with 17

Final result:

```
24846080177092
```

## Requirements
- Use each fragment only once.
- Build the longest possible sequence.
- Output the final combined number.
- Input file contains digits only.

## Expected Result
The program should print the longest possible connected number sequence.


## Running Tests

Make sure you are in the project root directory.

### Windows (PowerShell)

```powershell
$env:PYTHONPATH = "$PWD"
pytest
