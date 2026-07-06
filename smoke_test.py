import traceback
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from em_visualisering.registry import PROBLEMS
from em_visualisering.modes import mode_options_for_problem, normalize_mode_for_problem

fail=[]
count=0
for p in PROBLEMS:
    params=p.defaults()
    err=p.validate(params)
    if err:
        fail.append((p.name,'validate',err)); continue
    for label,mode in mode_options_for_problem(p):
        norm=normalize_mode_for_problem(p,mode)
        for meth in ['plot','draw_geometry','draw_3d']:
            fig=Figure(figsize=(3,2), dpi=80)
            try:
                if meth=='plot': p.plot(fig, params, norm)
                elif meth=='draw_geometry': p.draw_geometry(fig, params)
                else: p.draw_3d(fig, params, norm)
            except Exception as e:
                fail.append((p.name,mode,meth,repr(e),traceback.format_exc()))
        try:
            p.result_summary(params,norm)
            p.physics_check(params)
        except Exception as e:
            fail.append((p.name,mode,'summary/check',repr(e),traceback.format_exc()))
        count+=1
print('modes tested', count, 'failures', len(fail))
for f in fail[:20]: print(f)
raise SystemExit(1 if fail else 0)
