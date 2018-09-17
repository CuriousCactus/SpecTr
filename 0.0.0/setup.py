# A very simple setup script to create 2 executables.
#
# hello.py is a simple "hello, world" type program, which alse allows
# to explore the environment in which the script runs.
#
# test_wx.py is a simple wxPython program, it will be converted into a
# console-less program.
#
# If you don't have wxPython installed, you should comment out the
#   windows = ["test_wx.py"]
# line below.
#
#
# Run the build process by entering 'setup.py py2exe' or
# 'python setup.py py2exe' in a console prompt.
#
# If everything works well, you should find a subdirectory named 'dist'
# containing some files, among them hello.exe and test_wx.exe.


from distutils.core import setup
import py2exe
import glob

options = {
    'py2exe': { "includes" : ["matplotlib.backends",  "matplotlib.backends.backend_qt4agg",
                               "matplotlib.figure","pylab", "numpy",
                               "matplotlib.backends.backend_tkagg", "scipy.sparse.csgraph._validation",
                              "scipy.interpolate.dfitpack", "scipy.optimize.minpack2",
                              "scipy.integrate._quadpack", "numpy.fft.fftpack_lite"],
                'excludes': ['_gtkagg', '_tkagg', '_agg2', '_cairo', '_cocoaagg',
                             '_fltkagg', '_gtk', '_gtkcairo', ],
                'dll_excludes': ['libgdk-win32-2.0-0.dll',
                                 'libgobject-2.0-0.dll', 'MSVCP90.dll']
              }
       }


##options = {
##    'py2exe': { "includes" : ["sip", "PyQt4._qt", "matplotlib.backends",  "matplotlib.backends.backend_qt4agg",
##                               "matplotlib.figure","pylab", "numpy", "matplotlib.numerix.fft",
##                               "matplotlib.numerix.linear_algebra", "matplotlib.numerix.random_array",
##                               "matplotlib.backends.backend_tkagg"],
##                'excludes': ['_gtkagg', '_tkagg', '_agg2', '_cairo', '_cocoaagg',
##                             '_fltkagg', '_gtk', '_gtkcairo', ],
##                'dll_excludes': ['libgdk-win32-2.0-0.dll',
##                                 'libgobject-2.0-0.dll', 'MSVCP90.dll']
##              }
##       }

data_files = [(r'mpl-data', glob.glob(r'C:\program files\python\27\Lib\site-packages\matplotlib\mpl-data\*.*')),
                    # Because matplotlibrc does not have an extension, glob does not find it (at least I think that's why)
                    # So add it manually here:
                  (r'mpl-data', [r'C:\program files\python\27\Lib\site-packages\matplotlib\mpl-data\matplotlibrc']),
                  (r'mpl-data\images',glob.glob(r'C:\program files\python\27\Lib\site-packages\matplotlib\mpl-data\images\*.*')),
                  (r'mpl-data\fonts',glob.glob(r'C:\program files\python\27\Lib\site-packages\matplotlib\mpl-data\fonts\*.*'))]
setup(
    # The first three parameters are not required, if at least a
    # 'version' is given, then a versioninfo resource is built from
    # them and added to the executables.
    version = "0.0.0",
    description = "SpecTr - NMR file processing",
    name = "SpecTr",
    options = options,
    # targets to build
    console = ["GUI.py"],
    data_files=data_files,
    )

#get rid of tzdata
