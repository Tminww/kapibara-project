#!/bin/bash
cd ../frontend;
bun install;
bun run build;
cd dist;
python3 -m http.server -b 0.0.0.0 5173;