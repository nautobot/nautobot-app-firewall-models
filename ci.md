# Nautobot App CI Proposal

A proposal to improve GitHub based CI for Nautobot App development.

## Processes

Description of processes to be implemented. Bullets under `Trigger GitHub workflow ...` are automated GitHub workflow jobs and steps.

### Add Feature

Process of developing a new feature.

The idea is to run as simple as possible tests for each pull request commit, and all tests only once for merge commit.

- Locally run `invoke add-feature --issue <#issue>` to start developing a new feature. This task will:
    - Fetch the repository remote branches and tags.
    - Checkout and pull the latest `develop`.
    - Create a new feature branch `u/<user name>-<#issue>-<title>`.
        - Omit `#issue` if not related to any issue.
    - Add `towncrier` fragment.
    - Commit and push the feature branch.
    - Open a new pull request to `develop` branch.
- Implement the feature (assignee).
- Trigger GitHub workflow by pushing a commit to the feature branch.
    - Build the documentation using readthedocs.org.
    - Test `towncrier` fragment existence.
    - Run linters.
    - Run unit tests using latest `stable` Nautobot version, latest supported Python version and PostgreSQL.
- Review and approve the pull request (code owner).
- Squash and merge the pull requests (assignee).
- Trigger GitHub workflow by merging to `develop`.
    - [Fully test](#full-tests) the commit.
        - If full tests fail, trigger GitHub workflow to [fix failed merge](#fix-failed-merge).

#### How is this different from the current/existing CI workflow?

Here is an examples run, still WIP:

https://github.com/nautobot/nautobot-plugin-firewall-models/actions/runs/6470190422

- All linters run as a single job.
- Linters use the same docker image as unit tests, no need to install dependencies using poetry.
- Unit tests run only one test using latest `stable` Nautobot version, latest supported Python version and PostgreSQL.

Speedup against current solution is about 40 % and uses significantly fewer workers.

Docker caching is [explained here](#docker-caching).

### Bug Fix

The process is the same as [adding a new feature](#add-feature).

### Stable Release

To safely release a new stable version.

- Locally run `invoke release --version 'X.Y.Z' --ref <git reference> --push` to start the release process. This task will:
    - Fetch the repository remote branches and tags.
    - Pull the latest `develop` and `main`.
    - Fail if tag `vX.Y.Z` already exists.
    - Update `pyproject.toml` version to the version provided.
        - Implement some checking between the current vs provided versions.
    - Checkout and rebase `main` to the `--ref` argument value.
        - Default value is the latest `develop`.
        - Fail if provided git reference is not a descendant of `main` or `develop`.
    - Create changelog based on `towncrier` fragments.
    - Commit and push the `main` branch.
    - Open a new pull request to `develop` branch.
- Trigger GitHub workflow by pushing a commit to the release pull request.
    - [Fully test](#full-tests) the commit.
- Review and approve the pull request (code owner).
- Trigger GitHub workflow by approving the release pull request:
    - Check whether [full tests](#full-tests) for the commit passed.
    - Tag the commit `vX.Y.Z` and push the tag.
- Trigger GitHub workflow by pushing a tag:
    - Check whether [full tests](#full-tests) for the tagged commit passed.
        - The commit should be tagged in the previous step only if the tests passed, however, it is possible to tag the commit manually. This will verify it.
    - Build a package.
    - Create a new GitHub release.
- Trigger GitHub workflow by creating a GitHub release.
    - Release the package to PyPI.
    - Merge and close the release pull request. Do not squash to keep the release commit history.

When some step fails, it can be simply re-run.

### Pre Release

To be able to quickly release a new pre-release version.

Similar to [stable release](#stable-release), but:

- Locally run `invoke pre-release --version <version> --base <branch name> --push` to start the release process. This task will:
    - Increment the version if no `--version` argument is provided, e.g.:
        - `1.0.1` => `1.0.2-dev0`
        - `1.0.2-dev0` => `1.0.2-dev1`
        - An example implementation is [here](https://github.com/nautobot/cookiecutter-nautobot-app-drift-manager/blob/develop/tasks.py#L166).
    - Create a new `u/<username>-v<version>` branch from the current git reference.
    - Open a new pull request to the `--base` branch.
        - Use the current branch as the base branch if no `--base` argument is provided.
- Approval can be done by pull request author, if the base branch is not protected.
- Delete the release branch after successful release.

### Bug Fix LTM

Implement and merge bug fix to `develop` first, if the bug is present in both, stable and LTM releases.

- Locally run `invoke fix-ltm --ref <merge-commit-sha | #issue>` to start fixing LTM bug. This task will:
    - Fetch the repository remote branches and tags.
    - Checkout and pull the latest `ltm-1.6`.
    - Create a new branch `v/<user name>-<#issue>-<title>.
    - Increment the patch version in `pyproject.toml`.
    - Cherry-pick the commit from `develop` if provided by `--ref`.
        - Merge commit reference can be determined from #issue and vice versa.
    - Commit and push the branch.
    - Open a new pull request to `ltm-1.6` branch.
- If the bug is not present in stable release, implement and commit the bug fix (assignee).
- Trigger GitHub workflow by pushing a commit to the feature branch.
    - [Fully test](#full-tests) the commit.
- Review and approve the pull request (code owner).
- Squash and merge the pull requests (assignee).

### Back-port Feature to LTM

If allowed, process will be the same as [bug fix LTM](#bug-fix-ltm).

### LTM Release

To safely release a new LTM version.

Similar to [stable release](#stable-release), but:

- The invoke task is named `invoke release-ltm`.
    - `--version` argument is missing.
        - Increment version `patch` part only.
- Use `ltm-1.6` branch instead of `develop`.
- Use protected `ltm-1.6-main` branch (doesn't exist yet) instead of `main`.

Considerations:

- Align branch names:
    - Rename `ltm-1.6` => `ltm-1.6/develop`.
    - Rename `ltm-1.6-main` => `ltm-1.6/main`.
    - Use `ltm-1.6/u/...` for feature branches.
- Process can be automated for each [LTM bug fix](#bug-fix-ltm) to speed things up.

### Fix Failed Merge

It's rare but possible, that after the merge to the latest `develop`, something can get broken, even when tests on feature branch passes. E.g.: incompatibility between concurrent features.

When the full tests fail, the following steps will be done automatically by GitHub workflow:

- Create a new pull request with rollback commit.
- Re-open the feature pull request.
    - An option is to open a new issue instead.

It's up to the users to decide, whether to fix the failed merge or not.

## GitHub Actions

Define reusable actions to be used by workflows.

Actions `.yml` files can be stored in the following locations:

- `.github/actions` folder for each repository and managed by the Drift Manager.
- Some public shared repository (e.g. `cookiecutter-nautobot-app/` can be used after open-sourcing).

The following actions can be defined:

- Build Docker image for specific Python and Nautobot version.
- Run linters for specific Python and Nautobot version.
- Run unit tests for specific database type, Python and Nautobot version.
- Full tests as [described here](#full-tests).
- Build a package.
- Release a tag to GitHub.
- Release a package to PyPI.

### Full Tests

Action, that contains the following tests:

- Build the documentation using readthedocs.org.
- Python 3.11, Nautobot latest `stable` linters.
- Python 3.11, Nautobot latest `stable`, PostgreSQL unit tests.
- Python 3.11, Nautobot latest `stable`, MySQL unit tests.
- Python 3.11, Nautobot `2.0.0`, PostgreSQL unit tests.
- Python 3.8, Nautobot latest `stable`, PostgreSQL unit tests.

Jobs will run in parallel and re-use cached Docker layers and [database dumps](#database-caching).

## Docker Caching

When testing the single Nautobot and Python version the cache is much less utilized.

- Currently, the limit is 10 G per repository. Each Nautobot/Python combination uses almost 1 GB. That means, multiple concurrent PRs can often purge others cache.
- For full tests, caching will be disabled.

Better define `.gitignore` file to avoid unnecessary context changes.

- Deny everything first.
- Allow particular files/directories necessary for build.

## Database Caching

Cache and re-use empty migrated database dumps to avoid migrations using GitHub actions cache.

GitHub `unittest` action will first check, whether there is cached dump.

- If so, apply that dump.
- If not, run migrations, create a new dump, and cache that dump.

Unit tests will be run with `--keepdb` flag to avoid re-creating the database.

Calculate cache key as a hash of:

- `migrations` folder file content.
- Nautobot version.
- Database server Docker image reference.

This should speed up unit tests significantly.

## Future Improvements

- Add E2E Selenium tests.
- Add E2E external integrations tests.
- Factory dumps caching similar to Nautobot core.

## Questions

- [ ] What is preferred in GitHub workflows, to fail fast or finish fast?
