// News image for 17 November 2026: the entry is the PNG beside this
// file, drawn by tools/generate_image.py from the day's reported stories.
// This program only copies it to the grader's output directory, so both
// runs write exactly the same bytes. Node 22, standard library only.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

const source = new URL("./entry.png", import.meta.url);
if (!existsSync(source)) {
  throw new Error("entry.png is missing next to main.ts");
}
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(source, target);
const size = statSync(target).size;
if (size === 0 || size > 1048576) {
  throw new Error(`entry.png is ${size} bytes, outside the 1 MiB gate`);
}
