# A1: escalera de inicio del contexto

En el panel nacional, `tmin_anom_full` (contexto desde 1981) superó a `tmin_anom_med` (contexto desde 2002) por 0,062 °C de RMSE en ll4b y 0,047 °C en ll4 (`experiments/llr_simple/resultados_ll4_ll4b.txt`). Esa comparación cambiaba tres cosas a la vez: la longitud del contexto, la presencia de años anteriores a 2000 (cuando PISCO no usa LST de MODIS) y la climatología con la que se forman y deshacen las anomalías, porque `experiments/timesfm/panel.py` la calculaba solo con los años del contexto (2002-2008 en ll4b, 2002-2012 en ll4). Para separarlas se corrió TimesFM `tmin_anom_full` con el contexto empezando en 1981, 1986, 1991, 1996 y 2002 y la climatología fija en 1981-train_end (`--context-start-year`, `--clim-start-year 1981`, `experiments/timesfm/scripts/13_escalera_contexto.sh`), más un control en ll4b con contexto y climatología desde 2002, que reproduce lo que hacía `tmin_anom_med`. El LLR simple y el LLR con rezagos de Tmin se sometieron a la misma escalera (`--train-start`, `14_escalera_llr.sh`): coeficientes y elección de `h` con [inicio, train_end] y la climatología también fija en 1981-train_end. La evaluación se hizo sobre las 1.092 celdas del panel de cribado comunes con `tuned` y los mismos 1.595.412 pares celda-día en cada bloque (`experiments/amenazas/escalera_contexto.py`). La corrida ll4 con inicio 1981 coincidió bit a bit con `ll4__tmin_anom_full.parquet` del cribado original.

Con la climatología fija, el RMSE de TimesFM casi no cambió a lo largo de la escalera: entre 0,767 y 0,773 °C en ll4b y entre 0,839 y 0,844 °C en ll4. Pasar de 1981 a 2002 le costó +0,002 °C en ll4b (IC 95 % mes-año [−0,005; +0,009]) y +0,005 °C en ll4 ([+0,002; +0,008]). El único escalón que se distingue de cero en ambos bloques es el de 1996 a 2002 (+0,006 y +0,004 °C), que también recorta seis años de contexto, así que con esta escalera no se puede atribuir a un quiebre en 2000 y no a la pérdida de longitud. Su magnitud es pequeña frente a la brecha original. El control en ll4b mostró de dónde salía esa brecha: con contexto desde 2002, cambiar la climatología de 1981-2008 a 2002-2008 subió el RMSE de 0,773 a 0,817 °C (+0,044 °C, IC [+0,035; +0,053]). Ese control queda +0,046 °C por encima de la corrida con inicio 1981, del orden de la brecha de 0,062 °C observada en el panel nacional. En esta muestra, casi toda la diferencia entre `tmin_anom_med` y `tmin_anom_full` en ll4b se debe a la climatología de siete años, no a la longitud del contexto ni al régimen anterior a MODIS. El mismo control se corrió después en ll4 (contexto y climatología 2002-2012, `CONTROL_ONLY=1 SPLITS=ll4 13_escalera_contexto.sh`). Allí el control quedó en 0,866 °C, +0,028 °C por encima de la corrida con inicio 1981 (IC mes-año [+0,018; +0,036]). De esa diferencia, +0,022 °C ([+0,015; +0,029]) corresponden a cambiar la climatología de 1981-2012 a 2002-2012 con el contexto fijo desde 2002, y +0,005 °C al recorte del contexto con la climatología fija. En ll4 la climatología explica unas cuatro quintas partes de la diferencia en el panel de cribado, menos que en ll4b (donde explica casi toda), pero sigue siendo el componente principal. Con once años de climatología en vez de siete el efecto es menor, lo que concuerda con que el costo venga de estimar la climatología con pocos años.

