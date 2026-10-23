// Copiado de reports/pram/typst-preamble.typ (origen: PRAM, Palacios); reutilizado aquí sin cambios de contenido.
// Preámbulo de estilo para la salida Typst (se inyecta vía `include-in-header`).
// No fija página/fuente/tamaño: eso lo controla el YAML de Quarto
// (papersize, margin, fontsize, mainfont) para evitar conflictos.

// Párrafos justificados con guionado.
#set par(justify: true)
#set text(hyphenate: true)

// Encabezados con color de acento (azul corporativo sobrio).
#show heading.where(level: 1): set text(fill: rgb("#1F4E79"))
#show heading.where(level: 2): set text(fill: rgb("#2E74B5"))
#show heading.where(level: 3): set text(fill: rgb("#595959"))

// Bloques de código / pseudocódigo: fondo suave, esquinas redondeadas
// y una barra de acento a la izquierda.
#show raw.where(block: true): it => block(
  fill: rgb("#F4F6F8"),
  inset: 9pt,
  radius: 3pt,
  width: 100%,
  stroke: (left: 2pt + rgb("#2E74B5")),
  text(size: 8.5pt, it),
)

// Enlaces (DOIs, URLs) en color de acento.
#show link: set text(fill: rgb("#2E74B5"))

// Tablas del paper nuevo (reports/paper_nuevo/): letra menor, sin justificar ni guionar dentro de celdas
// y con corte entre páginas, para que las tablas largas no se salgan del pliego.
// Quarto envuelve las tablas en figure(kind: "quarto-float-tbl").
#show figure.where(kind: "quarto-float-tbl"): set block(breakable: true)
#show table: set text(size: 8pt, hyphenate: false)
#show table: set par(justify: false)

// --- Maquetación de tablas y pies (auditoría de figuras, 2026-10-23) ---------------------------
// Filas de tabla que no se parten entre páginas, con interlineado más ajustado.
#set table.cell(breakable: false)
#set table(inset: (x: 4pt, y: 3pt))
// Pies alineados a la izquierda, sin justificar, y pegados a su figura o tabla
// (el pie de una tabla va arriba: la tabla lleva su rótulo antes de las filas).
#show figure.caption: set align(left)
#show figure.caption: set par(justify: false)
#show figure.where(kind: "quarto-float-tbl"): set figure.caption(position: top)
// Suplemento: "Tabla S9" y "Figura S9" con el número de la seccion S9 del suplemento (no una cuenta corrida).
// Quarto compone el rotulo como "<suplemento> <numero>"; cuando el suplemento termina en " S" (crossref de suplemento.qmd)
// se sustituye el numero automatico por "<seccion>" o, si la seccion tiene varias tablas (o figuras), "<seccion>a", "<seccion>b"...
// La seccion se lee del texto del encabezado de nivel 1 ("S9. Habilidad ..."); sin ese patron, se mantiene la cuenta corrida.
#let _plano(c) = {
  if type(c) == str { c }
  else if c.has("text") { c.text }
  else if c.has("children") { c.children.map(_plano).join() }
  else if c.has("body") { _plano(c.body) }
  else if c == [ ] { " " }
  else { "" }
}
#let _sec = state("sup-sec", none)
#show heading.where(level: 1): it => {
  let m = _plano(it.body).match(regex("^S(\\d+)\\."))
  if m != none { _sec.update(m.captures.at(0)) }
  it
}
#let _es-sup(sup) = sup != none and sup.has("text") and sup.text.ends-with(" S")
// Numero que sigue a "S": "9", o "1a", "1b" si la seccion trae varias del mismo tipo.
// `loc` es la posicion de la figura o de su pie (el pie esta dentro de la figura, que no se anida).
#let _etq(loc, kind, numbering-fn) = context {
  let sec = _sec.at(loc)
  if sec == none { return numbering(numbering-fn, ..counter(figure.where(kind: kind)).at(loc)) }
  let mismas = query(figure.where(kind: kind)).filter(f => _sec.at(f.location()) == sec)
  if mismas.len() <= 1 { return sec }
  let k = query(figure.where(kind: kind).before(loc)).filter(f => _sec.at(f.location()) == sec).len() - 1
  sec + "abcdefghijklmnopqrstuvwxyz".at(k)
}
#show ref: it => {
  let el = it.element
  if el == none or el.func() != figure or not _es-sup(el.supplement) { return it }
  link(el.location(), [#el.supplement.text#_etq(el.location(), el.kind, el.numbering)])
}
#show figure.caption: it => block(sticky: true, {
  if _es-sup(it.supplement) {
    it.supplement
    _etq(here(), it.kind, it.numbering)
    it.separator
    it.body
  } else { it }
})

// Título único de la sección de bibliografía.
#set bibliography(title: "Referencias")
