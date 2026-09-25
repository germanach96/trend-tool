# Contexto del proyecto — Herramienta de visualización de tendencias (sell-in / sell-out) · v2

> **LEE ESTO PRIMERO.** Este archivo es contexto teórico y de diseño, no una orden de construir.
> La **spec conceptual ya está bastante completa** (a diferencia de la v1), pero **todavía faltan
> los campos/columnas exactos del Excel y algunos umbrales** (ver §12). **No construyas hasta que
> Germán te dé esos campos y confirmes contra ellos.** Tu tarea ahora es entender la teoría, la
> lógica de recomendación y los límites de fiabilidad para no contradecirlos cuando construyas.

---

## 1. Quién y para qué

- Autor: **Germán**, planificador de demanda en **Coty**, mercado **USA**, categorías **perfume y maquillaje**.
- Cartera muy de **iniciativas** (lanzamientos) → muchos artículos con **poca o ninguna historia**. Esto condiciona todo: cualquier cálculo debe degradar con elegancia cuando faltan datos.
- Objetivo: un **HTML** que visualice **tendencias existentes** de sell-in y sell-out por código y le diga a Germán, de un vistazo, **si un forecast es coherente y dónde mirar**.

---

## 2. Concepto base: sell-in vs sell-out y el *gap*

- **Sell-out (SO)** = lo que compra el **consumidor**. Demanda real, anclada a fechas fijas.
- **Sell-in (SI)** = lo que **pide el retailer**. Decisión de negocio, se mueve de un año a otro.
- **El gap es la señal central:** SO por encima de SI = **depleción** (riesgo de rotura). SI por encima de SO = **sobre-stock**. Un valle de SI por destock **no es demanda**, es ajuste de canal.
- **Regla sagrada:** SI y SO se calculan con **el mismo método y las mismas ventanas**, o el gap no significa nada.

---

## 3. Las barras/flechas: definición de tendencia (DECISIONES FINALES)

- **Tendencia = variación YoY (interanual).** 12m = últimos 12 meses vs los 12 anteriores; 6m = últimos 6 vs los mismos 6 del año pasado.
- **Se eligió YoY a propósito** porque se **desestacionaliza solo** (diciembre vs diciembre). → **NO se aplican índices de estacionalidad en v1.**
- **En unidades, no en valor.**
- La serie debe ir **limpia de promo y destock** antes de calcular (ver §11.5), o la tendencia hereda eventos de LY.

---

## 4. Aceleración / desaceleración → la flecha

En el gráfico, la tendencia de cada serie se dibuja como una **flecha gruesa** (no rectángulo):
- **Base de la flecha = tendencia 12m.** **Punta = tendencia 6m.**
- Punta por encima de base → **acelerando**. Punta por debajo → **frenando**.
- Una flecha para **SO (azul)** y otra para **SI (naranja)**.
- Interpretación: la flecha es **momentum** (dirección/magnitud del cambio 6m→12m), **no** una banda de tolerancia estadística.

---

## 5. Los rombos: son FORECAST futuro (corrección importante)

- Los **rombos** son la **variación YoY prevista (forecast)** de **Q2, Q3, Q4 y del FY completo** — es decir, **futuro**, no pasado. (Las flechas son pasado; los rombos son el forecast que se está validando.)
- Colores del gráfico original: Q2 rojo, Q3 morado, Q4 amarillo, FY verde.
- Se dibujan superpuestos sobre el gráfico, cada uno a su valor YoY.

---

## 6. La zona verde recomendada (dónde deben ir los rombos)

- Sobre el gráfico se pinta una **banda verde = la zona donde el forecast (rombos) debería situarse** según la tendencia de demanda. **No** es el gap; es la recomendación.
- El rombo que cae **dentro** de la banda es coherente; el que cae **fuera** es un *flag* ("míralo").
- **Regla de apertura:** cuando la recomendación es **abierta / más allá del límite de las flechas** ("at or above sell-out, high" o "down to sell-out, low"), la banda **crece hacia el borde** del gráfico y se **desvanece** en el lado abierto, dibujando solo la línea de límite en el lado del sell-out. Cuando la recomendación es **acotada** (entre las flechas, en convergencia), la banda es cerrada con línea arriba y abajo.

---

## 7. Motor de recomendación: los 12 casos

La posición de la zona verde sale de cruzar el estado de SO con el de SI.

**Estados por tendencia (una flecha): 6.** Dos ejes — signo (+/−) y momentum (↑/↓) → 4 estados base
(+↑ crece y acelera, +↓ crece y frena, −↑ cae y se recupera, −↓ cae y empeora), más **2 cruces de cero**
(**turnaround** = ↑ cruzando a positivo; **rollover** = ↓ cruzando a negativo), que son las alarmas más tempranas.

**Cruzando SO × SI → 12 casos que importan:** 3 gaps (depleción / equilibrio / sobre-stock) × 4 trayectorias del gap (↑↑, ↑↓, ↓↑, ↓↓). Signos y cruces de cero alimentan el gap y marcan intensidad.