Los LLR no se degradaron con menos años; mejoraron. Empezar los coeficientes en 1991 o 1996 bajó el RMSE entre 0,017 y 0,024 °C respecto a 1981 en ambos bloques, con intervalos que excluyen el cero. Empezar en 2002 empeoró algo respecto a 1996 (+0,007 a +0,010 °C), y quedó sin diferencia distinguible de 1981 en ll4b y por debajo de 1981 en ll4. La mejora aparece al quitar 1981-1990 y no al quitar 1996-1999, lo que no apunta a un quiebre en 2000. Es compatible con que la relación Td-Tmin de PISCO en la primera década no sea la misma que en los años recientes, aunque esta escalera no identifica la causa. Como TimesFM no se mueve y los LLR mejoran, la ventaja de TimesFM sobre el LLR con rezagos se reduce de 0,047 a 0,027 °C en ll4b (inicio 1991) y de 0,055 a 0,030 °C en ll4 (inicio 1996), y en todos los inicios sigue con intervalos que excluyen el cero. Que TimesFM necesite más historial que un regresor simple no se sostiene con estos datos: con climatología fija, la longitud del contexto le resulta casi indiferente entre 7 y 28 años (ll4b) o entre 11 y 32 (ll4), mientras que al LLR le conviene descartar los años más antiguos. Hay una salvedad para los LLR: la `h` elegida fue 60 en 19 de las 20 corridas, el extremo de la grilla `H_GRID`, así que una ventana más ancha podría cambiar algo sus cifras. En el panel nacional se repitió la elección con la grilla ampliada hasta `h` = 180 y el año de inicio elegido junto con `h` por validación interna (`--select-train-start`, `a1_desglose.md`): en los cuatro casos (dos LLR, dos bloques) se eligió el inicio 1991 y `h` entre 45 y 90, sin tocar el borde.

<!-- tablas:inicio -->
### Bloque `ll4b`: RMSE total (°C) por inicio del historial (1092 celdas, 1.595.412 filas)

| método | 1981 | 1986 | 1991 | 1996 | 2002 | Δ 2002 − 1981 |
|---|---|---|---|---|---|---|
| TimesFM tmin_anom_full | 0,771 | 0,770 | 0,769 | 0,767 | 0,773 | +0,002 |
| LLR simple | 0,823 | 0,814 | 0,805 | 0,807 | 0,815 | −0,009 |
| LLR con rezagos | 0,817 | 0,806 | 0,796 | 0,798 | 0,808 | −0,009 |
| TimesFM, climatología propia (control) |  |  |  |  | 0,817 | |
| climatología | 1,143 |  |  |  |  | |
| tuned (referencia) | 0,848 |  |  |  |  | |

### Bloque `ll4b`: RMSE por año del bloque (°C)

| método | inicio | 2009 | 2010 | 2011 | 2012 |
|---|---|---|---|---|---|
| TimesFM tmin_anom_full | 1981 | 0,723 | 0,753 | 0,773 | 0,829 |
| TimesFM tmin_anom_full | 1986 | 0,724 | 0,754 | 0,770 | 0,829 |
| TimesFM tmin_anom_full | 1991 | 0,722 | 0,753 | 0,773 | 0,824 |
| TimesFM tmin_anom_full | 1996 | 0,728 | 0,749 | 0,774 | 0,816 |
| TimesFM tmin_anom_full | 2002 | 0,738 | 0,760 | 0,777 | 0,814 |
| LLR simple | 1981 | 0,771 | 0,829 | 0,815 | 0,875 |
| LLR simple | 1986 | 0,766 | 0,815 | 0,808 | 0,865 |
| LLR simple | 1991 | 0,759 | 0,802 | 0,808 | 0,847 |
| LLR simple | 1996 | 0,759 | 0,803 | 0,809 | 0,853 |
| LLR simple | 2002 | 0,766 | 0,809 | 0,815 | 0,866 |
| LLR con rezagos | 1981 | 0,765 | 0,822 | 0,810 | 0,870 |
| LLR con rezagos | 1986 | 0,758 | 0,805 | 0,801 | 0,857 |
| LLR con rezagos | 1991 | 0,749 | 0,791 | 0,801 | 0,839 |
| LLR con rezagos | 1996 | 0,749 | 0,794 | 0,804 | 0,844 |
| LLR con rezagos | 2002 | 0,761 | 0,800 | 0,811 | 0,858 |

### Bloque `ll4`: RMSE total (°C) por inicio del historial (1092 celdas, 1.595.412 filas)

