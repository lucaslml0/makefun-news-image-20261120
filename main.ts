// Entry point for the make.fun "Sum up 20 November's world news in one
// image" bounty.
//
// The artwork (entry.png) is generated offline by draw_entry.py and ships
// in this repository. Running this script copies it to the output
// directory required by the competition:
//
//   MAKEFUN_OUTPUT_DIR=/output node main.ts   ->  /output/entry.png
//
// If MAKEFUN_OUTPUT_DIR is not set, the output directory defaults to
// /output. No network access is needed.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

if (!existsSync(source)) {
  console.error("entry.png not found next to main.ts");
  process.exit(1);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });

const dest = join(outDir, "entry.png");
copyFileSync(source, dest);
console.log(`Wrote ${dest}`);
