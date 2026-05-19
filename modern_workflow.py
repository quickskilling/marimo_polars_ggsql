import marimo

__generated_with = "0.23.6"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import polars as pl
    import ggsql

    import io
    import requests

    return ggsql, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Getting started with Marimo and ggsql
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Create a simple `render_marimo()` method

    Some added features to change the theme of the chart
    """)
    return


@app.cell
def _(ggsql):
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


    return (render_marimo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load Simple Polars DataFrame
    """)
    return


@app.cell
def _(pl):

    df = pl.DataFrame({
        "x": [1, 2, 3, 4, 5],
        "y": [10, 20, 15, 30, 25],
        "category": ["A", "B", "A", "B", "A"]
    })

    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Example that works
    """)
    return


@app.cell
def _(df, ggsql):
    # Example that works
    chart = ggsql.render_altair(df, "VISUALISE x, y DRAW point")
    chart = chart.properties(width=300, height=300)

    chart.display() 
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Example that doesn't work
    """)
    return


@app.cell
def _(df, ggsql):
    # Example that doesn't work
    chart1 = ggsql.render_altair(df, "VISUALISE x, y DRAW point")
    chart1.display(width=300, height=300) 
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Using the `render_marimo()` function

    The rest of this example will use `render_marimo()`
    """)
    return


@app.cell
def _(df, render_marimo):
    render_marimo(df, "VISUALISE x, y DRAW point")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Exploring ggsql
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Line Chart

    [Line Charts in ggsql](https://ggsql.org/gallery/examples/line-chart.html)
    """)
    return


@app.cell
def _(pl):
    names = pl.read_parquet("https://posit.byui.edu/names_year/names_year.parquet")
    return (names,)


@app.cell
def _(mo, names):
    mo.ui.table(names,max_columns=60, max_height=250)
    return


@app.cell
def _(names, pl, render_marimo):
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
    return


@app.cell
def _(mo, names, pl):
    mo.ui.table(names\
        .filter(pl.col('name').is_in(['John', 'Jay']))\
        .with_columns(pl.date(pl.col('year'), 1,1).alias('year')),max_columns=60, max_height=250)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - [Specify aesthetic scaling with SCALE – ggsql](https://ggsql.org/syntax/clause/scale.html)
    - [SCALE – ggsql](https://ggsql.org/syntax/scale/type/ordinal.html)
    - [Define different titles with LABEL – ggsql](https://ggsql.org/syntax/clause/label.html)
    """)
    return


@app.cell
def _(names, pl, render_marimo):
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
    return


@app.cell
def _(names, pl, render_marimo):
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
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Box Plots and Jitter Plots

    - [Box plots – ggsql](https://ggsql.org/gallery/examples/boxplot.html)
    - [Jitter – ggsql](https://ggsql.org/syntax/layer/position/jitter.html#examples)
    """)
    return


@app.cell
def _(names, pl):
    names\
        .select('name', 'Total', 'year')\
        .filter(pl.col('name').is_in(['John', 'Jay', 'Joel', 'David', 'Ethan', 'Donovan']))
    return


@app.cell
def _(names, pl, render_marimo):
    grammar_bp = '''
    VISUALISE name AS x, Total as y
        DRAW point
         SETTING position => 'jitter'
    '''

    render_marimo(
        names\
            .filter(pl.col('name').is_in(['John', 'Jay', 'Joel', 'David', 'Ethan', 'Donovan'])),
        grammar_bp)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
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
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
