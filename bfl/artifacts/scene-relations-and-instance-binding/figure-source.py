"""Artifact-local proof panels and numerical plots; no model execution."""
from pathlib import Path
import json
import hashlib
import shutil
import numpy as np
from PIL import Image, ImageDraw
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
SATURN=HERE.parents[1]
DEST=SATURN.parent/'research/bfl/artifacts/scene-relations-and-instance-binding'
FIRST=SATURN/'results/flux2-spectral-instance-binding/job-47589b8693dc'
SECOND=SATURN/'results/flux2-spectral-instance-binding/job-6386d22db7c1'


def main():
    DEST.mkdir(parents=True,exist_ok=True)
    seeds=[26091741,26091841,26091842]
    columns=[(FIRST,'neutral','Neutral'),(FIRST,'compiled-left','Saved adjust: L = R'),
             (SECOND,'mean','Shared native mean'),(SECOND,'complement-left','Mean + left complement'),
             (SECOND,'complement-right','Mean + right complement')]
    thumb=256; label=42
    canvas=Image.new('RGB',(thumb*len(columns),(thumb+label)*len(seeds)),'#101a2a')
    draw=ImageDraw.Draw(canvas)
    inputs={}
    for r,seed in enumerate(seeds):
        for c,(root,arm,title) in enumerate(columns):
            source=root/'images'/f'{seed}--{arm}.png'
            picture=Image.open(source).convert('RGB');picture.thumbnail((thumb,thumb),Image.Resampling.LANCZOS)
            x,y=c*thumb,r*(thumb+label)
            draw.text((x+7,y+6),title,fill='white');draw.text((x+7,y+22),f'seed {seed}',fill='#a6b8cf')
            canvas.paste(picture,(x,y+label))
            inputs[str(source.relative_to(SATURN.parent))]=hashlib.sha256(source.read_bytes()).hexdigest()
    canvas.save(DEST/'spectral-binding-followup-proof.png',compress_level=9)
    report=json.loads((FIRST/'report.json').read_text())
    fig,axes=plt.subplots(1,2,figsize=(10,3.7),layout='constrained')
    for seed in seeds:
        rows=[d for d in report['decompositions'] if d['seed']==seed]
        t=[d['step'] for d in rows]
        axes[0].plot(t,[100*d['target_predicate_energy']/d['target_energy'] for d in rows],marker='o',label=str(seed))
        axes[1].plot(t,[d['shared_action_energy']/d['target_energy'] for d in rows],marker='o',label=str(seed))
    axes[0].set(title='Directional energy in 3 predicate rows',xlabel='Denoising step',ylabel='Percent of squared norm',ylim=(0,10),xticks=range(4))
    axes[1].set(title='Shared displacement / directional energy',xlabel='Denoising step',ylabel='Ratio of squared norms',xticks=range(4))
    for ax in axes:ax.grid(alpha=.25);ax.spines[['top','right']].set_visible(False)
    axes[1].legend(title='Discovery seed',fontsize=8)
    fig.suptitle('Representation diagnostics — energy does not certify semantic causality',fontsize=11)
    fig.savefig(DEST/'spectral-binding-state-geometry.png',dpi=180)
    fig.savefig(DEST/'spectral-binding-state-geometry.svg')
    plt.close(fig)
    for label,root in [('first-cut',FIRST),('route-factorization',SECOND)]:
        for name in ('report.json','analysis.json','visual-audit.json','FINDINGS.md','evidence-receipt.json','custody-verification.json','run-receipt.json'):
            src=root/name;dst=DEST/f'{label}-{name}'
            shutil.copyfile(src,dst);inputs[str(src.relative_to(SATURN.parent))]=hashlib.sha256(src.read_bytes()).hexdigest()
    source=DEST/'figure-source.py';shutil.copyfile(__file__,source)
    files={p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
           for p in DEST.iterdir() if p.is_file() and p.name not in ('followup-manifest.json','verify.py')}
    (DEST/'followup-manifest.json').write_text(json.dumps({'schema':'spectral-binding-research-bundle-v1',
        'source_inputs':inputs,'files':files,'scope':'Summary bundle; full individual PNGs, source snapshots and logs remain in the linked Saturn job directories.'},indent=2,sort_keys=True)+'\n')
    print(DEST)


if __name__=='__main__':main()
