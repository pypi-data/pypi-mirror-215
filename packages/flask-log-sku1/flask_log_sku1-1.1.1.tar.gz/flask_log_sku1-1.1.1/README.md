# flask_log_sku1

Simple print formatter

## Installation

```
pip install flask-log-sku1
```

example:

```
from flask_log_sku1 import log

log("Hello world").success()
log("INFO").info()
log("WARNING").warning()
log("ERROR").error()
```

options for log() are:
success()
info()
warning()
error()

## Settings

use the following environment variables to change the following settings:

```
FLASK_LOG_COLOR="True" # default
FLASK_LOG_DATE_FORMAT="%d/%b/%Y %H:%M:%S" # default
```
