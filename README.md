# Artificial Vision: Stereo Vision and Homography

## Overview

This project explores various aspects of stereo vision, including stereo calibration, simple stereo processing, uncalibrated stereo, and homography. The goal is to understand how depth information can be extracted from images and how geometric transformations are applied in real-world scenarios.

## Table of Contents

- [Theory](#theory)
  - [Stereo Calibration](#stereo-calibration)
  - [Simple Stereo](#simple-stereo)
  - [Uncalibrated Stereo](#uncalibrated-stereo)
  - [Homography](#homography)

## Theory

### Stereo Calibration

Stereo calibration is essential in obtaining the intrinsic and extrinsic parameters of a stereo camera system. This process involves capturing images of a known pattern (e.g., a chessboard) and using them to estimate:

- **Intrinsic parameters**: The focal length, optical centre, and distortion coefficients of each camera.
- **Extrinsic parameters**: The rotation and translation between the two cameras.

Once calibrated, rectification is applied to align the image planes, ensuring epipolar constraints are satisfied.

More in-depth theory in:
![Camera Calibration](CameraCalibration.md)

### Simple Stereo

Once the cameras are calibrated, stereo matching algorithms can be applied to estimate depth. This involves:

- Computing disparity maps using block matching or semi-global matching.
- Converting disparity to depth using the known baseline and focal length.
- Visualising depth maps for scene understanding.

### Uncalibrated Stereo

In cases where calibration is unavailable, uncalibrated stereo techniques rely on feature detection and matching to estimate the fundamental matrix. The key steps include:

- Extracting feature points using the SIFT Algorithm.
- Computing correspondences between stereo images.
- Estimating the fundamental and essential matrices to derive epipolar constraints.

More in-depth theory in:
![Uncalibrated Stereo](UncalibratedStereo.md)

### Homography

Homography is a transformation that relates two planar views of the same scene. It is widely used for:

- Image stitching
- Perspective correction
- Augmented reality applications

Homography is estimated using feature correspondences and RANSAC to remove outliers. Once obtained, it allows for the warping of images to align different perspectives.