| método | 1981 | 1986 | 1991 | 1996 | 2002 | Δ 2002 − 1981 |
|---|---|---|---|---|---|---|
| TimesFM tmin_anom_full | 0,839 | 0,841 | 0,840 | 0,840 | 0,844 | +0,005 |
| LLR simple | 0,906 | 0,900 | 0,887 | 0,886 | 0,893 | −0,013 |
| LLR con rezagos | 0,894 | 0,886 | 0,873 | 0,871 | 0,877 | −0,017 |
| TimesFM, climatología propia (control) |  |  |  |  | 0,866 | |
| climatología | 1,284 |  |  |  |  | |
| tuned (referencia) | 0,933 |  |  |  |  | |

### Bloque `ll4`: RMSE por año del bloque (°C)

| método | inicio | 2013 | 2014 | 2015 | 2016 |
|---|---|---|---|---|---|
| TimesFM tmin_anom_full | 1981 | 0,805 | 0,841 | 0,823 | 0,883 |
| TimesFM tmin_anom_full | 1986 | 0,807 | 0,842 | 0,827 | 0,886 |
| TimesFM tmin_anom_full | 1991 | 0,809 | 0,841 | 0,821 | 0,886 |
| TimesFM tmin_anom_full | 1996 | 0,807 | 0,840 | 0,828 | 0,884 |
| TimesFM tmin_anom_full | 2002 | 0,816 | 0,845 | 0,826 | 0,887 |
| LLR simple | 1981 | 0,851 | 0,893 | 0,908 | 0,968 |
| LLR simple | 1986 | 0,846 | 0,890 | 0,903 | 0,956 |
| LLR simple | 1991 | 0,849 | 0,876 | 0,888 | 0,934 |
| LLR simple | 1996 | 0,846 | 0,881 | 0,888 | 0,928 |
| LLR simple | 2002 | 0,843 | 0,884 | 0,901 | 0,940 |
| LLR con rezagos | 1981 | 0,842 | 0,885 | 0,894 | 0,951 |
| LLR con rezagos | 1986 | 0,837 | 0,880 | 0,886 | 0,937 |
| LLR con rezagos | 1991 | 0,837 | 0,867 | 0,870 | 0,916 |
| LLR con rezagos | 1996 | 0,831 | 0,871 | 0,869 | 0,909 |
| LLR con rezagos | 2002 | 0,828 | 0,874 | 0,883 | 0,920 |

### Brechas pareadas RMSE(A) − RMSE(B), IC 95 % (°C; negativo favorece a A)

