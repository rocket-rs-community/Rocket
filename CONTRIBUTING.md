# Contributing to Rocket

**Please read this document before contributing!**

Thank you for contributing! We welcome your contributions in whichever form they
may come.

This document provides guidelines and resources to help you successfully
contribute to the project. Rocket is a tool designed to push the envelope of
usability, security, _and_ performance in web frameworks, and accordingly, our
quality standards are high. To make the best use of everyone's time and avoid
wasted efforts, take a moment to understand our expectations and conventions
outlined here.

## Submitting Pull Requests

Before creating a new pull request:

  * Read and understand [Code Style Conventions], [Commit Message Guidelines],
    and [Testing].
  * If you're resolving an open issue, follow [Resolving an Open Issue].
  * If you're implementing new functionality, check whether the functionality
    you're implementing has been proposed before, either as an [issue] or [pull
    request]. Ensure your PR resolves any previously raised concerns. Then,
    follow [Implementing an Unproposed Feature].
  * For everything else, see [Other Common Contributions].

We aim to keep Rocket's code quality at the highest level. This means that any
code you contribute must be:

  * **Commented:** Complex or subtle functionality must be properly commented.
  * **Documented:** Public items must have doc comments with examples.
  * **Styled:** ~~Your code must follow the [Code Style Conventions].~~ Your code must be formatted with the cargo fmt tool. (Community Fork)
  * **Simple:** Your code should accomplish its task as simply and
    idiomatically as possible.
  * **Tested:** You must write (and pass) convincing [tests](#testing) for all
    new or changed functionality.
  * **Focused:** Your code should do what it's supposed to and nothing more.

### Resolving an Open Issue
[Resolving an Open Issue]: #resolving-an-open-issue

If you spot an open issue that you'd like to resolve:

  1. **First identify if there's a proposed solution to the problem.**

     If there is, proceed to step 2. If there isn't, your first course of
     action, before writing any code, is to propose a solution. To do so, leave
     a comment describing your solution in the relevant issue. It's especially
     useful to see test cases and hypothetical examples. This step is critical:
     it allows us to identify and resolve concerns with a proposed solution
     before anyone spends time writing code. It may also allow us to point you
     in more efficient implementation directions.

  2. **Write a failing test case you expect to pass after resolving the issue.**

     If you can write proper tests cases that fail, do so (see [Testing]). If
     you cannot, for instance because you're introducing new APIs which can't be
     used until they exist, write a test case that mocks usage of those APIs. In
     either case, allow the tests and mock examples to guide your progress.

  3. **Write basic functionality, pass tests, and submit a PR.**

     Think about edge cases to the problem and ensure you have tests for those
     edge cases. Once your implementation is functionally complete, submit a PR.
     Don't spend time writing or changing a bunch of documentation just yet.

  4. **Wait for a review, iterate, and polish.**

     If a review doesn't come in a few days, feel free to ping a maintainer.
     Once someone reviews your PR, integrate their feedback. If the PR solves the
     issue (which it should because you have passing tests) and fits the project
     (which it should since you sought feedback _before_ submitting), it will be
     _conditionally_ approved pending final polish: documentation (rustdocs,
     guide docs), style improvements, and testing. Your PR will then be merged.

### Implementing an Unproposed Feature
[Implementing an Unproposed Feature]: #implementing-an-unproposed-feature

First and foremost, **please do not submit a PR that implements a new feature
without first proposing a design and seeking feedback.** We take the addition of
new features _very_ seriously because they directly impact usability.

To propose a new feature, create a [new feature request issue] and follow the
template. Note that certain classes of features require particularly compelling
justification to be taken into consideration. These include features that:

  * Can be implemented outside of Rocket.
  * Introduce new dependencies, especially heavier ones.
  * Only exist to add support for an external crate.
  * Are too specific to one use-case.
  * Are overtly complex _and_ have "simple" workarounds.
  * Only partially solve a bigger deficiency.

Once your feature request is accepted, follow [Resolving an Open Issue].

[new feature request issue]: https://github.com/rwf2/Rocket/issues/new?assignees=&labels=request&projects=&template=feature-request.yml

### Other Common Contributions
[Other Common Contributions]: #other-common-contributions

  * **Doc fixes, typos, wording improvements.**

    We encourage any of these! Just a submit a PR with your changes. Please
    preserve the surrounding markdown formatting as much as possible. This
    typically means keeping lines under 80 characters, keeping table delimiters
    aligned, and preserving indentation accordingly.

    The guide's source files are at [docs/guide]. Note the following special
    syntax available in guide markdown:

    - **Cross-linking** pages is accomplished via relative links. Outside
      of the index, this is: `../{page}#anchor`. For instance, to link to
      **Quickstart > Running Examples**, use `../quickstart#running-examples`.
    - **Aliases** are shorthand URLs that start with `@` (e.g, `@api`). They are
      used throughout the guide to simplify creating versioned URLs. They are
      replaced at build time with the appropriate versioned instance.

  * **New examples or changes to existing ones.**

    Please follow the [Implementing an Unproposed Feature] process.

  * **Formatting or other purely cosmetic changes.**

    We generally do not accept purely cosmetic changes to the codebase such as
    style or formatting changes. All PRs must add something substantial to
    Rocket's functionality, coherence, testing, performance, usability, bug
    fixes, security, documentation, or overall maintainability.

  * **Advertisements of any nature.**

    We do not accept any contributions that resemble advertisements or
    promotional content. If you are interested in supporting Rocket, we
    encourage you to [sponsor the project].

## Testing
[Testing]: #testing

All testing happens through [test.sh]. Before submitting a PR, run the script
and fix any issues. The default mode (passing no arguments or `--default`) will
usually suffice, but you may also wish to execute additional tests. In
particular:

  * If you make changes to `contrib`: `test.sh --contrib`
  * If you make user-facing API changes or update deps: `test.sh --examples`
  * If you add or modify feature flags: `test.sh --core`
  * If you modify codegen: see [UI Tests].

Run `test.sh --help` to get an overview of how to execute the script:

```sh
USAGE:
  ./scripts/test.sh [+<TOOLCHAIN>] [--help|-h] [--<TEST>]

OPTIONS:
  +<TOOLCHAIN>   Forwarded to Cargo to select toolchain.
  --help, -h     Print this help message and exit.
  --<TEST>       Run the specified test suite.
                 (Run without --<TEST> to run default tests.)

AVAILABLE <TEST> OPTIONS:
  default
  all
  core
  contrib
  examples
  benchmarks
  testbench
  ui

EXAMPLES:
  ./scripts/test.sh                     # Run default tests on current toolchain.
  ./scripts/test.sh +stable --all       # Run all tests on stable toolchain.
  ./scripts/test.sh --ui                # Run UI tests on current toolchain.
```

### Writing Tests

Rocket is tested in a variety of ways. This includes via Rust's regular testing
facilities such as doctests, unit tests, and integration tests, as well Rocket's
examples, testbench, and [UI Tests]:

  - **Examples**: The [`examples`](examples/) directory contains applications
    that make use of many of Rocket's features. Each example is integration
    tested using Rocket's built-in [local testing]. This both ensures that
    typical Rocket code continues to work as expected and serves as a way to
    detect and resolve user-facing breaking changes.

  - **Testbench**: Rocket's [testbench](testbench/) tests end-to-end server or
    protocol properties by starting up full Rocket servers to which it
    dispatches real HTTP requests. Each server is independently written in
    [testbench/src/servers/](testbench/src/servers/). You're unlikely to need to
    write a testbench test unless you're modifying low-level details.

  - **UI Tests**: UI tests ensure Rocket's codegen produces meaningful compiler
    diagnostics. They compile Rocket applications and compare the compiler's
    output to expected results. If you're changing codegen, you'll need to
    update or create UI tests. See [UI Tests] for details.

For any change that affects functionality, we ask that you write a test that
verifies that functionality. Minimally, this means a unit test, doctest,
integration test, or some combination of these. For small changes, unit tests
will likely suffice. If the change affects the user in any way, then doctests
should be added or modified. And if the change requires using unrelated APIs to
test, then an integration test should be added.

Additionally, the following scenarios require special attention:

  - **Improved Features**

    Modifying an existing example is a great place to write tests for improved
    features. If you do modify an example, make sure you modify the README in
    the example directory, too.

  - **New Features**

    For major features, introducing a new example that showcases idiomatic use
    of the feature can be useful. Make sure you modify the README in the
    `examples` directory if you do. In addition, all newly introduced public
    APIs should be fully documented and include doctests as well as unit and
    integration tests.

  - **Fixing a Bug**

    To avoid regressions, _always_ introduce or modify an integration or
    testbench test for a bugfix. Integration tests should live in the usual
    `tests/` directory and be named `short-issue-description-NNNN.rs`, where
    `NNNN` is the GitHub issue number for the bug. For example,
    `forward-includes-status-1560.rs`.

[local testing]: https://api.rocket.rs/master/rocket/local/

### UI Tests
[UI Tests]: #ui-tests

Changes to codegen (i.e, `rocket_codegen` and other `_codegen` crates)
necessitate adding and running UI tests, which capture compiler output and
compare it against some expected output. UI tests use [`trybuild`].

Tests can be found in the `codegen/tests/ui-fail` directories of respective
`codegen` crates. Each test is symlinked into sibling `ui-fail-stable` and
`ui-fail-nightly` directories, which also contain the expected error output for
stable and nightly compilers, respectively. For example:

```
./core/codegen/tests
├── ui-fail
│   ├── async-entry.rs
│   ├── ...
│   └── uri_display_type_errors.rs
├── ui-fail-nightly
│   ├── async-entry.rs -> ../ui-fail/async-entry.rs
│   ├── async-entry.stderr
│   ├── ...
│   ├── uri_display_type_errors.rs -> ../ui-fail/uri_display_type_errors.rs
│   └── uri_display_type_errors.stderr
└── ui-fail-stable
    ├── async-entry.rs -> ../ui-fail/async-entry.rs
    ├── async-entry.stderr
    ├── ...
    ├── uri_display_type_errors.rs -> ../ui-fail/uri_display_type_errors.rs
    └── uri_display_type_errors.stderr
```

If you make changes to codegen, run the UI tests for stable and nightly with
`test.sh +stable --ui` and `test.sh +nightly --ui`. If there are failures,
update the outputs with `TRYBUILD=overwrite test.sh +nightly --ui` and
`TRYBUILD=overwrite test.sh +stable --ui`. Look at the diff to see what's
changed. Ensure that error messages properly attribute (i.e., visually underline
or point to) the source of the error. For example, if a type need to implement a
trait, then that type should be underlined. We strive to emit the most helpful
and descriptive error messages possible.

### API Docs

If you make changes to documentation, you should build the API docs and verify
that your changes look as you expect. API documentation is built with
[mk-docs.sh] and output to the usual `target/docs` directory. By default, the
script will `clean` any existing docs to avoid potential caching issues. To
override this behavior, use `mk-docs.sh -d`.

## Code Style Conventions
[Code Style Conventions]: #code-style-conventions

Please use `cargo fmt` to format all contributions.

## Licensing

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in Rocket by you shall be dual licensed under the MIT License and
Apache License, Version 2.0, without any additional terms or conditions.


> [!IMPORTANT]
> This is a community fork of the Rocket.rs project, contributions to this fork
> may be incorporated into the original project in line with the permissions
> conveyed in the dual license.

The Rocket website docs are licensed under [separate terms](docs/LICENSE). Any
contribution intentionally submitted for inclusion in the Rocket website docs by
you shall be licensed under those terms.
