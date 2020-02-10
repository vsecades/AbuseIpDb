# Contributing

Any contributions are welcome.  It doesn't matter, if it is a code contribution
or a feature request.  As we're managing this package in our spare time please
understand, that we will add features without code as we've time.

# Developing

Please fork the repository and make your changes in a separate branch.
Give this branch a meaningful name, as it will show up in the *network* of the
*insights* tab.  Base your branch either on `master` or on `development`.
Branching from `development` is preferred.

For new functionality we expect automated tests.  The tests should cover all
added code.  If something can't be tested, please add an inline comment to that
code indicating this.  We will pay more attention to it during review.

If you've no experience writing tests, look at the existing ones.  Don't
hesitate to ask for help.  We're happy to pass on knowledge.

All tests, coverage and linting must pass.  Please do not create a pull request
before.  You can see the status of all supported environments in the *Actions*
tab of your fork.  

If you want to run test etc. locally, you will need to have `coverage`,
`flake8`, `isort`, `pytest` and `tox` installed in your environment.
See `tox.ini` for a full list of dependencies.  

# Documentation

Please don't forget to update the documentation, if needed.  There are several
levels of documentation.

 * All `*.md` files (like this one) contains high level usage description.
   The audience consists of programmers, system adminstrators and contributors.
 * Any docstring describes what the module, class or method is intendend to do.
   If necessary it should reference additional documentation, like the API
   documentation on AbuseIPDB.  Adding docstring is currently optional.
   The audience consists of programmers.
 * Inline comments are hints to other programmers, why you implemented
   something in a certain way, if it isn't obvious.  This should help future
   developers to understand the code.  This could also be a note to the reviewer
   about the ability of test coverage.  The audience consists of programmers
   and reviewers.

Please use American English spelling.

# Pull requests

When you're finished, create a pull request against `vsecades/development`.
Please describe your change and give any necessary references in your
description.

Changing the version number is done in `vsecades/development`.

# Versioning

We use a classical *major.minor.patch* versioning pattern with the following
meaning:

 * *major* changes, if
    * there is a breaking API change or
    * the package supports a new API version.
 * *minor* changes, if there is some new functionality not covered by the
   changes listed for changes of the *major* version number.
 * *patch* level changes for any change, that isn't covered above.  This could
   e.g. be an enhancement on the documentation or infrastructure.

Any lower level is set zo zero, if any higher level is increased.
