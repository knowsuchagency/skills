# Typst Programming Reference

## Functions

```typst
// Basic function
#let greet(name) = [Hello, #name!]

// Named + default parameters, trailing content body
#let callout(title: "Note", color: blue, body) = {
  block(
    fill: color.lighten(92%),
    stroke: (left: 4pt + color),
    inset: 12pt,
    width: 100%,
    radius: (right: 4pt),
  )[
    #text(fill: color.darken(20%), weight: "bold")[#title]
    #v(4pt)
    #body
  ]
}
#callout(title: "Warning", color: orange)[Content here.]

// Variadic
#let sum-all(..nums) = nums.pos().fold(0, (a, b) => a + b)
```

## Variables and Control Flow

```typst
#let x = 10
#let items = ("A", "B", "C")
#let record = (name: "Alice", age: 28)

// Conditionals
#if x > 5 [Big] else [Small]

// Loops
#for item in items [- #item #linebreak()]
#for i in range(1, 6) [#i ]

// Array methods
#items.map(x => [*#x*]).join([, ])
#items.filter(x => x != "B")
#items.enumerate().map(((i, x)) => [#(i + 1). #x])

// IMPORTANT: array.sorted(by:) takes a function returning BOOLEAN, not integer
#let nums = (3, 1, 4)
#nums.sorted()                          // ascending
#nums.sorted(by: (a, b) => a > b)      // descending — returns bool!

// Default values on first/last/join (0.14)
#().first(default: "N/A")
#().last(default: "fallback")
#().join(default: "nothing")

// String methods
#"hello".normalize(form: "nfc")  // Unicode normalization (0.14)
// Valid forms: "nfc", "nfd", "nfkc", "nfkd" — named parameter `form:`
```

## Counters

```typst
#let thm-counter = counter("theorem")

#let theorem(title: none, body) = {
  thm-counter.step()
  block(fill: blue.lighten(95%), stroke: (left: 3pt + blue), inset: 10pt, width: 100%)[
    #text(weight: "bold")[
      Theorem #context thm-counter.display()#if title != none [: #title]
    ]
    #v(4pt)
    #emph(body)
  ]
}
```

## State

```typst
#let total = state("total", 0)
#total.update(42)
#total.update(x => x + 10)
#context total.get()     // Read current value (requires context)
```

## Context

`context` is required when reading values that depend on document position.

```typst
// Page number and position
#context [Page #here().page()]
#context [Position: #here().position()]

// Counter final value (for "Page X of Y")
#context [
  Page #counter(page).display() of #counter(page).final().first()
]

// Query all headings
#context {
  let headings = query(heading)
  [Found #headings.len() headings.]
}
```

## Show Rules

```typst
// Transform specific text
#show "Typst": name => text(fill: blue, weight: "bold")[#name]

// Style headings
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  text(size: 20pt, weight: "bold")[#it.body]
}

// Style inline code
#show raw.where(block: false): it => {
  box(fill: gray.lighten(90%), inset: (x: 3pt, y: 0pt), radius: 2pt)[#it]
}

// Style links
#show link: it => text(fill: blue.darken(20%))[#underline(it)]
```

## Templates

```typst
#let report(title: "", authors: (), abstract: none, body) = {
  set document(title: title, author: authors)
  set page(numbering: "1", number-align: center)
  set text(font: "New Computer Modern", size: 11pt)
  set par(justify: true)
  set heading(numbering: "1.1")

  // Title page
  align(center)[
    #v(2cm)
    #text(size: 24pt, weight: "bold")[#title]
    #v(1cm)
    #text(size: 13pt)[#authors.join(", ")]
    #v(0.5cm)
    #datetime.today().display()
  ]

  if abstract != none {
    v(2cm)
    align(center)[*Abstract*]
    abstract
  }

  pagebreak()
  outline(title: [Contents], indent: auto)
  pagebreak()
  body
}

// Apply template
#show: report.with(
  title: "My Report",
  authors: ("Alice", "Bob"),
  abstract: [This is the abstract.],
)
```

## Page Headers/Footers

```typst
#set page(
  header: context {
    if here().page() > 1 {
      set text(size: 8pt, fill: gray)
      emph("Document Title")
      h(1fr)
      [Page #here().page()]
    }
  },
  footer: context {
    align(center, text(size: 8pt)[#counter(page).display()])
  },
)
```

## Data Loading

```typst
#let data = json("data.json")
#let records = csv("data.csv")
#let config = toml("config.toml")
#let doc = yaml("doc.yml")
// toml() always returns a dictionary

// Iterate
#for item in data.items [- #item.name: #item.value]
```

## Dynamic Table from Data

```typst
#let students = (
  (name: "Alice", score: 95),
  (name: "Bob", score: 82),
)

#table(
  columns: 2,
  [*Name*], [*Score*],
  ..students.map(s => (s.name, str(s.score))).flatten(),
)
```

## Module Inspection (0.14)

```typst
// Check if a name exists in a module
#if "sqrt" in calc [sqrt exists: #calc.sqrt(16)]
```

## Bibliography

```typst
// At end of document or in template
#bibliography("refs.yml", title: [References], style: "ieee")
// Styles: "ieee", "apa", "chicago-notes", "mla", etc.

// Cite in text
@turing1950          // [1] or (Turing, 1950) depending on style
#cite(<turing1950>)  // Equivalent
```

Hayagriva YAML format for references:
```yaml
turing1950:
  type: article
  title: Computing Machinery and Intelligence
  author: Turing, Alan M.
  date: 1950
  parent:
    type: periodical
    title: Mind
    volume: 59
  page-range: 433-460
```
