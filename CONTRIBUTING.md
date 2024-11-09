# Contributing back

Thank you very much for noticing this little project and helping me make it better!

Though I created this project because I needed it for a specific project's documentation
suite, it is free to use by anyone that thinks it is useful and is also free to modify.
I'm more than willing to accept contributions as well. Here are a few ways that you can
help:

* Create an issue if you have a question
* Create an issue if you find a defect
* Submit pull requests to update documentation (including fixing typos)
* Submit pull requests to update dependencies, add tests, or anything else

## Creating issues

If you have a question about something or found a defect, create a new issue in GitHub.
If you have a question, then someone else probably has the same thought so please ask.
There are no stupid questions. Do look at the closed issues as well since someone else
may have already noticed the issue.

If you are creating an issue for a defect, please include a [Minimal, Reproducible Example]
that demonstrates the problem. I am less likely to look at an issue that is lacking an
example unless it is facepalmingly obvious.

[Minimal, Reproducible Example]: https://stackoverflow.com/help/minimal-reproducible-example

## Submitting a pull request

This project uses [hatch] for project management and [ruff] for the vast majority of
style and formatting tasks. I also use [pre-commit] to keep source code inline every
time that I commit... it makes life so much easier. The easiest way to get started is
to install the hatch and pre-commit utilities. You can do this in a virtual environments
or into your Python interpreters user directory. I find the latter easier but your
mileage may vary.

```shell
python3 -m pip install --user hatch
hatch run ci
```

Running the "ci" script will create an environment somewhere for you to use. No need
to worry about _where_ this lives for the time being -- you will use `hatch shell` to
spawn a shell with the environment activated. I highly recommend installing the pre-commit
hook so that you don't have to think much about formatting and linting.

```
$ hatch shell
(pymdown-ietflinks) $ pre-commit install --install-hooks
pre-commit installed at .git/hooks/pre-commit
```

Now you are set up to make changes. Once you are ready to contribute back, push your
work up to your fork and create a new Pull Request in GitHub. THere are a few things that
I require though...

1. all tests must pass before I'll merge
2. add entries to CHANGELOG.md
3. update any related documentation
4. add yourself to AUTHORS.md _if you want to make your contribution visible_

These are all required **before** the request is merged. Feel free to submit the pull
request when you are ready. I can help with tests if you are having trouble getting them
to pass or add documentation if you are not comfortable writing it. Please "@" mention
me if you need help with anything.

[hatch]: https://hatch.pypa.io/latest/
[pre-commit]: https://pre-commit.com
[ruff]: https://astral.sh/ruff
