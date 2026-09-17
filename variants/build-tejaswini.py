#!/usr/bin/env python3
"""Build the bride-side variant of the site (invite.prijwal-weds-gauri.in) from this repo.

    python3 variants/build-tejaswini.py            # writes ../prijwal-weds-tejaswini

Every substitution must match exactly once, otherwise the build stops so a silent drift
between the two sites cannot happen. Run it again after any change to the main site,
then commit and push the output repo.
"""
import os, re, shutil, subprocess, sys

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(os.path.dirname(SRC), 'prijwal-weds-tejaswini')
DOMAIN = 'invite.prijwal-weds-gauri.in'


SUBS = [
    # names
    ('<title>Prijwal & Gauri</title>', '<title>Prijwal & Tejaswini</title>'),
    ('content="Prijwal & Gauri — 26 & 27 November 2026, Mannat Palace, Gwalior"', 'content="Prijwal & Tejaswini — 26 & 27 November 2026, Mannat Palace, Gwalior"'),
    ('content="Prijwal & Gauri — Wedding Invitation"', 'content="Prijwal & Tejaswini — Wedding Invitation"'),
    ('<div class="mono">P<span>&amp;</span>G</div>', '<div class="mono">P<span>&amp;</span>T</div>'),
    ('<p class="eyebrow">Prijwal &nbsp;·&nbsp; Gauri</p>', '<p class="eyebrow">Prijwal &nbsp;·&nbsp; Tejaswini</p>'),
    ('alt="Prijwal and Gauri"', 'alt="Prijwal and Tejaswini"'),
    ('alt="Gauri as a little girl"', 'alt="Tejaswini as a little girl"'),
    ('<div class="couple rv d1">Prijwal <span class="amp">&amp;</span> Gauri</div>', '<div class="couple rv d1">Prijwal <span class="amp">&amp;</span> Tejaswini</div>'),
    ('<span>Prijwal &amp; Gauri</span>', '<span>Prijwal &amp; Tejaswini</span>'),
    ("' — Prijwal & Gauri'", "' — Prijwal & Tejaswini'"),
    ("'Wedding celebrations of Prijwal & Gauri. '", "'Wedding celebrations of Prijwal & Tejaswini. '"),
    # domain
    ('content="https://prijwal-weds-gauri.in/"', 'content="https://%s/"' % DOMAIN),
    ('href="https://prijwal-weds-gauri.in/"', 'href="https://%s/"' % DOMAIN),
    ('content="https://prijwal-weds-gauri.in/wedding-photos-v4/', 'content="https://%s/wedding-photos-v4/' % DOMAIN),
    # contacts: bride's side
    ("<b>Ramkumar Singh Rajawat</b><small>Groom's Father</small>", "<b>Aditya Gole</b><small>Bride's Elder Brother</small>"),
    ('href="tel:+918109112694"', 'href="tel:+918830357338"'),
    ('>81091 12694</a>', '>88303 57338</a>'),
    ("<b>Arun Singh Rajawat</b><small>Groom's Elder Brother</small>", "<b>Vijay Gole</b><small>Bride's Father</small>"),
    ('href="tel:+918602170217"', 'href="tel:+917972178745"'),
    ('>86021 70217</a>', '>79721 78745</a>'),
]

def build_html(src_path):
    s = open(src_path, encoding='utf-8').read()
    for old, new in SUBS:
        n = s.count(old)
        if n != 1:
            sys.exit('%s: expected exactly one match, found %d for:\n  %s' % (os.path.basename(src_path), n, old[:90]))
        s = s.replace(old, new)
    leftovers = [m.start() for m in re.finditer('Gauri', s) if 'prijwal-weds-gauri' not in s[max(0, m.start()-25):m.start()+5]]
    if leftovers:
        sys.exit('%s: "Gauri" still present at offsets %s' % (os.path.basename(src_path), leftovers))
    return s

def main():
    if os.path.isdir(OUT):
        for name in os.listdir(OUT):
            if name == '.git':
                continue
            p = os.path.join(OUT, name)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(OUT, exist_ok=True)
    for name in os.listdir(SRC):
        if name in ('.git', 'variants', '.DS_Store'):
            continue
        p = os.path.join(SRC, name)
        if os.path.isdir(p):
            shutil.copytree(p, os.path.join(OUT, name))
        elif name in ('index.html', '404.html'):
            open(os.path.join(OUT, name), 'w', encoding='utf-8').write(build_html(p))
        elif name == 'CNAME':
            open(os.path.join(OUT, name), 'w').write(DOMAIN + '\n')
        else:
            shutil.copy2(p, os.path.join(OUT, name))
    print('built', OUT)

if __name__ == '__main__':
    main()
