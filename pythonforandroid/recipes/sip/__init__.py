from pythonforandroid.recipe import CompiledComponentsPythonRecipe


class SipRecipe(CompiledComponentsPythonRecipe):
    version = '6.7.7'
    url = "https://pypi.python.org/packages/source/s/sip/sip-{version}.tar.gz"
    name = 'sip'

    depends = ['setuptools', 'packaging', 'toml', 'ply']

    call_hostpython_via_targetpython = False
    install_in_hostpython = True
    install_in_targetpython = False  # FIXME broken
    site_packages_name = 'sipbuild'


recipe = SipRecipe()
