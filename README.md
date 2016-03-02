# Tests for Mozilla's Marketplace
This repository contains tests for [Mozilla's Marketplace](https://marketplace.firefox.com/).

[![license](https://img.shields.io/badge/license-MPL%202.0-blue.svg)](https://github.com/mozilla/marketplace-tests/blob/master/LICENSE)
[![travis](https://img.shields.io/travis/mozilla/marketplace-tests.svg?label=travis)](http://travis-ci.org/mozilla/marketplace-tests/)
[![dev](https://img.shields.io/jenkins/s/https/webqa-ci.mozilla.com/marketplace.dev.svg?label=dev)](https://webqa-ci.mozilla.com/job/marketplace.dev/)
[![stage](https://img.shields.io/jenkins/s/https/webqa-ci.mozilla.com/marketplace.stage.saucelabs.svg?label=stage)](https://webqa-ci.mozilla.com/job/marketplace.stage.saucelabs/)
[![prod](https://img.shields.io/jenkins/s/https/webqa-ci.mozilla.com/marketplace.prod.svg?label=prod)](https://webqa-ci.mozilla.com/job/marketplace.prod/)
[![requirements](https://img.shields.io/requires/github/mozilla/marketplace-tests.svg)](https://requires.io/github/mozilla/marketplace-tests/requirements/?branch=master)

## Getting involved
We love working with contributors to fill out the test coverage for Marketplace,
but it does require a few skills. By contributing to our test suite you will
have an opportunity to learn and/or improve your skills with Python, Selenium
WebDriver, GitHub, virtual environments, the Page Object Model, and more.

For some resources for learning about these technologies, take a look at our
documentation on [running Web QA automated tests][running-tests].

All of [these awesome contributors][contributors] have opened pull requests against this
repository.

## Questions are always welcome
While we take pains to keep our documentation updated, the best source of
information is those of us who work on the project. Don't be afraid to join us
in irc.mozilla.org [#mozwebqa][irc] to ask questions about our tests. We also
have a [mailing list][list] available that you are welcome to join and post to.

## How to run the tests locally
We maintain a [detailed guide][running-tests] to running our automated tests.
However, if you want to get started quickly, you can try following the steps
below:

### Clone the repository
If you have cloned this project already then you can skip this, otherwise you'll
need to clone this repo using Git. If you do not know how to clone a GitHub
repository, check out this [help page][git-clone] from GitHub.

If you think you would like to contribute to the tests by writing or maintaining
them in the future, it would be a good idea to create a fork of this repository
first, and then clone that. GitHub also has great documentation for
[forking a repository][git-fork].

### Create or activate a Python virtual environment
You should install this project's dependencies (which is described in the next
step) into a virtual environment in order to avoid impacting the rest of your
system, and to make problem solving easier. If you already have a virtual
environment for these tests, then you should activate it, otherwise you should
create a new one. For more information on working with virtual environments see
our [summary][virtualenv].

### Install dependencies
Install the Python packages that are needed to run our tests using pip. In a
terminal, from the the project root, issue the following command:

```bash
$ pip install -Ur requirements.txt
```

### Create a variables file
Some of the tests in this repository need sensitive credentials. We store these
in a JSON file, which we then pass to the tests via the command line. If you
want to be able to run any of those tests, you will need to create a variables
file containing your own credentials. The following is an example JSON file with
the values missing. You can use this as a template.

```json
{
  "users": {
    "default": {
      "email": "",
      "password": "",
      "name": "",
      "api": {
        "marketplace-dev.allizom.org": {
          "key": "",
          "secret": ""
        },
        "marketplace.allizom.org": {
          "key": "",
          "secret": ""
        }
      }
    }
  }
}
```

You will then pass the name of that your variables file on the command line.
For the purposes of the examples below, assume you named your copy of the file
`my_variables.json`.

### Run the tests
Tests are run using the command line. Below are a couple of examples of running
the tests:

To run all of the desktop tests against the default environment:

```bash
$ py.test --driver Firefox --variables my_variables.json tests/desktop
```

To run against a different environment, pass in a value for `--base-url`, like so:

```bash
$ py.test --base-url https://marketplace.allizom.org --driver Firefox --variables my_variables.json tests/desktop
```

The pytest plugin that we use for running tests has a number of advanced
command line options available. To see the options available, run
`py.test --help`. The full documentation for the plugin can be found
[here][pytest-selenium].

[contributors]: https://github.com/mozilla/Addon-Tests/contributors
[git-clone]: https://help.github.com/articles/cloning-a-repository/
[git-fork]: https://help.github.com/articles/fork-a-repo/
[irc]: http://widget01.mibbit.com/?settings=1b10107157e79b08f2bf99a11f521973&server=irc.mozilla.org&channel=%23mozwebqa
[list]: https://mail.mozilla.org/listinfo/mozwebqa
[pytest-selenium]: https://github.com/davehunt/pytest-selenium
[running-tests]: https://developer.mozilla.org/en-US/docs/Mozilla/QA/Running_Web_QA_automated_tests
[virtualenv]: https://wiki.mozilla.org/QA/Execution/Web_Testing/Automation/Virtual_Environments
