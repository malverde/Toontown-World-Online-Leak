Git Style Guidelines
====================
For Git, we try to follow a general pattern for commit messages and branch naming to make things organized and neat.
- - -

## Committing ##
All commits should not be done on the Master branch, especiall if:
* The commit hasn't been tested.
* The changes haven't been reviewed.
* A discussion about a change hasn't taken place.
* You THINK something is a good idea to tweak, but in fact completely changes the originality and hasn't been properly discussed.

# NOTE: GitLab is not your personal storage system. Do NOT commit libraries, photos, debugs, logs or files not necessary for developing. Once a file is committed it is never deleted. Do not take up unnecessary storage space.

## Committing, fixing issues and linkng ##
All commits should not be done on the Master branch, put the branch on a PR and:
* Label, title your PR.
* If you want to make clear that something is a WIP, put [WIP] in the PR title - no one can easily merge it.
* Give your PR a description, linking any issues related to it.
* Include 'fixes' # (issue number) if at all possible.

## Commit Messages ##
All commit messages should:
* Start with a capital letter.
* Never end in puncuation.
* Link to an issue if at all possible.
* Include 'fixes' # (issue number) if at all possible.
* Be in the present tense.
* Have a title less than 100 characters.
* End in a new line.

If a description is provided in the commit message, it should be separated from the title by a blank line. If the commit addresses an issue, its issue number should be referenced at the end of the commit message's description.

Whenever possible, commit messages should be prefixed with the directory name of which the commit modified the most, followed by a colon and a space.

For example: ```toon: ``` or ```tools: ``` or ```ai: ```

## Branch Naming ##
All branch names should:
* Be entirely lower case.
* Use **-** as a separator.
* Be categorized into one of the following groups:
    * wip
    * bugfix
    * test
    * enhancement
    * feature

For example: ```feature/parties``` or ```bugfix/toontorial``` or ```enhancement/fix-memory-leak```


Python Style Guidelines
=======================
For Python programming, we use a slightly modified version of the standard [PEP-8 Style Guide for Python Code](http://legacy.python.org/dev/peps/pep-0008 "PEP-8 Style Guide for Python Code"). Read below for our modifications.
- - -
## Code lay-out ##
### Indentation ###
The closing brace/bracket/parenthesis on multi-line constructs may either be directly at the end, as in:

    my_list = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        16, 17, 18, 19, 20]
    result = some_function_that_takes_arguments(
        'a', 'b', 'c', 'd', 'e', 'f')
        
or it may be by itself on the next line:

    my_list = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        16, 17, 18, 19, 20
    ]
    result = some_function_that_takes_arguments(
        'a', 'b', 'c', 'd', 'e', 'f'
    )

### Tabs or Spaces? ###
**_Always_** use spaces.

### Maximum Line Length ###
**Docstrings and comments** should be restricted to _80 characters_. Anything else should be limited to _100 characters_.

## Naming Conventions ##
### Variables ###
Intentionally **unused** variables should be named "**_**". This will make common IDEs and editors ignore it.

## Strings ##
### Quotations ###
Use single quotations _(')_ unless there is one inside the string, in which case use double quotations _(")_.
