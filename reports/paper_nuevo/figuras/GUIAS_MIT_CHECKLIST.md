# Lista de verificación de figuras según las guías MIT GTL-AI

Fuentes (en `presentations/guias/`): S4 = Sesión 4 «Selecting and Presenting Data (Part 3)», 62 láminas; S5 = Sesión 5 «Designing the Presentation», 24 láminas; S6 = Sesión 6 «Confidence and Delivery», 22 láminas; `academic_style.md` (solo prosa). S4 y S5 son las que tocan figuras; S6 aporta la estructura del mensaje (conclusión primero). Referencias «S4 p.N» = número de lámina del PDF.

Estas guías están escritas para presentaciones. S5 distingue documentos (se sostienen solos) de apoyos visuales (acompañan a un expositor). Un paper es un documento: se conserva el pie de figura con más texto que una lámina, pero cada figura mantiene una idea y un titular.

## A. Percepción gráfica

1. **Jerarquía de canales (S4 p.4–6, 18, 43).** Para magnitudes, de más a menos efectivo: posición en escala común, posición en escala no alineada, longitud, ángulo, área, luminosidad y saturación, curvatura, volumen. Para categorías: región espacial, matiz, movimiento, forma. Una cantidad que importa va en posición o longitud, no en color ni área.
2. **Discriminabilidad (S4 p.7–13).** Dos valores cercanos de luminosidad no se distinguen; hay un umbral de diferencia apenas perceptible y las escalas continuas se leen en escalones. Si hace falta distinguir, los niveles deben estar claramente separados. Pocos niveles, bien espaciados.
3. **Estimación de magnitud (S4 p.14–21).** El área se subestima (ley de Stevens, exponente 0,7); la longitud sobre línea base común se lee con más exactitud. Barras con base común (S4 p.4) mejor que círculos o saturación (S4 p.5). Si se usa área, debe haber una escala de referencia.
4. **Efecto de salto (pop-out) (S4 p.22–27).** El color o la forma únicos se detectan en menos de 200–250 ms. Resaltar el elemento focal con un solo color sobre fondo gris (ejemplos de Google Material, p.27). Un color de foco solo sirve si el resto es neutro.
5. **Atención selectiva (S4 p.28–44).** Dos atributos en el mismo marcador pueden ayudarse (ganancia por redundancia, p.38: misma información en forma y luminosidad) o estorbarse (interferencia de filtrado, p.42–44: dos variables distintas en un mismo símbolo). Usar un canal por variable; redundar solo si ambos canales dicen lo mismo.

## B. Gráficos expresivos

6. **Ejes (S4 p.46–48).** Equilibrar énfasis y omisión: truncar un eje exagera la tendencia, no truncar la oculta. Si se trunca, decirlo en la figura. Una barra no se trunca (la longitud es el dato); un punto sí puede.
7. **Valores atípicos (S4 p.49–53).** Recortar, cortar la escala o usar escala logarítmica, avisando. No dejar que un valor extremo aplaste el resto sin avisar.
8. **Ejes duales (S4 p.54–57).** Evitarlos; preferir múltiplos pequeños con escala compartida (p.56–57).
9. **Relación de aspecto (S4 p.58–60).** El aspecto debe corresponder a la tendencia que se muestra: ni «muy alto y angosto» ni «muy ancho y bajo». En mapas, proporción cartográfica (lon/lat corregida por cos(lat)).

## C. Mensaje y limpieza (S5)

10. **Una idea por figura y destacarla en el diseño (S5 p.9–10).** El cerebro deja de procesar cuando cree entender; muchas ideas por figura agotan la memoria. «Agregar», «limitar tinta, color e ideas», «tan simple como sea posible, pero no más» (S5 p.9).
11. **Color para enfoque, no para decoración (S5 p.11).** Antes: tres colores por categoría; después: un color de énfasis y gris para el resto, con titular que dice qué mirar.
12. **Titular que enuncia el punto, con verbo y como historia (S5 p.14–15).** «Los costos del tercer trimestre suben en la región Este», no «Costos por región». En el paper: la primera frase del pie de figura es el titular.
13. **Maximizar la razón datos/tinta (S5 p.16).** Quitar fondos, íconos sin sentido, exceso de color, rejillas, sombras, 3D y cajas.
14. **Despejar el gráfico (S5 p.17–18).** Quitar marco y rejilla innecesaria, un solo color de barra, etiquetas directas en lugar de ejes y leyendas, texto del título alineado a la izquierda y legible.
15. **Gráfico de pastel con muchas categorías: error típico (S5 p.13).** Leyendas con 20 colores, etiquetas rotadas, categorías diminutas. Equivale a leyenda de siete colores categóricos.
16. **Texto breve (S5 p.12).** Palabras clave, no párrafos dentro de la figura.

