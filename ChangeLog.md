# ChangeLog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## v1.1.3
### Changed

- __init__: Fix bug, missing encoding for file.
- tests/*.py: Fix bug, typo in directory for data.
- pysto/improc.py: Fix bug. np.divide in Python 2 is integer division
- Make compatible and add local environment for python 2.7.

## v1.1.2
### Changed

- setup.py: Improve metainformation.

## v1.1.1
### Changed

- ChangeLog.md: Update ChangeLog.

## v1.1.0
### Added

- imgproc.block_split(): "Split an nd-array into blocks".

## v1.0.0
### Added

- imgproc.matchHist(): "Modify image intensities to match the
  histogram of a reference image" by
  [rcasero](https://github.com/rcasero)
- imgproc.imfuse(): "Composite of two images" by
  [rcasero](https://github.com/rcasero)
- testdata/*.png: Stereo cloud images with ROI masks (left_mask.png,
  left.png, right_mask.png, right.png) by
  [rcasero](https://github.com/rcasero)
