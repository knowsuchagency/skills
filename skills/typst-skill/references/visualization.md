# Data Visualization & Graphics Reference

## CeTZ Package (Vector Graphics)

CeTZ is the standard vector graphics package for Typst. Use `@preview/cetz:0.3.4`.

```typst
#import "@preview/cetz:0.3.4"

#cetz.canvas(length: 1cm, {
  import cetz.draw: *

  // Lines
  line((0, 0), (5, 3), stroke: 2pt + blue)

  // Circles
  circle((2, 2), radius: 0.5, fill: red, stroke: 1pt + black)

  // Rectangles
  rect((0, 0), (4, 3), fill: blue.lighten(80%))

  // Arcs (for pie charts)
  arc((0, 0), start: 0deg, stop: 90deg, radius: 2, mode: "PIE", fill: green)

  // Text labels
  content((2, -0.5), text(size: 8pt)[Label], anchor: "north")
})
```

### Line Chart Pattern

```typst
#cetz.canvas(length: 1cm, {
  import cetz.draw: *

  let width = 12
  let height = 6
  let data = (("Jan", 120), ("Feb", 145), ("Mar", 200))
  let max-val = 250
  let n = data.len()

  // Grid lines
  for i in range(0, 6) {
    let y = i * height / 5
    line((0, y), (width, y), stroke: 0.3pt + gray.lighten(50%))
    content((-0.5, y), text(size: 7pt, fill: gray)[#str(calc.round(i * max-val / 5))], anchor: "east")
  }

  // Compute points
  let points = data.enumerate().map(((i, (_, val))) => {
    (i * width / (n - 1), val / max-val * height)
  })

  // Fill area under curve
  line((0, 0), ..points, (width, 0), close: true, fill: blue.lighten(90%), stroke: none)

  // Line
  line(..points, stroke: 2pt + blue)

  // Data points
  for pt in points { circle(pt, radius: 0.1, fill: blue, stroke: 1pt + white) }

  // X-axis labels
  for (i, (month, _)) in data.enumerate() {
    content((i * width / (n - 1), -0.5), text(size: 7pt)[#month], anchor: "north")
  }

  // Axes
  line((0, 0), (width, 0), stroke: 1pt)
  line((0, 0), (0, height), stroke: 1pt)
})
```

### Pie Chart Pattern

```typst
#cetz.canvas(length: 1cm, {
  import cetz.draw: *

  let segments = (("A", 40, blue), ("B", 35, green), ("C", 25, orange))
  let radius = 2.5
  let start = 0deg

  for (label, pct, color) in segments {
    let sweep = pct / 100 * 360deg
    let end = start + sweep
    let mid = start + sweep / 2

    arc((0, 0), start: start, stop: end, radius: radius,
        mode: "PIE", fill: color.lighten(30%), stroke: 1pt + white)

    let r = radius + 0.8
    content((r * calc.cos(mid), r * calc.sin(mid)),
            text(size: 8pt)[#label #pct%])

    start = end
  }
})
```

## Native Drawing with `curve()` (replaces deprecated `path()`)

**IMPORTANT:** `path()` is deprecated since Typst 0.14. Use `curve()` instead.

```typst
// Straight lines
#curve(
  fill: yellow,
  stroke: 2pt + orange,
  curve.move((0%, 0%)),
  curve.line((100%, 0%)),
  curve.line((50%, 100%)),
  curve.close(),
)

// Cubic bezier
#curve(
  stroke: 2pt + blue,
  curve.move((0%, 50%)),
  curve.cubic((25%, 0%), (75%, 100%), (100%, 50%)),  // (ctrl1, ctrl2, end)
)

// Quadratic bezier
#curve(
  stroke: 2pt + purple,
  curve.move((0%, 80%)),
  curve.quad((50%, -20%), (100%, 80%)),  // (control, end)
)
```

## Dashboard Components

### Horizontal Bar Chart

```typst
#let h-bar(value, max-val, height: 16pt, color: blue) = {
  let pct = calc.min(100, calc.round(value / max-val * 100))
  box(width: 100%, height: height)[
    #place(rect(width: 100%, height: height, fill: color.lighten(88%), radius: 3pt))
    #place(rect(width: pct * 1%, height: height, fill: color, radius: 3pt))
  ]
}
```

### Metric Card

```typst
#let metric-card(label, current, previous, format-fn: str) = {
  let pct = if previous != 0 { calc.round((current - previous) / previous * 100, digits: 1) } else { 0 }
  let trend-color = if pct >= 0 { green } else { red }
  let arrow = if pct >= 0 { sym.arrow.t } else { sym.arrow.b }

  block(fill: white, stroke: 1pt + gray.lighten(60%), radius: 8pt, inset: 14pt, width: 100%)[
    #text(size: 7.5pt, fill: gray, weight: "semibold")[#upper(label)]
    #v(6pt)
    #text(size: 22pt, weight: "bold")[#format-fn(current)]
    #v(4pt)
    #text(size: 7.5pt, fill: trend-color, weight: "semibold")[#arrow #calc.abs(pct)%]
  ]
}
```

### Progress Bar

```typst
#let progress-bar(label, value, max-val, color: blue) = {
  let pct = calc.round(value / max-val * 100, digits: 0)
  grid(
    columns: (80pt, 1fr, 40pt),
    gutter: 8pt,
    align: (left + horizon, horizon, right + horizon),
    text(size: 8pt, weight: "medium")[#label],
    h-bar(value, max-val, color: color),
    text(size: 8pt, fill: gray)[#pct%],
  )
}
```

## Adaptive Layout

### Using `layout()` for Responsive Design

```typst
#let responsive(body) = {
  layout(size => {
    if size.width > 400pt {
      columns(2, gutter: 1em, body)
    } else {
      body
    }
  })
}
```

### Using `measure()` for Content-Aware Decisions

```typst
// measure() requires context
#context {
  let size = measure[Some content]
  [Width: #size.width, Height: #size.height]
}
```
