<!-- This file is a placeholder for customizing description of your plugin 
on the napari hub if you wish. The readme file will be used by default if
you wish not to do any customization for the napari hub listing.

If you need some help writing a good description, check out our 
[guide](https://github.com/chanzuckerberg/napari-hub/wiki/Writing-the-Perfect-Description-for-your-Plugin)
-->
CAREamics is a PyTorch library aimed at simplifying the use of Noise2Void and its many
variants and cousins (CARE, Noise2Noise, N2V2, P(P)N2V, HDN, muSplit etc.).

## Why CAREamics?

Noise2Void is a widely used denoising algorithm, and is readily available from the `n2v`
python package. However, `n2v` is based on TensorFlow, while more recent methods
denoising methods (PPN2V, DivNoising, HDN) are all implemented in PyTorch, but are
lacking the extra features that would make them usable by the community.

The aim of CAREamics is to provide a PyTorch library reuniting all the latest methods
in one package, while providing a simple and consistent API. The library relies on
PyTorch Lightning as a back-end. In addition, we will provide extensive documentation and
tutorials on how to best apply these methods in a scientific context.

## Installation and use

Check out the [documentation](https://careamics.github.io/) for installation instructions and guides!
