// Entry for make.fun news-image-20261120 (Node 22, standard library only):
// the image is entry.png beside this file, drawn in code by draw_entry.py,
// and this program copies it to /output/entry.png. Deterministic: the same
// bytes are written on every run, with no network.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
