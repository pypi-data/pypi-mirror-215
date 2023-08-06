import invoke

from .release import build
from .utils import check_tools


@invoke.task
@check_tools('twine')
def release(ctx, scm_root='.'):
    ctx.run(f'twine upload {build(ctx, scm_root)[0]}', pty=True)
