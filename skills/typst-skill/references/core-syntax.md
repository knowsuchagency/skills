# Core Typst Syntax Reference

## Document Setup

```typst
#set document(title: "Title", author: "Author", keywords: ("kw1", "kw2"))
#set page(
  paper: "a4",           // "us-letter", "a5", etc.
  margin: (x: 2.5cm, y: 2cm),  // or: 2cm, or: (top: 2cm, bottom: 2cm, left: 2.5cm, right: 2.5cm)
  numbering: "1",        // "1", "i", "I", "a", "1 / 1"
  number-align: center,
  fill: white,           // page background color
)
#set text(font: "New Computer Modern", size: 11pt, hyphenate: true)
#set par(justify: true, leading: 0.65em, first-line-indent: 1.5em)
#set heading(numbering: "1.1")
```

## Text Formatting

```typst
*Bold*  _Italic_  `Monospace`
#text(fill: red)[Colored]
#text(size: 14pt, weight: "bold", style: "italic")[Styled]
#smallcaps[Small Caps]
#upper[uppercased]  #lower[LOWERCASED]
#underline[Underlined]  #strike[Struck]  #highlight[Highlighted]
#sub[subscript]  #super[superscript]
```

## Headings

```typst
= Level 1
== Level 2
=== Level 3
```

## Lists

```typst
- Unordered item          + Ordered item
  - Nested item             + Nested ordered
/ Term: Definition
```

## Math

```typst
// Inline
$E = m c^2$

// Display (centered)
$ sum_(i=1)^n i = (n(n+1))/2 $

// Fractions, subscripts, superscripts
$ (a + b) / (c + d) $    $ x_1^2 $

// Greek: alpha, beta, gamma, delta, Delta, Sigma, pi, theta, phi, omega
// Operators: sum, product, integral, union, inter, infinity, emptyset
// Relations: in, subset, <=, >=, !=, approx, equiv

// Matrix
$ mat(a, b; c, d) $

// Aligned equations
$ f(x) &= x^2 + 2x + 1 \
       &= (x + 1)^2 $

// Cases
$ f(x) = cases(
  x^2 &"if" x >= 0,
  -x^2 &"if" x < 0,
) $

// Equation numbering
#set math.equation(numbering: "(1)")
$ E = m c^2 $ <eq-label>
See @eq-label.

// Fraction styles (0.14): "vertical" (default), "skewed", "horizontal"
#set math.frac(style: "skewed")

// Alt text for accessibility (0.14) — takes a STRING, not content
#set math.equation(alt: "description of equation")
```

## Figures & Cross-References

```typst
#figure(
  table(...),  // or image("path.png", width: 80%)
  caption: [Caption text],
  alt: "Alt text string for accessibility",  // 0.14, STRING not content
) <fig-label>

As shown in @fig-label, ...

// Labels on headings
= Introduction <sec-intro>
See @sec-intro.

// Outline
#outline(title: [Table of Contents], indent: auto, depth: 3)
```

## Tables

```typst
// Basic
#table(
  columns: (auto, 1fr, 1fr),
  align: (left, center, right),
  inset: 8pt,
  stroke: 0.5pt,
  fill: (x, y) => if y == 0 { blue.lighten(80%) }
                  else if calc.rem(y, 2) == 0 { gray.lighten(95%) },
  [*Header 1*], [*Header 2*], [*Header 3*],
  [Data], [Data], [Data],
)

// Merged cells
table.cell(colspan: 2)[Spans 2 cols]
table.cell(rowspan: 2)[Spans 2 rows]

// Headers, subheaders, footers (0.14)
table.header([*Col A*], [*Col B*])
table.header([*Sub A*], [*Sub B*], level: 2)
table.footer(table.cell(colspan: 2, align: right)[*Total*], [\$100])
```

## Layout

```typst
#v(1em)  #h(1em)  #v(1fr)  #h(1fr)   // Spacing (fr = fill available)

#align(center)[Centered]
#align(center + horizon)[Both axes]

#columns(2, gutter: 1.5em)[... #colbreak() ...]

#grid(
  columns: (1fr, 2fr, 1fr),
  gutter: 1em,
  [Cell 1], [Cell 2], [Cell 3],
)

#stack(dir: ltr, spacing: 1em, [A], [B], [C])

#pagebreak()
#pagebreak(weak: true)  // Only if not already at page start
```

## Boxes and Blocks

```typst
// Inline box
#box(fill: gray.lighten(90%), inset: (x: 3pt, y: 0pt), radius: 2pt)[inline]

// Block-level
#block(fill: blue.lighten(90%), stroke: (left: 4pt + blue), inset: 12pt, width: 100%, radius: 4pt)[
  Content
]

#rect(width: 100%, height: 50pt, fill: blue.lighten(80%), radius: 4pt)[Content]
#circle(radius: 20pt, fill: red)
#ellipse(width: 60pt, height: 40pt, fill: green)
#line(length: 100%, stroke: 1pt + gray)
```

## Footnotes

```typst
Text with a footnote#footnote[Footnote content].
```

## Special Characters

```typst
~          // Non-breaking space
---        // Em dash
--         // En dash
...        // Ellipsis
```

## Gradients

```typst
gradient.linear(red, yellow, green)
gradient.radial(blue, white)
gradient.conic(red, yellow, green, blue, red)
```

## Tiling Patterns (formerly `pattern`, renamed in 0.14)

```typst
#let dots = tiling(size: (6pt, 6pt))[
  #circle(fill: blue, radius: 1.5pt)
]
#rect(width: 100pt, height: 40pt, fill: dots)
```
