# Cómo contribuir

La guía vive en `GUIA.md`; el sitio (`index.html`) se genera a partir de él. No edites `index.html` a mano.

## Cambiar el contenido

1. Edita `GUIA.md`.
2. Si un dato no está verificado, márcalo con `**Sin verificar:**` y agrégalo a la tabla "Pendientes por verificar" con su fuente.
3. Abre un pull request. El workflow `build` regenera `index.html` y el workflow `test` corre las pruebas.

Para ver el sitio localmente:

```sh
pip install markdown
python3 build.py
python3 -m http.server 8000
```

## Actualizar una tasa o parámetro

Las tasas del simulador están en `assets/params.json`, cada una con valor, fecha de verificación y fuente.

- **UF**: se actualiza sola cada lunes (workflow `update-uf`).
- **SIS, ATEP/SANNA, tope en UF, UTA**: lanza el workflow `update-tasas` desde la pestaña Actions e indica la tasa, el valor (decimal: `0.02` = 2%), desde cuándo rige y la fuente.
- Si cambia una tasa, actualiza también el texto y los ejemplos de `GUIA.md`, y los valores por defecto de `assets/simulador.js`. La prueba `params.json es consistente` avisa si quedan distintos.

## Pruebas

```sh
npm install
node --test
```

Las pruebas comparan el simulador con los ejemplos de la guía, con la tabla de tramos de la guía y con la librería `tax-cl` para el impuesto global complementario.

## Commits y pull requests

Usa commits semánticos (`feat:`, `fix:`, `docs:`, `style:`, `chore:`) y títulos de PR en el mismo formato.

## Recordatorios automáticos

- `links`: revisa los enlaces de la guía cada mes y abre un issue si hay rotos.
- `revision-semestral`: en enero y julio abre un issue para revisar SIS, tope imponible y retención.
