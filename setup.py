# Run the build process by entering 'setup.py py2exe' or
# 'python setup.py py2exe' in a console prompt.
#
# If everything works well, you should find a subdirectory named 'dist'
# containing some files, among them hello.exe and test_wx.exe.

from distutils.core import setup
import py2exe
import glob
import os, shutil

def find_data_files(source,target,patterns):
    """Locates the specified data-files and returns the matches
    in a data_files compatible format.

    source is the root of the source data tree.
        Use '' or '.' for current directory.
    target is the root of the target data tree.
        Use '' or '.' for the distribution directory.
    patterns is a sequence of glob-patterns for the
        files you want to copy.
    """
    if glob.has_magic(source) or glob.has_magic(target):
        raise ValueError("Magic not allowed in src, target")
    ret = {}
    for pattern in patterns:
        pattern = os.path.join(source,pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target,os.path.relpath(filename,source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path,[]).append(filename)
    return sorted(ret.items())

options = {
    'py2exe': { "includes" : ["matplotlib.backends",  "matplotlib.backends.backend_qt4agg",
                               "matplotlib.figure","pylab", "numpy",
                               "matplotlib.backends.backend_tkagg", "scipy.sparse.csgraph._validation",
                              "scipy.interpolate.dfitpack", "scipy.optimize.minpack2",
                              "scipy.integrate._quadpack", "numpy.fft.fftpack_lite"],
                'excludes': ['_ssl','_gtkagg', '_tkagg', '_agg2', '_cairo', '_cocoaagg',
                             '_fltkagg', '_gtk', '_gtkcairo', 'pytz'],
                'dll_excludes': ['libgdk-win32-2.0-0.dll',
                                 'libgobject-2.0-0.dll', 'MSVCP90.dll']
              }
       }

data_files = find_data_files('Examples','Examples',['1\*', '2\*', '1\pdata\\1\*', '2\pdata\\1\*']) + \
    find_data_files('C:\program files\python\\27\Lib\site-packages\matplotlib\mpl-data','mpl-data',['images\*', '*']) + \
    find_data_files('Images','Images',['*.gif', '*.ico']) + \
    find_data_files('','',['3rd_party_licenses.txt'])

setup(
    # The first three parameters are not required, if at least a
    # 'version' is given, then a versioninfo resource is built from
    # them and added to the executables.
    version = "0.0.1",
    description = "SpecTr - NMR file processing",
    name = "SpecTr",
    options = options,
    # targets to build
    windows = ["SpecTr.py"],
    data_files=data_files,
    )

#get rid of tzdata
shutil.rmtree('dist/tcl/tcl8.5/tzdata')
shutil.rmtree('dist/tcl/tcl8.5/encoding')
shutil.rmtree('dist/tcl/tk8.5/images')
shutil.rmtree('dist/tcl/tk8.5/demos')
