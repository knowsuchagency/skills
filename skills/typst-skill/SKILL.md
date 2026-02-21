---
name: typst
description: "Expert reference for the Typst typesetting system (v0.14). Use this skill when creating professional documents, academic papers, reports, data-driven dashboards, or any typeset output with Typst. Triggers: creating .typ files, typesetting documents, building PDFs with Typst, making charts/tables/math in Typst, academic paper formatting, document templates."
---

# Typst Expert Reference (v0.14)

Typst is a modern typesetting system — fast compilation, clean syntax, built-in scripting. Compiles to PDF (accessible/tagged by default in 0.14), SVG, PNG, or HTML.

## Compilation

```bash
typst compile input.typ                    # Compile to PDF
typst compile input.typ output.pdf         # Explicit output
typst watch input.typ                      # Auto-recompile on save
typst fonts                                # List available system fonts
```

## Reference Files

- **Core syntax** (text, math, tables, layout, figures): See [references/core-syntax.md](references/core-syntax.md)
- **Programming** (functions, state, counters, templates, show rules, data loading, bibliography): See [references/programming.md](references/programming.md)
- **Visualization** (CeTZ charts, curve drawing, dashboard components, adaptive layout): See [references/visualization.md](references/visualization.md)

## Critical Gotchas (Verified by Testing)

These are non-obvious pitfalls that cause compilation errors. Memorize these.

### Deprecated Functions (0.14)
| Old | New | Removal |
|---|---|---|
| `path(...)` | `curve(curve.move(...), curve.line(...), curve.close())` | 0.15 |
| `pattern(...)` | `tiling(...)` | 0.15 |
| `pdf.embed(...)` | `pdf.attach(...)` | 0.15 |

### Types That Catch You Off Guard
| Feature | Expected | Actual |
|---|---|---|
| `figure(alt: ...)` | content `[...]` | **string** `"..."` |
| `math.equation(alt: ...)` | content | **string** |
| `array.sorted(by: ...)` | integer comparator | **boolean** `(a, b) => a > b` |
| `str.normalize(...)` | positional arg | **named**: `.normalize(form: "nfc")` |
| `math.frac(style: ...)` | "inline"/"display" | `"vertical"`, `"skewed"`, `"horizontal"` |

### The `context` Requirement
`context` is required to read any value that depends on document position:
```typst
// WRONG: #counter(page).display()
// RIGHT:
#context counter(page).display()
#context here().page()
#context state("x").get()
```

### Content vs Code Mode
Inside `{ }` you're in code mode. Inside `[ ]` you're in content mode. Use `#` to embed code in content.
```typst
#let myfunc(x) = {
  let y = x + 1        // code mode — no # needed
  [Result: #y]          // content mode — # needed for variables
}
```

### Variable Fonts Warning
Some system fonts (e.g., "Ubuntu Sans") are variable fonts and produce warnings. Prefer static fonts:
- `"New Computer Modern"` — default, good for academic
- `"Libertinus Serif"` — good serif alternative
- `"Lato"` — clean sans-serif
- `"DejaVu Sans"` / `"DejaVu Serif"` — widely available

### Show Rule Gotchas
```typst
// Access heading number inside show rule — need context
#show heading.where(level: 1): it => {
  text(size: 20pt)[
    #if it.numbering != none {
      context counter(heading).display()  // context needed!
      h(8pt)
    }
    #it.body  // Use it.body, not it (avoids infinite recursion)
  ]
}
```

### Common Patterns That Just Work

Callout box:
```typst
#let callout(title: "Note", color: blue, body) = block(
  fill: color.lighten(92%), stroke: (left: 4pt + color),
  inset: 12pt, width: 100%, radius: (right: 4pt),
)[
  #text(fill: color.darken(20%), weight: "bold")[#title]
  #v(4pt)
  #body
]
```

Theorem environment with auto-numbering:
```typst
#let thm-ctr = counter("theorem")
#let theorem(title: none, body) = {
  thm-ctr.step()
  block(fill: blue.lighten(95%), stroke: (left: 3pt + blue), inset: 10pt, width: 100%)[
    #text(weight: "bold")[Theorem #context thm-ctr.display()#if title != none [: #title]]
    #v(4pt)
    #emph(body)
  ]
}
```

Dynamic table from array data:
```typst
#let data = ((name: "A", val: 1), (name: "B", val: 2))
#table(
  columns: 2,
  [*Name*], [*Value*],
  ..data.map(d => (d.name, str(d.val))).flatten(),
)
```

## Typst 0.14 Key Features

- **Accessible PDFs**: Tagged by default, PDF/UA-1 opt-in
- **PDF/A support**: All standards (1a through 4e)
- **Multiple table headers**: `table.header(..., level: 2)` for subheaders
- **Table footers**: `table.footer(...)`
- **`curve()` replaces `path()`**: With `curve.move`, `curve.line`, `curve.cubic`, `curve.quad`, `curve.close`
- **`tiling()` replaces `pattern()`**
- **`figure.alt`**: String alt text for accessibility
- **`math.equation.alt`**: String alt text for equations
- **`math.frac(style:)`**: `"vertical"`, `"skewed"`, `"horizontal"`
- **`pdf.artifact()`**: Mark decorative content as non-semantic
- **`pdf.attach()`**: Attach files to PDF (replaces `pdf.embed`)
- **Character-level justification**:
  ```typst
  #set par(justify: true, justification-limits: (
    spacing: (min: 66.67% + 0pt, max: 150% + 0pt),
    tracking: (min: -0.01em, max: 0.02em),
  ))
  ```
- **`array.sorted(by:)`**: Custom sort with boolean comparator
- **`str.normalize(form:)`**: Unicode normalization ("nfc", "nfd", "nfkc", "nfkd")
- **`in` for modules**: `if "sqrt" in calc [...]`
- **More locatable elements**: `par`, `table`, `enum`, `list`, `image`, `link`, `cite`, `raw`, etc. work with `query()` without labels
- **WebP and PDF images**: Both now supported as image sources

## Useful Packages

Import from Typst Universe with `#import "@preview/name:version"`.

| Package | Version | Use |
|---|---|---|
| `cetz` | `0.3.4` | Vector graphics (charts, diagrams, shapes) |
| `fletcher` | `0.5.8` | Flow diagrams and commutative diagrams |
| `tablex` | `0.0.9` | Advanced tables (mostly superseded by built-in tables in 0.14) |
| `showybox` | `2.0.4` | Decorative boxes and callouts |
| `codly` | `1.3.0` | Code block styling |
| `ctheorems` | `1.1.3` | Theorem environments |
