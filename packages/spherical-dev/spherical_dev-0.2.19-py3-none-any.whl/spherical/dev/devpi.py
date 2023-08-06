import invoke

from .release import build
from .utils import check_tools


@invoke.task
@check_tools('devpi', 'true')
def release(ctx, scm_root='.'):
    ctx.run(f'devpi upload {build(ctx, scm_root)[0]}', pty=True)
