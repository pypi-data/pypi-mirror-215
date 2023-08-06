<!-- #region -->
# FDTD Meep gratings

[Meep](https://meep.readthedocs.io/en/latest/) can also compute grating coupler Sparameters and far field.


## grating sparameters

```bash

                fiber_xposition
                     |
                fiber_core_diameter
             /     /  /     /       |
            /     /  /     /        | fiber_thickness
           /     /  /     /    _ _ _| _ _ _ _ _ _  _
                                    |
                                    | air_gap_thickness
                               _ _ _| _ _ _ _ _ _  _
                                    |
                   clad_material            | top_clad_thickness
                               _ _ _| _ _ _ _ _ _  _
                _|-|_|-|_|-|___     |              _| etch_depth
               core_material        |     |core_thickness
                ______________|_ _ _|_ _ _ _ _ _ _ _
                                    |
                 nbox               |box_thickness
                ______________ _ _ _|_ _ _ _ _ _ _ _
                                    |
                 nsubstrate         |substrate_thickness
                ______________ _ _ _|


```
<!-- #endregion -->

```python
import matplotlib.pyplot as plt
import numpy as np
import gdsfactory.simulation.gmeep as gm
import gdsfactory.simulation as sim
import gdsfactory as gf
from gdsfactory.generic_tech import get_generic_pdk

gf.config.rich_output()
PDK = get_generic_pdk()
PDK.activate()
```

```python
sp = gm.write_sparameters_grating(plot=True)
```

```python
sp = gm.write_sparameters_grating(plot=True, plot_contour=True)
```

```python
sp = gm.write_sparameters_grating(plot=True, plot_contour=True, fiber_angle_deg=45)
```

`plot=True` only plots the simulations for you to review that is set up **correctly**

However the core and cladding index of the fiber are very close to 1.44, so it's hard to see. You can also use

`plot_contour=True` to plot only the contour of the simulation shapes.

```python
sp20 = gm.write_sparameters_grating()  # fiber_angle_deg = 20
```

```python
sim.plot.plot_sparameters(sp20)
```

```python
sp = gm.write_sparameters_grating(fiber_angle_deg=15)
sim.plot.plot_sparameters(sp)
```

### Single core

Running on a single CPU core can be slow as the a single core needs to update all the simulation grid points sequentially.

### Multicore (MPI)

You can divide each simulation into multiple cores thanks to [MPI (message passing interface)](https://en.wikipedia.org/wiki/Message_Passing_Interface)



### Batch

You can also run a batch of multicore simulations


## Far field

TODO
