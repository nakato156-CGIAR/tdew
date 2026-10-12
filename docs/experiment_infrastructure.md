# Infraestructura experimental: Beads + DVC + MLflow + Git

> Generado con asistencia de IA (Claude Code) el 2026-09-15 para preparar el
> arranque de la Semana 1 del plan en Notion (Timeline Planner). Validar con
> el equipo antes de asumir cualquier decision cientifica listada aqui como
> cerrada.

## Separacion de responsabilidades

| Herramienta | Dueña de que estado |
|---|---|
| **Notion** | Planificacion humana / timeline / fechas / prioridades del negocio. Fuente de verdad del plan. |
| **Beads** (`bd`) | Trabajo ejecutable para agentes: dependencias, blockers, acceptance criteria. Un bead puede referenciar un artefacto/stage DVC/experiment MLflow, pero no duplica metricas. |
| **DVC** | Datasets, transformaciones y reproducibilidad de datos (`dvc.yaml`, archivos `*.dvc`). |
| **MLflow** | Runs, parametros, metricas, checkpoints y artefactos experimentales. |
| **Git** | Codigo, configuracion y documentacion (incluye `dvc.yaml` y los `*.dvc` pointers, que son texto pequeño). |

No se duplica la misma informacion en las cuatro herramientas: el timeline
vive en Notion, el grafo de trabajo vive en Beads, los datos versionados
viven en DVC, y las metricas de entrenamiento viven en MLflow.

## 1. Consultar y ejecutar trabajo con Beads

```bash
bd ready              # Que bead(s) estan desbloqueados ahora mismo
bd show <id>          # Objetivo, actividades, entregable, DoD, dependencias
bd update <id> --claim --status=in_progress
# ... hacer el trabajo ...
bd close <id> --reason="..."
bd ready              # Vuelve a consultar: que se desbloqueo
```

El timeline completo de la Semana 1 (Notion Timeline Planner, pagina
"Tdew") esta representado como una cadena lineal de 7 beads
(`tdew-cra` -> `tdew-ztn` -> `tdew-x46` -> `tdew-2s6` -> `tdew-efi` ->
`tdew-bs4` -> `tdew-dy3`), reflejando exactamente las relaciones
`Blocked by` / `Blocking` de Notion. Cada bead incluye en su descripcion el
objetivo y las actividades de Notion, y en su acceptance criteria el
entregable y el "Criterio de cierre" / Definition of Done literal de Notion.

No agregar tareas de dias futuros como "ready" artificialmente: si un bead
tiene un blocker real de Notion, debe seguir bloqueado en Beads.

## 2. DVC — versionado de datos

```bash
dvc status      # Que deps/outs del pipeline cambiaron desde el ultimo dvc.lock
dvc dag         # Ver el grafo de stages (bronze -> silver -> gold)
dvc add <ruta>  # Empezar a versionar un dataset nuevo (crea <ruta>.dvc)
dvc repro       # Ejecutar el pipeline completo (pesado: Data/bronze ~3GB, Data/silver ~11GB)
```

Estado actual:
- `dvc init` ya ejecutado; `.dvc/config` y `.dvcignore` versionados en git.
- `dvc.yaml` declara las 3 etapas que YA EXISTEN como scripts reales
  (`pipeline/bronze.py`, `pipeline/silver.py`, `pipeline/gold.py`). No se
  inventaron stages para el pipeline de deep learning (TCN/GRU/Transformer)
  porque esos scripts todavia no existen — se agregaran cuando los beads
  `tdew-ztn`/`tdew-x46`/`tdew-2s6`/`tdew-efi` los implementen.
- El unico dataset ya trackeado con `dvc add` es
  `Data/silver/department_grid_ids/` (13MB, el artefacto de seleccion de
  sitios del Dia 1). `Data/bronze` y `Data/silver` (el resto) son grandes
  (~3GB / ~11GB) y **no** se hicieron `dvc add` en esta sesion para no
  duplicar ese volumen en la cache local sin necesidad inmediata; el
  `dvc.yaml` los referencia como archivos planos en disco, no como salidas
  cacheadas (`cache: false`).
- **Remote: pendiente.** No hay `dvc remote` configurado (no se inventaron
  credenciales ni un backend ficticio). DVC funciona 100% local por ahora.
  Cuando exista un remote real (S3/GDrive/servidor propio), agregarlo con
  `dvc remote add -d <name> <url>` y `dvc push`.

### Nota tecnica sobre `.gitignore`

La regla `data/` en `.gitignore` tambien bloqueaba `Data/` (mayuscula) por
case-insensitivity en checkouts de Windows, ocultando cualquier archivo
`.dvc` bajo `Data/`. Se agrego una excepcion minima y explicita (ver
comentario en `.gitignore`) que solo destapa la ruta
`Data/silver/department_grid_ids.dvc`; el resto de `Data/` sigue ignorado
por git como antes. Si se agregan mas datasets DVC bajo `Data/`, extender
esa cadena de negacion.

## 3. MLflow — tracking de experimentos

Backend local por defecto: SQLite (`mlflow.db` en la raiz del repo). El
store de archivos plano (`./mlruns`) esta en modo mantenimiento en MLflow
3.x, por eso se eligio SQLite en vez de eso.

```bash
# Iniciar la UI para inspeccionar runs localmente
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

Todo script de entrenamiento futuro (TCN, GRU, Transformer, ...) debe
loguear via el helper compartido `tdew_estimation/experiment_tracking.py`
en vez de llamar a `mlflow` directamente, para que todos los runs queden
taggeados de forma consistente:

```python
from tdew_estimation import experiment_tracking as et
import mlflow

with et.start_run(
    "week1-tcn",
    seed=0,
    dataset_version="Data/silver/department_grid_ids.dvc@<md5>",
    site="lima",
    context_length=30,
    params={"hidden_size": 64, "n_layers": 3},
) as run:
    ...
    mlflow.log_metric("val_rmse", rmse)
    mlflow.log_artifact("checkpoint.pt")
```

`start_run` tagea automaticamente: `git_commit`, `seed`, `dataset_version`,
`site`, `context_length`. El resto (arquitectura, config completa, tiempo de
entrenamiento, uso de GPU, checkpoints, resultados de validation/test) se
loguea con las llamadas normales de MLflow (`mlflow.log_param(s)`,
`mlflow.log_metric(s)`, `mlflow.log_artifact(s)`) dentro del `with`.

Hay un smoke test dedicado (`tests/test_experiment_tracking_smoke.py`) que
verifica que un run se abre, se tagea y se cierra correctamente contra un
store SQLite temporal. Es un smoke test, no un experimento real; se puede
borrar una vez que el primer script de entrenamiento real haya ejercitado
este camino end-to-end.

## 4. Workflow esperado para una sesion futura de Claude/Codex

```text
1. bd ready                        # Que bead esta desbloqueado
2. bd show <id>                    # Leer objetivo/actividades/DoD/dependencias
3. bd update <id> --claim          # Reclamar el trabajo
4. Implementar el trabajo
5. dvc add / dvc repro             # Versionar datos/outputs reproducibles (si aplica)
6. et.start_run(...) + mlflow.log* # Registrar el run experimental (si aplica)
7. pytest                          # Quality gates (tests existentes + nuevos)
8. Verificar acceptance criteria del bead contra lo entregado
9. bd close <id> --reason="..."
10. bd ready                       # Continuar solo con lo recien desbloqueado
```

Git: seguir el perfil "conservador" documentado en `CLAUDE.md` — no hacer
commit/push sin autorizacion explicita de la sesion actual.
