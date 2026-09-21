#!/usr/bin/env python3
from pathlib import Path
import shutil, subprocess
root=Path(__file__).parents[1].resolve(); out=root/'_site'
subprocess.run([str(root/'check-site.sh')],check=True)
if out.exists(): shutil.rmtree(out)
out.mkdir()
for name in ('index.html','guide.html','privacy.html','press.html','styles.css','robots.txt','sitemap.xml'):
 shutil.copy2(root/name,out/name)
(out/'.nojekyll').write_text('',encoding='utf8')
(out/'assets').mkdir()
for name in ('brand.svg','app-icon-1024.png','screenshot-iphone.png','screenshot-ipad.png'):
 shutil.copy2(root/'assets'/name,out/'assets'/name)
print('staged whitelist:', ', '.join(str(p.relative_to(out)) for p in sorted(out.rglob('*')) if p.is_file()))
