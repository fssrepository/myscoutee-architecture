# MyScoutee Engineering Deep Dive guide

The [English PDF](MyScoutee_Engineering_Deep_Dive_EN.pdf) is the branded architecture guide for this repository. It covers current product architecture, the concise Firebase configuration note, a worked C4/arc42/TOGAF ADM/ADR comparison, software delivery methods from sequential planning through RUP and agile practice, a proposed RUP-to-agile transition, and decision lenses for marketing, cost, Netcup/cloud/Cloudflare, comparable AWS/Azure/Google/OCI stacks, and technology trials. Its source is the Markdown chapters under `guides/development/`; the editable generator is `build-guide.py`. The heart asset is in `assets/heart.png`.

The same generator publishes a separate English patterns, data structures, algorithms and laboratory learning PDF into the sibling `myscoutee-backend/guides/learning/` directory. Its editable source is under `guides/development/engineering/`; the build requires that backend sibling checkout.

Regenerate from the repository root:

```sh
python3 guides/publication/manuals/build-guide.py
```

The generator needs ReportLab, Pillow, Graphviz `dot` and DejaVu Sans fonts. It writes temporary diagram PNGs to `tmp/pdfs/`. Comparison chapters use landscape pages so the alternatives remain side by side. Render the resulting PDF with Poppler and visually inspect all pages after content or layout changes. Update the Markdown, generator and PDF together. The guide distinguishes current application behavior, standalone labs and proposed decisions; it does not replace owner manuals or runtime qualification.
