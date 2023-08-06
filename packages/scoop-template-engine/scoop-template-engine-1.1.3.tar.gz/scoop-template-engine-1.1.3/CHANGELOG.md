# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.3] - 2023-06-23
### Changed
- Allow out-of-directory compilation with custom `.bib` files, e.g., using `latexmk -pdf -outdir=build manuscript-pamm.tex`.

## [1.1.2] - 2023-06-23
### Fixed
- Unexpanded `\detokenize` commands in custom `.bib` files.

## [1.1.1] - 2023-04-30
### Changed
- Review and amend documentation.

## [1.1.0] - 2023-04-29
### Added
- Add `orcid:` key to `authors:`.
### Changed
- Implement `--protectfamilynames` switch into `spbf`.

## [1.0.4] - 2023-04-01
### Changed
- Update `Centre Mersenne/ojmo` resources.

## [1.0.3] - 2023-04-01
### Changed
- Update `Springer/sn-jnl.cls` resources.
### Fixed
- Use `wget` to retrieve SIAM style guides.

## [1.0.2] - 2023-03-07
### Fixed
- Fix version detection in `utilities.py`.

## [1.0.1] - 2023-03-07
### Changed
- Use `wget` to retrieve SIAM resources.

## [1.0.0] - 2023-03-07
### Added 
- Initial production release with support of 377 scientific journals.
