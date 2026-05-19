---
title: Modern Workflow
marimo-version: 0.23.6
width: full
---

```python {.marimo}
import marimo as mo
```

```python {.marimo}
import polars as pl
import ggsql

import io
import requests
```

# Getting started with Marimo and ggsql
<!---->
## Notes on rendering in Marimo

As of 5/1925, [ggsql](https://ggsql.org/get_started/tooling/python.html) provides an example for use with Python in Jupyter. It doesn't work for Marimo. You can see notes on two issues that discuss this point.

- [ggsql for Python](https://github.com/posit-dev/ggsql-python/issues/7)
- [Marimo render conversation](https://github.com/marimo-team/marimo/issues/9320)

Notice the `chart.properties(width=300, height=300)` to get the chart to display in Marimo. The guidance from the issue in Marimo didn't work for me. This guidance said to use `chart1.display(width=300, height=300)`.

This workbook will use `render_marimo()` to render the ggsql visualizations.  The full function is;

```python
def render_marimo(df, viz, width = 600, height = 300, **kwargs):
    chart = ggsql.render_altair(df, viz, **kwargs)
    return chart.properties(width=width, height=height)
```
<!---->
## Create a simple `render_marimo()` method

Some added features to change the theme of the chart

```python {.marimo}
# def render_marimo(df, viz, width = 600, height = 300, **kwargs):
#     chart = ggsql.render_altair(df, viz, **kwargs)
#     return chart.properties(width=width, height=height)

def render_marimo(df, viz, width=600, height=300, **kwargs):
    chart = ggsql.render_altair(df, viz, **kwargs)

    chart = (
        chart
        .configure_view(
            fill="white",        # plot area background
            stroke="transparent" # remove grey border if present
        )
        .configure(
            background="white"   # outer chart background
        )
        .properties(width=width, height=height)
    )

    return chart
```

## Load Simple Polars DataFrame

```python {.marimo}
df = pl.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [10, 20, 15, 30, 25],
    "category": ["A", "B", "A", "B", "A"]
})
```

### Example that works

```python {.marimo}
# Example that works
chart = ggsql.render_altair(df, "VISUALISE x, y DRAW point")
chart = chart.properties(width=300, height=300)

chart.display()
```

### Example that doesn't work

```python {.marimo}
# Example that doesn't work
chart1 = ggsql.render_altair(df, "VISUALISE x, y DRAW point")
chart1.display(width=300, height=300)
```

### Using the `render_marimo()` function

The rest of this example will use `render_marimo()`

```python {.marimo}
render_marimo(df, "VISUALISE x, y DRAW point")
```

# Exploring ggsql
<!---->
## Line Chart

[Line Charts in ggsql](https://ggsql.org/gallery/examples/line-chart.html)

```python {.marimo}
names = pl.read_parquet("https://posit.byui.edu/names_year/names_year.parquet")
```

```python {.marimo}
mo.ui.table(names,max_columns=60, max_height=250)
```

```python {.marimo}
# Visualize Command
grammar = '''
VISUALISE year as x, UT as y, name as color
DRAW line
SCALE ORDINAL color
LABEL
    title => 'Plot of Name Distribution',
    x => 'Year',
    y => 'Count of Names',
    color => 'Baby Name'
'''

render_marimo(names.filter(pl.col('name').is_in(['John', 'Jay'])), grammar)
```

```python {.marimo}
mo.ui.table(names\
    .filter(pl.col('name').is_in(['John', 'Jay']))\
    .with_columns(pl.date(pl.col('year'), 1,1).alias('year')),max_columns=60, max_height=250)
```

- [Specify aesthetic scaling with SCALE – ggsql](https://ggsql.org/syntax/clause/scale.html)
- [SCALE – ggsql](https://ggsql.org/syntax/scale/type/ordinal.html)
- [Define different titles with LABEL – ggsql](https://ggsql.org/syntax/clause/label.html)

```python {.marimo}
# Note that the color doesn't change the legend title but doesn't error
grammar_date = '''
VISUALISE year as x, UT as y, name as color
DRAW line
SCALE ORDINAL color
SCALE x VIA date
    RENAMING * => '{:time %Y}'
LABEL
    title => 'Plot of Name Distribution',
    x => 'Year',
    y => 'Count of Names',
    color => 'Baby Name'
'''

render_marimo(
    names\
        .filter(pl.col('name').is_in(['John', 'Jay']))\
        .with_columns(pl.date(pl.col('year'), 1,1).alias('year')),
    grammar_date)
```

```python {.marimo}
# Note that the color doesn't change the legend title but doesn't error
grammar_date_facet = '''
VISUALISE year as x, UT as y, name as color
DRAW line
FACET name SETTING free => 'x'
SCALE ORDINAL color
SCALE x VIA date
    RENAMING * => '{:time %Y}'
LABEL
    title => 'Plot of Name Distribution',
    x => 'Year',
    y => 'Count of Names',
    color => 'Baby Name'
'''
# simple function doesn't handle facet well
render_marimo(
    names\
        .filter(pl.col('name').is_in(['John', 'Jay']))\
        .with_columns(pl.date(pl.col('year'), 1,1).alias('year')),
    grammar_date_facet)
```

## Box Plots and Jitter Plots

- [Box plots – ggsql](https://ggsql.org/gallery/examples/boxplot.html)
- [Jitter – ggsql](https://ggsql.org/syntax/layer/position/jitter.html#examples)

```python {.marimo}
names\
    .select('name', 'Total', 'year')\
    .filter(pl.col('name').is_in(['John', 'Jay', 'Joel', 'David', 'Ethan', 'Donovan']))
```

```python {.marimo}
grammar_bp = '''
VISUALISE name AS x, Total as y
    DRAW point
     SETTING position => 'jitter'
'''

render_marimo(
    names\
        .filter(pl.col('name').is_in(['John', 'Jay', 'Joel', 'David', 'Ethan', 'Donovan'])),
    grammar_bp)
```

## [From grammar to syntax](https://ggsql.org/get_started/wrap_up.html#from-grammar-to-syntax)

To help you in your further learning, we provide an overview of where the different grammar components fit into the ggsql syntax. Use this as a reference when you explore the full documentation.

| Grammar     | Syntax                                                       |
| ----------- | ------------------------------------------------------------ |
| Data        | Data can be specified in several places:`SELECT … FROM …` (the SQL portion before `VISUALISE`) gets injected as the global data)`VISUALIZE ... FROM ...` (the global data source can be specified as part of the [`VISUALIZE` clause](https://ggsql.org/syntax/clause/visualise.html))`MAPPING ... FROM ...` (the layer data source can be specified as part of the mapping in the [`DRAW` clause](https://ggsql.org/syntax/clause/draw.html)) |
| Mappings    | Mappings also exist in multiple places in the syntax`... AS ...` following [`VISUALIZE`](https://ggsql.org/syntax/clause/visualise.html) sets global mapping that layers inherit.`... AS ...` following `MAPPING` in the [`DRAW`](https://ggsql.org/syntax/clause/draw.html) clause sets layer specific mapping, potentially overriding the inherited global mapping.`... AS ...` following `REMAPPING` in the [`DRAW`](https://ggsql.org/syntax/clause/draw.html) clause defines how data created by the statistics gets mapped in the layer. |
| Statistics  | Statistics are implicitly part of the layer created with [`DRAW`](https://ggsql.org/syntax/clause/draw.html). Each layer has their own statistics transformation hard-wired. |
| Scales      | ggsql provides default scales as needed, but these can be overridden with the [`SCALE`](https://ggsql.org/syntax/clause/scale.html) clause. |
| Geometries  | Geometries are inherent to the layers created with [`DRAW`](https://ggsql.org/syntax/clause/draw.html) and [`PLACE`](https://ggsql.org/syntax/clause/place.html). Each layer has a specific geometry and some layers may share the same geometry (e.g. [histogram](https://ggsql.org/syntax/layer/type/histogram.html) and [bar](https://ggsql.org/syntax/layer/type/bar.html)). |
| Facets      | Facets are created with the [`FACET`](https://ggsql.org/syntax/clause/facet.html) clause. The default facet creates a single view showing all the data. |
| Coordinates | Coordinate systems are defined using [`PROJECT`](https://ggsql.org/syntax/clause/project.html) but can also be derived from the mapping. If you map to `x` and `y`, ggsql knows you are using a Cartesian coordinate system and if you map to `angle` and `radius` it knows you want a polar coordinate system. |
| Theme       | Currently not supported.                                     |

```python {.marimo}

```


#### Commands to get it set up

_These have already been done in this repo._

1. Created the repo on Github and then clones
2. `uv init .` in the base folder and then delete the `main.py` file.
3. Then add `package = false` under `[tool.uv]` in the `pyproject.toml` as this will not be a package.
4. Now run the following uv command in terminal: `uv add marimo[edit,recommended] polars ggsql `