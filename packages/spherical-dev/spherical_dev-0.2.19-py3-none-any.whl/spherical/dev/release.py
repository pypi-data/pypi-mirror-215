import pathlib

from setuptools_scm import version_from_scm


def build(ctx, scm_root):
    if not version_from_scm(scm_root).exact:
        raise RuntimeError('dirty versions is not for release')
    ctx.run('python -m build --wheel', pty=True)
    packages = list(pathlib.Path('dist').glob('*'))
    if len(packages) != 1:
        raise RuntimeError('please cleanup (especially dist) before release')
    return packages
