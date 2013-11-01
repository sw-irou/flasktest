#!/usr/bin/env python
import sys
sys.path.append('/var/www/lib')
from demo import app

if __name__ == "__main__":
    app.debug = True

    app.run(host='0.0.0.0', port=5003)
