#!/usr/bin/python2.7 -OO

from packager import MiraiUnpackager

import sys
package = sys.argv.pop(1)

mu = MiraiUnpackager()
sys.meta_path.append(mu)
mu.load(package)

exec mu.modules['__main__'][1]
