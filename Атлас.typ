#import "@preview/glossarium:0.5.10": make-glossary, print-glossary, register-glossary
#import "sections/00-glossary.typ": entries, glossary-title

#show: make-glossary
#register-glossary(entries)

#let s_title = "Справочник по русскоязычному БДСМ"
#let s_author = "Тео"
#set document(title: s_title, author: s_author)
#set page(paper: "a5", numbering: "1")
#set text(lang: "ru")
#set par(justify: true)
#set heading(numbering: "1.")
// Синие только внешние ссылки; внутренние (глоссарий) -- обычным цветом.
#show link: it => if type(it.dest) == str { text(fill: blue, it) } else { it }
#show bibliography: set text(size: 2 / 3 * 1em)

#page(
  numbering: none,
  margin: 0.5cm,
  fill: gradient.linear(rgb("#EB5324"), rgb("#489B6E"), rgb("#111314"), angle: -247deg),
)[
  #align(center + horizon)[
    #text(size: 1cm, font: "Montserrat", weight: 500)[АТЛАС] \
    #s_author \u{2E31} `v0.1.0` \u{2E31} 2026 \
    #link("https://github.com")[#text(fill: black)[github.com]] // Ссылка на репозиторий книги

    #place(right + top)[#image("assets/images/mark.svg", width: 2cm)]
  ]
]

#outline(depth: 1)

#pagebreak()

Cправочник-навигатор. Книга имеет две части: главы 1-4 читаются последовательно и полностью, остальные -- произвольно.

Примечание: фундаментальных академических исследований русскоязычного БДСМ практически не существует, данная книга опирается на энциклопедические данные, профильную публицистику и устоявшиеся этические нормы самого сообщества.

#pagebreak()

#include "sections/01-intro.typ"

#include "sections/02-history.typ"

#include "sections/03-russia.typ"

#include "sections/04-safety.typ"

#include "sections/05-culture.typ"

#include "sections/06-infrastructure.typ"

#pagebreak()

= Глоссарий

#print-glossary(
  entries,
  groups: ("Основы", "Роли", "Взаимодействие", "Безопасность"),
  show-all: true,
  deduplicate-back-references: true,
  group-heading-level: 2,
  user-print-group-heading: (g, level: none) => heading(g, level: level, numbering: none, outlined: false),
  entry-sortkey: e => e.short,
  user-print-title: glossary-title,
)

#pagebreak()

#bibliography("assets/nerd.bib", title: "Источники")
