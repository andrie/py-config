# User Guide

Given this `config.yaml` file:

``` yaml
default:
  trials: 5
  dataset: "data-sampled.csv"
  
production:
  trials: 30
  dataset: "data.csv"
```

You can read the config file:

``` python
import config.core as config
```

``` python
config.config_get('trials')
```

5

``` python
config.config_get('trials', 'production')
```

30

