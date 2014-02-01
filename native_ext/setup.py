from distutils.core import setup, Extension
import numpy as np

module1 = Extension('hello', sources = ['hellomodule.c'])

setup (name = 'PackageName',
        version = '1.0',
        description = 'This is a demo package',
        include_dirs = [np.get_include()],
        ext_modules = [module1])


#http://en.wikibooks.org/wiki/Python_Programming/Extending_with_C
#http://dan.iel.fm/posts/python-c-extensions/
#http://docs.scipy.org/doc/numpy/user/c-info.how-to-extend.html