# otter-assign: Jupyter Notebook Assignments with Otter-Grader

Format and tools for authoring and distributing Jupyter notebook assignments with autograding using [Otter-Grader](https://github.com/ucbds-infra/otter-grader).

Requires: **Python 3** (even if it's installed, check that it's your working version `python --version`)


## Getting started
Course instructors author assignments as Jupyter notebooks by creating a
notebook that contains setup code, questions, solutions, and tests to validate
those solutions. This project prepares an assignment to be distributed to
students and later scored automatically.

The [notebook format](docs/notebook-format.md) is not specific to a programming
language or autograding framework, but was designed to be used with
Otter, which is Python based. Contributions to
support other testing frameworks, such as nbgrader and other programming
languages, are welcome.

An example notebook appears in `test/example.ipynb`, which uses the [notebook
format](docs/notebook-format.md). To convert it, run:

```
oassign test/example.ipynb test/output
```


* `test/example.ipynb`: an example notebook path that you'll need to replace with the _path to the master solution notebook_, which was augmented with the metadata and commands from the [notebook format](docs/notebook-format.md).
* `test/output`: _the path to where the output will be stored_ 
  * the output contains two directories `autograder` and `student`
  * the `autograder` directory contains the full set of tests and a solution notebook (a solution notebook is different from the master notebook, because it is not formatted accordidng to the [notebook format](docs/notebook-format.md) but instead looks like the student notebook with solutions)
  * the `student` directory contains an automatically created redacted version. 
* at the end of the command, specify paths to any support files (e.g. data files) needed by the notebooks to be copied into the `autograder` and `student` directories


Before you run the `oassign` command, make sure that you **run the entire notebook** top to bottom (`Cell -> Run All`) to make sure that every cell has the correct output -- the output of the cells will be turned into the appropriate tests stored in the provided output directory (second argument of the `oassign` command). If you change the tests, you need to re-generate the files by re-running the notebook and the `oassign` command. 

<!-- **Note**: `oassign` will issue an error and quit if the output directory already exists. -->


<!-- 

You can then generate a PDF from the result:

```python
jassign-pdf tests/output/autograder/example.ipynb tests/output/autograder/example.pdf
``` -->


## Caution

#### Test outside of a question

```
File "/opt/conda/lib/python3.6/site-packages/oassign/to_ok.py", line 141, in gen_ok_cells
    assert not is_test_cell(cell), 'Test outside of a question: ' + str(cell)
AssertionError: Test outside of a question:
```

If you get this error, this means that you have _more than one cell_ between the markdown cell that declared the question (i.e., the one that contains `#BEGIN QUESTION`) and the cell that contains the `# TEST`. 


**SOLUTION**: remove the extra code/markdown cell(s) either between the solution cell and the markdown cell with the `#BEGIN QUESTION` or between the solution cell and the `# TEST` cell.

#### Test cell with a blank on the last line

If your test contains a blank/newline after the test, otter-assign seems to automatically add a semicolon at the end of the test, thus, supressing the output of the command.

Example:

```python
# TEST
movies.head(1)['plots'][0]=='Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.'

```

Turns into the following failed test in the students' notebook:

```python
>>> movies.head(1)['plots'][0]=='Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.';
>>> 

# Error: expected
#     True
# but got

```

**SOLUTION**: remove the blank line at the end of the `# TEST` cell.
