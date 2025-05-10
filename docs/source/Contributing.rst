Commit Message Guidelines
=========================

Commit messages are crucial for maintaining an organized and understandable project history. They also serve as the foundation for tools like changelogs, build systems, and versioning.

This guide outlines how to structure your commit messages to improve readability and ensure consistency across projects, while also supporting automated tools like changelog generation, semantic versioning, and more.

.. note::

   This guide is NOT only for YOU. It is just FOR ME.

---

Commit Message Format
---------------------

Each commit message should have the following structure::

   <type>(<scope>): <subject>
   
   <BLANK LINE>
   <body>
   <BLANK LINE>
   <footer>

- **Type**: A required part of the message that defines the nature of the change.
- **Scope**: An optional field that specifies the part of the project the change impacts.
- **Subject**: A short summary of the change, limited to 50 characters.

**Type** and **subject** are mandatory; the **scope** is optional.

Header
~~~~~~

The header is the first line and includes the **type**, an optional **scope**, and a **subject**. It’s crucial to ensure the header is concise, follows the format, and doesn’t exceed 50 characters.

**Example**::

   fix(database): resolve connection issue

Body
~~~~

The body provides a more detailed explanation of the change, including the rationale and context. Like the subject, it should use the **imperative mood** (e.g., "fix" instead of "fixed"). It should begin one blank line after the header.

**Example**::

   fix: prevent racing of requests

   Introduce a request id and dismiss incoming responses other than from the latest request.
   Remove obsolete timeouts.

Footer
~~~~~~

The footer is used for additional information like references to related issues or breaking changes. Any breaking changes should be prefixed with ``BREAKING CHANGE:``.

**Example**::

   BREAKING CHANGE: The method `getData` has been replaced by `fetchData`.

Revert
~~~~~~

If the commit reverts a previous change, prepend ``revert:`` in the header. The body should state: ``This reverts commit <hash>``, where the hash is the SHA of the reverted commit.

---

Conventional Commits Specification
----------------------------------

The Conventional Commits format defines a structured and consistent approach to commit messages, integrating well with tools that follow `SemVer <http://semver.org>`_. It includes specific guidelines for **types**, **scopes**, and handling **breaking changes**.

Type
~~~~

The commit **type** communicates the nature of the change. Some examples of standard types are:

- **build**: Changes that affect the build system or external dependencies.
- **ci**: Continuous Integration changes (e.g., GitHub Actions or Jenkins configurations).
- **docs**: Documentation-only changes.
- **feat**: A new feature (this correlates with a ``MINOR`` version bump in Semantic Versioning).
- **fix**: A bug fix (this correlates with a ``PATCH`` in Semantic Versioning).
- **perf**: A code change that improves performance.
- **refactor**: Code changes that neither fix a bug nor add a feature.
- **style**: Code style changes (e.g., formatting, missing semicolons).
- **test**: Adding or modifying tests.

**Example**::

   feat(api): add new authentication method

Scope
~~~~~

The **scope** provides additional context by specifying the part of the codebase the change affects. For example:

- **database**
- **auth**
- **api**
- **model**

This is optional but recommended for clarity. You may also use general scopes like ``changelog``, or leave it blank for project-wide changes.

Subject
~~~~~~~

The **subject** line should:

- Use the **imperative mood** ("fix", "add", "change").
- Avoid capitalizing the first letter.
- Not end with a period.
- Be concise but informative (limited to 50 characters).

Breaking Changes
~~~~~~~~~~~~~~~~

To indicate a **breaking change**, you have two options:

1. Append a ``!`` after the type or scope in the header.
2. Add a ``BREAKING CHANGE:`` note in the footer.

**Example**::

   feat!: drop support for Node 6

   BREAKING CHANGE: JavaScript features incompatible with Node 6 are now used.

Footer and Issue References
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the **footer**, you can reference issues or PRs the commit closes using:

- ``Fixes #<issue_number>``
- ``Closes #<issue_number>``

---

Examples
--------

Commit with a breaking change and a footer::

   feat(api)!: send an email when a product is shipped

   BREAKING CHANGE: Order confirmation emails are now sent automatically.

Commit with no body::

   docs: fix typo in the README

Commit with multiple footers::

   fix: resolve issue with multiple API requests

   Reviewed-by: Jane Doe
   Closes #456

Revert commit::

   revert: let us never again speak of the noodle incident

   This reverts commit 676104e.

---

Why Use This Format?
--------------------

1. **Structured commit history**: Makes the project’s history more readable and easier to navigate.
2. **Automated changelog generation**: Facilitates automatic changelog creation from commit messages.
3. **Semantic versioning**: The commit types correlate directly with versioning changes (``MAJOR``, ``MINOR``, ``PATCH``).
4. **Tooling compatibility**: Integrates seamlessly with tools like commitlint and release automation.

---

FAQ
---

What if I accidentally use the wrong type?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you notice the mistake before release, you can correct the history with ``git rebase``. If the commit has been released, leave it as is and correct it moving forward.

How does this relate to SemVer?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **fix** -> ``PATCH`` version bump
- **feat** -> ``MINOR`` version bump
- **BREAKING CHANGE** -> ``MAJOR`` version bump
