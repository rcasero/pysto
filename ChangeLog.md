# ChangeLog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## vx.x.x

## Changed
- Move bash scripts to new tools directory.
- imgproc.imfuse(): Add warning if both images don't have the same
  pixel type, because in that case, they produce visualisation
  artifacts.
- README.md: Simplify and rewrite notes for users vs. developers.

## v1.4.1

## Changed
- imgprocITK.imshow(): Fix bug. When origin='lower', the image will be
  upside down, so we need to take that into account for the vertical
  axis

## v1.4.0

### Added
- imgprocITK.TypicalBorderIntensity(): Compute the typical values at
  the boundaries of SimpleITK Images or np.arrays

## v1.3.4

### Changed
- Makefile: fix bugs, missing test targets
- Makefile: error with README.rst rule when README.md hasn't been edited
- imgprocITK.imshow(): fix bug, wrong indirection level passing kwargs to plt.imshow().
- test_imshow.py: add kwargs argument, so that it gets tested.

## v1.3.3

### Changed
- Allow developer to install the SimpleITK dependency either as
  official SimpleITK package or build and install SimpleElastix.

## v1.3.2

### Changed
- README.md: increase code block tab by 1 so that it translates
  correctly into PyPI HTML.

## v1.3.1

- minor

## v1.3.0

### Added
- imgprocITK.imshow(): matplotlib.imshow extended for the ITK Image class.
- module imgprocITK for functions that depend on SimpleITK.

### Changed
- Clarify help header of block_split().
- In setup.py, link long_description to README.md.

## v1.2.0

### Added
- improc.block_stack(): Stack a list of blocks to reassemble the
  original array. This function is the opposite of block_split().
- Makefile: Simplify common development tasks (test, package).

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
