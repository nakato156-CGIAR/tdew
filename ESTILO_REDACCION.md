# Estilo de redacción para este proyecto

Este archivo define cómo debe escribirse cualquier texto en prosa que un
agente produzca para este proyecto: documentación (`docs/`, `reports/`,
`README`), páginas de Notion, resúmenes de resultados, mensajes largos, etc.
**No aplica** a comentarios de código (ver `CLAUDE.md`/`AGENTS.md` para eso)
ni a mensajes cortos de ida y vuelta en el chat.

Leer este archivo antes de escribir cualquier documento, reporte o página
nueva.

## Idioma y voz

- Todo texto va en **español**.
- Voz **impersonal/pasiva refleja**, como en un paper o un reporte técnico:
  "se implementó", "se desarrolló", "se validó", "se encontró que...".
  **Nunca primera persona** ("yo hice", "armé", "decidí") ni segunda persona
  dirigida a un lector específico salvo que el propio usuario pida
  explícitamente ese tono para un documento puntual.
- Mantener la misma voz de principio a fin del documento — no alternar entre
  un registro simple y uno excesivamente formal o técnico.

## Qué evitar

- **Lenguaje grandilocuente o inflado.** No calificar algo como "crucial",
  "fundamental", "pivotal", "transformador", "robusto" o "significativo"
  salvo que haya una razón concreta y explicada para ese calificativo.
- **Interpretaciones genéricas después de cada afirmación.** No cerrar
  oraciones con "destacando la importancia de…", "reflejando…",
  "demostrando…", "contribuyendo a…" o "subrayando…".
- **Vocabulario recurrente de textos de IA**: "panorama", "intrincado",
  "robusto", "fomentar", "potenciar", "explorar", "destacar", "evidenciar",
  "testimonio" u otros equivalentes cuando una palabra más simple alcanza.
- **Contrastes retóricos repetidos**: "no solo X, sino también Y", "no se
  trata de X, sino de Y", "más que X, Y".
- **Enumeraciones forzadas de tres elementos.** Usar la cantidad de
  elementos que la idea realmente requiera, ni más ni menos.
- **Estructuras prefabricadas y simétricas** (introducción / beneficios /
  desafíos / futuro / conclusión) cuando el contenido no las pide.
- **Secciones genéricas de relleno** como "Desafíos", "Perspectivas
  futuras", "Impacto" o "Conclusión" agregadas solo para completar una
  estructura. Cada sección debe responder a una necesidad real del
  documento.
- **Conclusiones optimistas genéricas** sin evidencia que las sostenga
  ("el futuro parece prometedor", "esto seguirá siendo importante").
- **Negritas mecánicas.** Reservarlas para lo que de verdad necesita
  énfasis, no aplicarlas por hábito.
- **Fórmulas de asistente conversacional** dentro del documento: "Claro",
  "Por supuesto", "Aquí tienes", "Espero que esto ayude", "¿Te gustaría
  que…?", o cualquier comentario sobre el propio proceso de generación.
- **Residuos técnicos o placeholders**: `[cite]`, `turn0search0`,
  `contentReference`, `[Tu nombre]` o cualquier marcador que no pertenezca
  al texto final.
- **Afirmaciones abstractas sin mecanismo.** En vez de "mejora la
  eficiencia" o "fortalece la innovación", explicar qué cambia
  concretamente, por qué mecanismo, y en qué magnitud si es posible.
- **Exceso de seguridad cuando la evidencia es limitada.** Usar
  formulaciones proporcionales: "sugiere", "es consistente con", "se
  observó en esta muestra".
- **Redundancia semántica**: no reformular la misma idea con otras palabras
  solo para alargar el párrafo.
- Convertir cada dato en una conclusión inmediata. Presentar primero la
  evidencia; interpretar solo cuando esté justificado.
- Forzar cada idea en una lista, subtítulo, tabla o bloque separado cuando
  un párrafo normal alcanza — mantener una estructura natural de párrafos.

## Qué priorizar

- **Afirmaciones concretas**: qué ocurrió, quién/qué lo hizo, cuándo, cómo
  y con qué resultado — no relaciones vagas como "está relacionado con" o
  "desempeña un papel importante".
- **Lenguaje directo sobre lenguaje ornamental.** Si una oración dice lo
  mismo con menos palabras, usar la versión más corta.
- **Variación natural en la longitud y estructura de las oraciones** — no
  repetir el mismo patrón sintáctico en cada párrafo.
- **Detalles específicos** cuando son relevantes: cifras, fechas, nombres,
  condiciones experimentales, límites, ejemplos y excepciones. Aportan más
  que una afirmación general.
- **Referencias verificadas.** No inventar autores, títulos, DOI, ISBN,
  páginas, fechas ni enlaces. Cada fuente citada debe respaldar
  específicamente la afirmación para la que se usa — no citar algo solo
  porque está relacionado con el tema.
- No introducir contexto obvio que el lector objetivo ya debería conocer,
  salvo que sea necesario para seguir el argumento.

## Principio general

Cada oración debe aportar información, evidencia, razonamiento o contexto
necesario. Si una frase solo existe para que el texto suene más elaborado,
se elimina.
