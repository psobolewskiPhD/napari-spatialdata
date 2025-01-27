# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog][],
and this project adheres to [Semantic Versioning][].

[keep a changelog]: https://keepachangelog.com/en/1.0.0/
[semantic versioning]: https://semver.org/spec/v2.0.0.html

## [0.2.8] - tbd

## [0.2.7] - 2023-10-02

### Added

- Multiple SpatialData objects support (ported from the "spatialdata" branch)
- Interactive is more ergonomic, has a headless parameter, can be used to display pre-configured elements
- Remembering user layer visibility settings when changing coordinate system

### Fixed

- Fixes in CLI
- Several internal bugfixes and code refactorings
- Fixes in updating affine transformation when changing coordinate system

## [0.2.6] - 2023-07-13

### Fixed

- Wrong tag preventing the release to pip (the previous tag was not of a commit merged to main).

## [0.2.5] - 2023-07-13

### Fixed

- CLI @berombau @LucaMarconato
- Display of points and circles @LucaMarconato
- Issue with name reinitialization @tothmarcella
- Reverted to use PyQt5 @melonora
- RGB/RGBA correctly displayed for 3/4 channel images @rahulbshrestha
- Layer visibility changes when changing coordinate system @melonora
- Performance with multiscale images @LucaMarconato
- Refactored internal code to prepare for future refactoring @melonora

### Thanks

- Reviewers @giovp @timtreis @kevinyamauchi and the users that reported bugs.

## [0.2.4] - 2023-05-23

### Added

- Color circles and polygons with annotations (#73)

## [0.2.3] - 2023-05-11

### Fixed

- Shapes support

## [0.2.1] - 2023-05-04

### Fixed

- Package versioning (#63)

## [0.2.0] - 2023-05-04

### Merged

- Merge pull request #62 from scverse/kevinyamauchi-patch-1 - Install spatialdata from pypi
