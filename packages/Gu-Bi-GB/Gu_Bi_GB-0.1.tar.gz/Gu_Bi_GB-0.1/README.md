`pip install .`

If everything is set up correctly, pip will install the distributions package into the workspace. You can then start the python interpreter from the terminal typing:
`python`

Then within the Python interpreter, you can use the distributions package:
from distributions import Gaussian

```
gaussian_one = Gaussian(25, 2)
gaussian_one.mean
gaussian_one + gaussian_one
```