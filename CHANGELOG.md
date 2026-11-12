# Changelog

The releases this repository pins, newest first, in the form of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
A pin move is recorded here, not in decisions/.

## Unreleased

### Added

- `skills/gather-data/SKILL.md`, the baseline as a skill an agent loads before it searches. It logs every result,
  leaves a string after 5 results with no new concept, and stops when the estimator says so. Agents of other
  repositories link this one place instead of restating the rules.
- `stopping_estimator.py --unlisted-as-concept` and `unlisted_as_concept` in `checks/config.toml`, off by default: a
  result with no listed concept counts as one concept of its own, seen once (issue #1).

## [0.1.0] - 2026-11-04

### Changed

- Pinned reader-ergonomics v1.21.0 (`2e5b6f0`), from v1.20.0 (`4f99372`): duplication skips the lines a declared shape prescribes
- Tag v0.1.0 and a GitHub release of the same name.

## 2026-11-03

### Added

- Pinned reader-ergonomics v1.20.0 (`4f99372`), at the repository's start: the standard's pin, link, changelog and
  decision-record checks, which this skeleton is written to pass.
