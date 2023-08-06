# import subprocess
# import os
# import shutil
# import pkg_resources
# import sys
#
# package_path = os.path.dirname(__file__)
# print(f'module_path: {package_path}')
#
# subprocess.check_call(['pip', 'install', package_path])
#
# installed_package_path = pkg_resources.get_distribution('pypdfe').location
# sys.path.insert(0, installed_package_path + os.sep + 'pypdfe')
# # import pypdfe.src.pypdfe
# # shutil.move('pypdfe', 'saves/pypdfe')
# # os.rename('pypdfe', 'pypdfe2')
# # print('importing pypdfe')
# import pypdfe
# # print('imported pypdfe')
# # os.rename('pypdfe2', 'pypdfe')
# # shutil.move('saves/pypdfe', 'pypdfe')
# print('')