| bloque | A − B | brecha | IC mes-año | IC espacial 2° |
|---|---|---|---|---|
| ll4b | timesfm@1986 − timesfm@1981 | −0,0004 | [−0,0020; +0,0010] | [−0,0023; +0,0012] |
| ll4b | timesfm@1991 − timesfm@1981 | −0,0020 | [−0,0042; +0,0003] | [−0,0038; −0,0006] |
| ll4b | timesfm@1996 − timesfm@1981 | −0,0033 | [−0,0085; +0,0017] | [−0,0055; −0,0011] |
| ll4b | timesfm@2002 − timesfm@1981 | +0,0022 | [−0,0049; +0,0090] | [−0,0024; +0,0067] |
| ll4b | timesfm@1991 − timesfm@1986 | −0,0016 | [−0,0044; +0,0013] | [−0,0030; −0,0004] |
| ll4b | timesfm@1996 − timesfm@1991 | −0,0013 | [−0,0050; +0,0024] | [−0,0033; +0,0009] |
| ll4b | timesfm@2002 − timesfm@1996 | +0,0055 | [+0,0024; +0,0085] | [+0,0025; +0,0087] |
| ll4b | llr_simple@1986 − llr_simple@1981 | −0,0092 | [−0,0129; −0,0057] | [−0,0125; −0,0057] |
| ll4b | llr_simple@1991 − llr_simple@1981 | −0,0187 | [−0,0274; −0,0093] | [−0,0258; −0,0114] |
| ll4b | llr_simple@1996 − llr_simple@1981 | −0,0166 | [−0,0265; −0,0067] | [−0,0249; −0,0076] |
| ll4b | llr_simple@2002 − llr_simple@1981 | −0,0088 | [−0,0212; +0,0038] | [−0,0184; +0,0007] |
| ll4b | llr_simple@1991 − llr_simple@1986 | −0,0094 | [−0,0157; −0,0033] | [−0,0134; −0,0056] |
| ll4b | llr_simple@1996 − llr_simple@1991 | +0,0021 | [−0,0009; +0,0050] | [+0,0004; +0,0039] |
| ll4b | llr_simple@2002 − llr_simple@1996 | +0,0077 | [+0,0017; +0,0141] | [+0,0047; +0,0104] |
| ll4b | llr_rezagos@1986 − llr_rezagos@1981 | −0,0111 | [−0,0146; −0,0075] | [−0,0150; −0,0071] |
| ll4b | llr_rezagos@1991 − llr_rezagos@1981 | −0,0215 | [−0,0302; −0,0122] | [−0,0299; −0,0126] |
| ll4b | llr_rezagos@1996 − llr_rezagos@1981 | −0,0189 | [−0,0284; −0,0087] | [−0,0287; −0,0084] |
| ll4b | llr_rezagos@2002 − llr_rezagos@1981 | −0,0092 | [−0,0210; +0,0028] | [−0,0199; +0,0011] |
| ll4b | llr_rezagos@1991 − llr_rezagos@1986 | −0,0103 | [−0,0165; −0,0042] | [−0,0150; −0,0055] |
| ll4b | llr_rezagos@1996 − llr_rezagos@1991 | +0,0026 | [−0,0004; +0,0053] | [+0,0008; +0,0044] |
| ll4b | llr_rezagos@2002 − llr_rezagos@1996 | +0,0096 | [+0,0041; +0,0155] | [+0,0067; +0,0124] |
| ll4b | timesfm@1981 − llr_rezagos@1981 | −0,0466 | [−0,0597; −0,0343] | [−0,0573; −0,0361] |
| ll4b | timesfm@1981 − llr_simple@1981 | −0,0527 | [−0,0656; −0,0400] | [−0,0604; −0,0451] |
| ll4b | timesfm@1986 − llr_rezagos@1986 | −0,0359 | [−0,0457; −0,0268] | [−0,0421; −0,0303] |
| ll4b | timesfm@1986 − llr_simple@1986 | −0,0439 | [−0,0543; −0,0340] | [−0,0486; −0,0393] |
| ll4b | timesfm@1991 − llr_rezagos@1991 | −0,0272 | [−0,0343; −0,0201] | [−0,0307; −0,0237] |
| ll4b | timesfm@1991 − llr_simple@1991 | −0,0361 | [−0,0433; −0,0289] | [−0,0405; −0,0314] |
| ll4b | timesfm@1996 − llr_rezagos@1996 | −0,0310 | [−0,0401; −0,0223] | [−0,0346; −0,0274] |
| ll4b | timesfm@1996 − llr_simple@1996 | −0,0395 | [−0,0484; −0,0309] | [−0,0440; −0,0346] |
| ll4b | timesfm@2002 − llr_rezagos@2002 | −0,0352 | [−0,0439; −0,0261] | [−0,0401; −0,0305] |
| ll4b | timesfm@2002 − llr_simple@2002 | −0,0417 | [−0,0507; −0,0326] | [−0,0484; −0,0349] |
| ll4b | timesfm_clim_propia@2002 − timesfm@2002 | +0,0442 | [+0,0347; +0,0532] | [+0,0406; +0,0480] |
| ll4b | timesfm_clim_propia@2002 − timesfm@1981 | +0,0463 | [+0,0347; +0,0575] | [+0,0396; +0,0529] |
| ll4 | timesfm@1986 − timesfm@1981 | +0,0023 | [+0,0009; +0,0036] | [+0,0014; +0,0032] |
| ll4 | timesfm@1991 − timesfm@1981 | +0,0010 | [−0,0007; +0,0028] | [−0,0003; +0,0025] |
| ll4 | timesfm@1996 − timesfm@1981 | +0,0013 | [−0,0009; +0,0037] | [−0,0008; +0,0038] |
| ll4 | timesfm@2002 − timesfm@1981 | +0,0051 | [+0,0019; +0,0084] | [+0,0024; +0,0087] |
| ll4 | timesfm@1991 − timesfm@1986 | −0,0013 | [−0,0032; +0,0006] | [−0,0022; −0,0002] |
| ll4 | timesfm@1996 − timesfm@1991 | +0,0002 | [−0,0020; +0,0029] | [−0,0022; +0,0031] |
| ll4 | timesfm@2002 − timesfm@1996 | +0,0039 | [+0,0011; +0,0065] | [+0,0020; +0,0060] |
| ll4 | llr_simple@1986 − llr_simple@1981 | −0,0062 | [−0,0098; −0,0028] | [−0,0097; −0,0021] |
| ll4 | llr_simple@1991 − llr_simple@1981 | −0,0185 | [−0,0268; −0,0099] | [−0,0258; −0,0103] |
| ll4 | llr_simple@1996 − llr_simple@1981 | −0,0198 | [−0,0288; −0,0102] | [−0,0281; −0,0105] |
| ll4 | llr_simple@2002 − llr_simple@1981 | −0,0130 | [−0,0228; −0,0029] | [−0,0219; −0,0028] |
| ll4 | llr_simple@1991 − llr_simple@1986 | −0,0123 | [−0,0178; −0,0061] | [−0,0163; −0,0080] |
| ll4 | llr_simple@1996 − llr_simple@1991 | −0,0012 | [−0,0039; +0,0012] | [−0,0028; +0,0003] |
| ll4 | llr_simple@2002 − llr_simple@1996 | +0,0067 | [+0,0026; +0,0111] | [+0,0048; +0,0091] |
| ll4 | llr_rezagos@1986 − llr_rezagos@1981 | −0,0081 | [−0,0115; −0,0049] | [−0,0123; −0,0034] |
| ll4 | llr_rezagos@1991 − llr_rezagos@1981 | −0,0212 | [−0,0289; −0,0129] | [−0,0301; −0,0111] |
| ll4 | llr_rezagos@1996 − llr_rezagos@1981 | −0,0235 | [−0,0320; −0,0143] | [−0,0339; −0,0122] |
| ll4 | llr_rezagos@2002 − llr_rezagos@1981 | −0,0169 | [−0,0256; −0,0078] | [−0,0272; −0,0053] |
| ll4 | llr_rezagos@1991 − llr_rezagos@1986 | −0,0131 | [−0,0184; −0,0071] | [−0,0180; −0,0076] |
| ll4 | llr_rezagos@1996 − llr_rezagos@1991 | −0,0023 | [−0,0051; +0,0005] | [−0,0046; −0,0002] |
| ll4 | llr_rezagos@2002 − llr_rezagos@1996 | +0,0066 | [+0,0025; +0,0107] | [+0,0044; +0,0092] |
| ll4 | timesfm@1981 − llr_rezagos@1981 | −0,0552 | [−0,0672; −0,0427] | [−0,0680; −0,0400] |
| ll4 | timesfm@1981 − llr_simple@1981 | −0,0670 | [−0,0803; −0,0536] | [−0,0763; −0,0552] |
| ll4 | timesfm@1986 − llr_rezagos@1986 | −0,0447 | [−0,0548; −0,0344] | [−0,0534; −0,0339] |
| ll4 | timesfm@1986 − llr_simple@1986 | −0,0585 | [−0,0698; −0,0471] | [−0,0649; −0,0501] |
| ll4 | timesfm@1991 − llr_rezagos@1991 | −0,0330 | [−0,0408; −0,0258] | [−0,0382; −0,0256] |
| ll4 | timesfm@1991 − llr_simple@1991 | −0,0475 | [−0,0569; −0,0387] | [−0,0531; −0,0405] |
| ll4 | timesfm@1996 − llr_rezagos@1996 | −0,0304 | [−0,0380; −0,0237] | [−0,0360; −0,0224] |
| ll4 | timesfm@1996 − llr_simple@1996 | −0,0460 | [−0,0542; −0,0376] | [−0,0514; −0,0390] |
| ll4 | timesfm@2002 − llr_rezagos@2002 | −0,0332 | [−0,0432; −0,0235] | [−0,0398; −0,0246] |
| ll4 | timesfm@2002 − llr_simple@2002 | −0,0489 | [−0,0610; −0,0369] | [−0,0550; −0,0408] |
| ll4 | timesfm_clim_propia@2002 − timesfm@2002 | +0,0224 | [+0,0147; +0,0294] | [+0,0197; +0,0249] |
| ll4 | timesfm_clim_propia@2002 − timesfm@1981 | +0,0275 | [+0,0183; +0,0361] | [+0,0240; +0,0308] |

<!-- tablas:fin -->