## D. Estructura del mensaje (S6)

17. **Conclusión primero («BLUF», S6 p.12) y directo cuando la audiencia es técnica (S6 p.11).** La primera frase del pie dice el resultado; el detalle viene después.
18. **Repetir la idea clave y cerrar con ella (S6 p.17).** El pie termina con la lectura que el texto retomará.
19. **¿Qué gana la audiencia? (S6 p.16).** Cada figura responde una pregunta del lector, no solo muestra datos.

## Lista de comprobación operativa (usada para criticar y rediseñar)

| # | Pregunta | Principio |
|---|---|---|
| 1 | ¿Cuál es la única idea de la figura y se nombra en una frase? | 10, 12, 17 |
| 2 | ¿La cantidad principal va en posición o longitud sobre base común? | 1, 3 |
| 3 | ¿Hay un único color de foco y el resto es gris o neutro? | 4, 11 |
| 4 | ¿Cada color o forma codifica una sola variable? ¿Más de 4 matices categóricos? | 5, 15 |
| 5 | ¿Los niveles de luminosidad o saturación que importan están bien separados? | 2 |
| 6 | ¿Etiquetas directas en lugar de leyenda? ¿Queda alguna leyenda redundante? | 14, 15 |
| 7 | ¿Marco, ticks, rejilla, fondos o texto repetido que no aporten? | 13, 14 |
| 8 | ¿Aspecto correcto (mapas con cos(lat)) y eje sin truncar o con aviso? | 6, 9 |
| 9 | ¿Valores atípicos tratados y avisados? | 7 |
| 10 | ¿Múltiplos pequeños con escala compartida en vez de ejes duales? | 8 |
| 11 | ¿Texto dentro de la figura limitado a palabras clave y del mismo tamaño en todas las figuras? | 16 |
| 12 | ¿El pie abre con el titular y cierra con la lectura? | 12, 17, 18 |

---

# Crítica de las figuras vigentes (antes del rediseño)

Se aplicó la lista a cada PNG. «Viola n.º X» remite a la tabla operativa.

## Figura 1 `fig1_panel` (rechazada)

- **Viola 1.** Dos mensajes en dos mapas (Perú frente a fuera, y zonas) y ninguno enunciado: el lector debe decidir qué mirar.
- **Viola 3 y 4.** Panel b usa siete categorías en siete colores (A a E, Lago Titicaca, Loma): sin foco, sin salto visual y por encima del límite de 4 matices distinguibles (S4 p.4, 43). Violeta, rojo, turquesa, azul grisáceo y rosa tienen luminosidades parecidas.
- **Viola 6.** Dos leyendas en una columna aparte (ámbito y zona), más de un tercio del ancho del gráfico, con puntos de leyenda que obligan a emparejar color con texto (S5 p.13).
- **Viola 7.** Marco con ticks y rejilla de latitud y longitud cada 4° en ambos mapas; el eje de latitud se repite; título «a)» y «b)» solo como rótulos. El panel b repite exactamente la geometría del a.
- **Viola 5.** Gris oscuro y gris claro del panel a están bien separados, pero los puntos con huecos blancos entre celdas generan una textura de moiré que compite con el contorno.
- **Viola 8.** El aspecto es igual en lon y lat (`set_aspect("equal")`), lo que sobreestima el ancho en unos 1,5 %: aceptable, pero no está justificado en la figura.
- **Viola 12.** Pie descriptivo («Celdas de evaluación…»): no dice qué debe concluir el lector.
- Los números (8.272, 8.755) están escritos a mano dentro de las etiquetas de leyenda; el código solo los verifica.

## Figura 2 `fig2_brechas`

- **Bien.** Posición en escala común (S4 p.4), línea del cero marcada, un color por rival coherente con el resto, sin título interno.
- **Viola 6.** Leyenda inferior para dos tipos de IC (trazo grueso con punto lleno, trazo fino con punto hueco): debería ser una etiqueta directa en el primer panel.
- **Viola 7.** Etiqueta del eje x repetida en las dos columnas (dos líneas cada una); rótulos de bloque girados 90° (texto rotado, difícil de leer, S5 p.12).
- **Viola 3.** Los nombres de rival en el eje y están en gris; el color del método solo aparece en los marcadores, de modo que hay que cruzar marcador y etiqueta.
- **Viola 12.** Pie sin titular: abre describiendo, no concluyendo.

## Figura 3 `fig3_anual`