### Gap 1 — DEPLECIÓN (SO por encima de SI, riesgo de rotura)
| Caso (SO/SI) | Qué pasa | Zona recomendada para los rombos |
|---|---|---|
| SO↑ / SI↓ | Depleción acelerando — peor caso | **En o por encima del sell-out (abierta arriba)**; nunca seguir al SI hundido |
| SO↑ / SI↑ | Demanda sube, envíos persiguen por debajo | En el sell-out, sesgo ligeramente arriba |
| SO↓ / SI↓ | Ambos enfrían, aún corto | Entre las dos flechas, bajando pero por encima del SI |
| SO↓ / SI↑ | Auto-corrección, gap cerrando | En la convergencia (mid) |

### Gap 2 — EQUILIBRIO (SO ≈ SI, vigilar la divergencia)
| Caso (SO/SI) | Qué pasa | Zona recomendada |
|---|---|---|
| SO↑ / SI↑ | Expansión sana | Arriba, en línea con ambas flechas |
| SO↓ / SI↓ | Declive gestionado (o alerta si no es intencionado) | Abajo, en línea con ambas |
| SO↑ / SI↓ | Depleción formándose (alerta temprana) | Sesgo arriba hacia el sell-out, pronto |
| SO↓ / SI↑ | Sobre-stock formándose (alerta temprana) | Sesgo abajo hacia el sell-out, pronto |

### Gap 3 — SOBRE-STOCK (SI por encima de SO, exceso de inventario)
| Caso (SO/SI) | Qué pasa | Zona recomendada |
|---|---|---|
| SO↓ / SI↑ | Sobre-stock acelerando — peor caso | **Abajo, hasta el sell-out (abierta abajo)**; cortar |
| SO↓ / SI↓ | Envíos enfriando hacia la demanda | Bajo, tendiendo al sell-out |
| SO↑ / SI↑ | Demanda subiendo hacia los envíos | Arriba; el gap cierra por demanda |
| SO↑ / SI↓ | Convergiendo rápido (puede voltear a depleción) | En la convergencia; vigilar el flip |

**Filosofía:** es un **detector de dónde mirar, no un veredicto**. Que un rombo salga de la banda significa *investiga*, no *está mal*. La causa la pone el planner.

---

## 8. Suficiencia de datos y fallback en cascada

Como la cartera es de iniciativas, muchos códigos no tienen historia propia. Regla:

- **Cascada de repliegue: EAN → familia → segmento → categoría.** Si el EAN no tiene datos suficientes, sube a familia; si no, a segmento; y así hasta el **primer nivel con datos suficientes**. Sube **lo mínimo necesario** (más arriba = más robusto pero más genérico).
- **Mínimo: al menos 1 año** de historia comparable. Si ni subiendo de nivel hay ≥1 año → marcar **"no suficiente info"** (no inventar tendencia ni dibujar barra con 3 datos).
- **Emparejar periodos, no solo rangos:** el YoY solo vale comparando **los mismos meses**. Un artículo nacido a mitad de año no compara 8 meses contra 12; alinear meses equivalentes o subir de nivel.
- **La familia también tiene que ser YoY-comparable** (tener su propio año de referencia); si es toda de lanzamientos recientes, el problema se hereda un piso arriba.
- La herramienta muestra **tendencias a distintos niveles** de la jerarquía cuando cada nivel tiene datos.
- El **umbral exacto** de "datos suficientes" (mínimo de meses + % de cobertura) **lo define Germán** (pendiente).

---

## 9. Fiabilidad y límites (IMPORTANTE — construir estos avisos en la herramienta)

Esta herramienta es un **filtro de coherencia**, no un generador de forecast. Es fiable para *priorizar dónde mirar* y cazar errores gordos; **no** para clavar la cifra del FY. Puntos a respetar y, cuando aplique, a **mostrar en la UI**:

- **Detector, no oráculo.** Mostrar un aviso permanente tipo "place to look, not a verdict".
- **Efecto base (el más importante):** como todo es YoY, la comparación es tan limpia como lo fuera LY. En códigos **jóvenes / de poca historia** la **magnitud** del YoY está inflada por una **base baja de LY** (ej. sell-out +185% o +68%). → **Fiarse de la dirección, no del nivel**, y bajar al fallback de familia antes de dimensionar. La herramienta debería **marcar visualmente** los códigos con %-alto y/o poca historia como "nivel poco fiable".
- **Base sucia:** si LY tuvo promo, stockout, pipeline de lanzamiento o distribución distinta, el YoY mide contra una base deformada. De ahí la limpieza de promo/destock (§11.5).
- **Persistencia:** las flechas son **trailing (pasado)**; los rombos son **futuro**. Alinear el rombo al sell-out asume que el momentum reciente persiste — la asunción que más falla cuanto más lejos se mira.
- **FY vs quarter:** anclar el forecast al sell-out es **conceptualmente más sólido a nivel FY** que a nivel quarter (el gap y el destock son de *timing* y se netean en el año). Pero el horizonte de 12m degrada la persistencia, el FY esconde estacionalidades de regalo distintas, y buena parte del FY son iniciativas sin tendencia → la herramienta es **más fiable en la punta de 6m y el quarter cercano** que en el rombo del FY.
- **Lo que estructuralmente NO ve:** el **nivel** (solo trabaja en % vs LY — un código pequeño y uno enorme con el mismo YoY pesan igual); la **causa** (destock, colapso de demanda o eco de promo se parecen); lo **exógeno** (distribución nueva, delisting, precio, lanzamiento de competidor).
- **La única medida real de fiabilidad es backtestearlo:** coger las flechas de hace un año, ver dónde habrían mandado los rombos, y compararlo con lo que pasó. Ese hit-rate sobre el histórico propio dice en qué gaps y a qué madurez acierta.

