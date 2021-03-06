""" Uploads wheels to pypi from travisci.

The commit requires an UPLOAD line.
"""
import glob
import os
import subprocess
import sys


def write_config():
    """
    # Set these inside travis. Note, it is on a per repo basis.
    # https://docs.travis-ci.com/user/environment-variables/#Encrypting-Variables-Using-a-Public-Key
    # travis encrypt PYPI_USERNAME=super_secret --add
    # travis encrypt PYPI_PASSWD=super_secret --add
    """
    username = os.environ['PYPI_USERNAME']
    password = os.environ['PYPI_PASSWD']

    pypirc_template = """\
[distutils]
index-servers =
    pypi
[pypi]
repository: https://upload.pypi.io/legacy/
username: {username}
password: {password}
""".format(username=username, password=password)

    with open('pypirc', 'w') as afile:
        afile.write(pypirc_template)

if '--write-config' in sys.argv:
    write_config()
    sys.exit(0)
else:
    if '--no-config' not in sys.argv:
        write_config()


commit = subprocess.check_output(['git', 'log', '-1'])
print(commit)
if b'UPLOAD' not in commit:
    print('Not uploading')
    sys.exit(0)

# There should be exactly one .whl
filename = glob.glob('dist/*.whl')[0]


print('Calling twine to upload...')
try:
    subprocess.check_call(['twine', 'upload', '--config-file', 'pypirc', filename])
finally:
    os.unlink('pypirc')
