# packgen

`packgen` is a tool that generates a packing of particles for various purposes. The primary goal is to generate an STL file with a mesh of the packing.

Currently, only hexagonal particles are implemented. In addition, there is no configurability.

## Installation

Install this project with `pip` or `uv pip`:

```shell
pip install git+https://github.com/cmt-dtu-energy/packgen@0.1.0
```

Upon installation, the command `packgen` becomes available in the current environment;
runnint it opens the [Blender][blender] software with the packing simulation set up, but 
before it is run.

[blender]: https://www.blender.org/
