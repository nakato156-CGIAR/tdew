# Reconstrucción continua de Td

Este paquete implementa el protocolo de reconstrucción continua de Td,
independiente del protocolo Td(t+1) de la semana 1. Los módulos están
organizados en capas: contrato del protocolo, datos, modelado, ejecución
y evaluación.

## Contrato del protocolo

- `protocol.py`: fronteras de fecha congeladas (`Protocol.DEV_A`,
  `DEV_B`, `LL4`, `PRODUCTION`) y las funciones guarda
  (`require_protocol_access`) que impiden leer datos fuera del horizonte
  permitido para cada fase.

## Datos

- `data.py`: validaciones de la tabla canónica, construcción de paneles
  deterministas y features termales causales (incluye `AR_LAGS`, usado
  por los módulos de rollout y de modelado).
- `bucketed.py`: adaptador de la fuente silver. Separa dos operaciones
  costosas en disco: `materialize_silver_buckets` (escanea los TMIN/TMAX
  mensuales y escribe buckets estilo Hive) y `build_canonical_buckets`
  (une un bucket histórico con los buckets silver y los lookups
  espaciales correspondientes). Ninguna de las dos se ejecuta al importar
  el módulo.

## Modelado

- `baselines.py`: baselines de CPU y calibración de shrinkage ajustada
  solo con el split de entrenamiento.
- `rollout.py`: rollouts directos y autorregresivos sin fuga de
  información (leak-safe).
- `tcn.py`: variantes de TCN y las primitivas diferenciables de
  entrenamiento en bucle cerrado (`closed_rollout`, `rollout_loss`).
- `training.py`: bucle de entrenamiento por pasos (no por épocas), con
  validación intra-época y checkpoints exactos.
- `tcn_runner.py`: capa que combina `tcn.py` y `training.py` para
  materializar datos, entrenar e inferir con la TCN de reconstrucción.

## Ejecución

- `cli.py`: interfaz de línea de comandos para correr el protocolo de
  forma manual (baselines, bucketed, rollout y TCN). Es el punto de
  entrada para corridas ad-hoc.
- `zenml_pipeline.py`: orquestación con ZenML sobre `cli.py`,
  `bucketed.py` y `evaluation.py`. Es el punto de entrada para corridas
  orquestadas y reproducibles. Tampoco ejecuta nada al importarse; los
  comandos para lanzar el pipeline deben verificarse contra las rutas de
  origen y la capacidad de almacenamiento disponibles en cada sesión.

## Evaluación

- `evaluation.py`: esquema de las predicciones (`PREDICTION_COLUMNS`),
  métricas, pruebas pareadas y el gate de aprobación final.
- `evaluate.py`: evaluador de línea de comandos para columnas de
  predicción registradas en un manifest.

## Convención de nombres

`evaluate.py` y `evaluation.py` son módulos distintos: `evaluation.py`
contiene la lógica de métricas y `evaluate.py` es el CLI que la invoca,
siguiendo el mismo patrón que `cli.py`/cli de ejecución.