- **Bien.** Etiquetas directas al final de cada línea, cero marcado, bloques separados con línea discontinua, sin leyenda.
- **Viola 7.** Anotaciones «↑ TimesFM peor» y «↓ TimesFM mejor» repetidas en ambos paneles; una por figura basta.
- **Viola 1.** Dos rivales y dos ámbitos en una sola figura: aceptable porque se comparan con el mismo eje, pero el titular debe decir cuál es la lectura (la brecha cambia de signo solo en 2013 de dominio completo).
- Sin cambios mayores.

## Figura 4 `fig4_zonas`

- **Bien.** Puntos ordenados (posición en escala común), orden compartido entre bloques, línea del cero, tamaño de punto con ley de raíz cuadrada y leyenda de tamaños (necesaria por la ley de Stevens, S4 p.15–21).
- **Viola 6.** Leyenda de caja inferior «Rival» con puntos azul y ocre: debe ser etiqueta directa en el panel.
- **Viola 11.** Fuente de 6,4–6,6 pt en las etiquetas de zona y en la nota al pie; 33 filas obligan a ello, pero la nota explicativa del código de zona queda mejor en el pie Quarto.
- **Viola 4.** El tamaño codifica el número de celdas y el color el rival: dos canales para dos variables (S4 p.42: sin interferencia), correcto.
- **Viola 9.** La zona con una sola celda (`D (i) D′`) es un valor extremo a −0,30; no está avisado dentro de la figura, solo por el tamaño del punto.

## Figura 5 `fig5_horizonte`

- **Bien.** Múltiplos pequeños con escala compartida (S4 p.56–57), bandas translúcidas estrechas, cero marcado.
- **Viola 7.** Las anotaciones «↑ TimesFM peor / ↓ TimesFM mejor» y los rótulos «año 1–4» se repiten en las cuatro celdas; los títulos de los cuatro paneles repiten «(17.027 celdas)» y «(8.272 celdas)».
- **Viola 4 y 6.** Cuatro series que se cruzan; el matiz azul claro (`tuned sin Td`) y el azul pleno (`tuned`) difieren sobre todo en luminosidad (S4 p.7–13: difícil), y el trazo discontinuo duplica el canal. La leyenda inferior es inevitable aquí porque las líneas se solapan y no admiten etiqueta directa sin ocultarlas.
- **Viola 9.** Un solo valor extremo (mes 37 de 2013–2016, dominio completo) fija el rango vertical de los cuatro paneles y comprime los de 2009–2012 y Perú (S4 p.49). Se conserva para respetar la escala compartida y comparar bloques.

## Figura 6 `fig6_robustez`

- **Bien.** Intervalos como longitud sobre base común, un color por rival, círculo blanco para el punto.
- **Viola 4.** El grosor del trazo codifica el esquema de bootstrap: el grosor es un canal ordinal débil (S4 p.4, longitud y área frente a grosor); aquí funciona porque los tres esquemas están apilados en orden fijo y la leyenda lo explica.
- **Viola 7.** «← favorece a TimesFM» repetido en cuatro celdas; título «(17.027 celdas)» repetido.
- **Viola 3.** Nombres de rival en gris; el color del método solo en las líneas.

## Suplemento `sfig_escalera_contexto`

- **Bien.** Etiquetas directas, referencia `tuned` como línea punteada, sin leyenda.
- **Viola 7.** Título de panel con «(1.092 celdas)» repetido y etiqueta «tuned (referencia)» repetida.
- **Viola 5.** `llr_rezagos` (ocre claro) y `llr_simple` (marrón) tienen luminosidades distintas y el trazo discontinuo duplica la separación: correcto.

## Suplemento `sfig_a3_tmin_barajada`

- **Viola 6.** Leyenda interna («Corrida de referencia», «Tmin barajada») redundante: los nombres de fila ya dicen «Tmin real» y «Tmin barajada» (S4 p.38: redundancia aceptable, pero la leyenda añade una tercera capa).
- **Viola 8.** El eje x empieza en 0,75 y se avisa en la etiqueta; con puntos (posición) es aceptable (S4 p.46–48).
- **Viola 9.** Tres semillas casi iguales se solapan; se resuelve con desplazamiento vertical mínimo y etiqueta numérica.

---

# Cambios aplicados

Por indicación del usuario solo se rediseñó la Figura 1. Las figuras 2 a 6 y los suplementos no se modificaron; la crítica anterior queda como documentación.

- **Figura 1** rediseñada desde cero: un solo mapa en gris con una zona resaltada, barras de longitud sobre base común con etiquetas directas, sin marco, ticks ni leyendas, escala en km.