---

## 10. Objetivo de la herramienta (lo YA definido)

Un **HTML local, mono-usuario**, que:
- **Lee un Excel que el usuario selecciona** con un **botón (file picker)** — un solo clic; sin servidor, offline. Parseo con **SheetJS embebido** en el propio HTML (no depender de internet en red corporativa).
- **Pestañas (tabs): una por categoría.**
- Dentro de cada tab, **elegir entre las opciones del Excel** cargado (combo box desplegable **o** texto tecleado), por **EAN o por familia**.
- **Muestra**, siempre que haya datos suficientes (§8; si no, "no suficiente info"):
  - los **puntos por quarter (Q2, Q3, Q4) y del FY** (rombos = forecast YoY),
  - las **tendencias a distintos niveles** de la jerarquía,
  - la **tendencia como flecha gruesa** (base 12m, punta 6m) por SO y SI,
  - la **zona verde recomendada** para los rombos, con la **regla de apertura** del §6.
- Es un **prototipo de visualización** para iterar el gráfico antes del dashboard de producción (ver §11.0).

---

## 11. Contexto de fondo (no todo es v1)

### 11.0 Pipeline de datos (Databricks)
El dato vive en un **datalake** accesible vía **Databricks**. Pipeline eventual de producción:
**Extraer** (un `SELECT` acotado, read-only, a una tabla Delta en un sandbox propio) → **Analizar**
(notebook: limpieza + perfiles + tendencias + zonas) → **Dashboard** (Databricks SQL nativo o Power BI encima).
Principios: **solo lectura**, escribir solo en schema propio, **agregar/filtrar en el motor** y no materializar
millones de filas al driver. **El HTML de este proyecto es el prototipo de la capa de visualización**, alimentado
por un Excel exportado; la lógica de cálculo acabará en el notebook, no en el front.

### 11.1 Estacionalidad categorías US (contexto)
Fragancia muy *gift-driven* (Q4 >40% del año, dic ~60% del Q4; picos Navidad, San Valentín, Día de la Madre, Día del Padre). Maquillaje más plano (back-to-school en agosto, Halloween en octubre, holiday). En v1 no se modela (YoY lo absorbe).

### 11.2 Lag sell-out → sell-in
~1 quarter como primera aproximación, pero es una **convolución** (distribución de lead times) → el pico de SI es más bajo y ancho. No uniforme: gift sets se adelantan más, maquillaje menos, iniciativas = pipeline fill anclado al lanzamiento.

### 11.3 Dos ejes de perfil (para fases futuras de forecast, no v1)
**Temporada** (mes) × **ciclo de vida / antigüedad** (meses-desde-lanzamiento, MOM). Forecast ≈ base × idx_temporada × idx_ciclo. El perfil de antigüedad se saca de la cohorte de lanzamientos pasados (normalizar, alinear por MOM, mediana), **desestacionalizando antes** de alinear por edad. Beauty muy *front-loaded*.

### 11.4 Rango razonable por percentiles (fases futuras)
Percentiles (P10–P90) por MOM: banda **ancha en el lanzamiento, estrecha con la madurez**. Cuidado con sesgo de supervivencia; normalizar por punto de distribución (sell-in por puerta).

### 11.5 Limpieza de promo y destock
Fuera del baseline; van como eventos por encima. Promo = incremental **real** + adelanto (pull-forward con payback). Destock = **no es demanda**, es canal. Separar usando el **sell-out** (POS). Taggear eventos; tratar pico+payback en pareja.

---

## 12. Pendiente (lo aporta Germán — no lo inventes)

- **Campos y columnas exactas** del Excel (nombres, estructura, qué es cada uno, cómo vienen SO/SI 6m/12m y los forecast por quarter/FY).
- **Umbral preciso de "datos suficientes"** (mínimo de meses + % de cobertura para no subir de nivel).
- **Niveles exactos** de la jerarquía (EAN, familia, segmento, categoría) y **cómo se identifican** en el Excel.
- **Parámetros finales de cálculo** y estética/layout definitivos.

**Hasta tener esos campos: no construyas.** Confirma que entiendes la teoría, la lógica de los 12 casos, la zona verde y los límites de fiabilidad, y espera.
