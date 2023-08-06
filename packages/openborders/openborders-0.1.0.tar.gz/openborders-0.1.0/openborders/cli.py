import typer
import pandas as pd
import numpy as np

from .utils import Root, Path, Pkg, Data
from .indices import DataIndex, console
from .data import DIMS_DB_PATH, Dimensions
from .indices import spinner

app = typer.Typer(
    name="openborders",
    help="A small toolbox to make open-borders metrics using World Bank (& ILO) data.",
    add_completion=True,
    no_args_is_help=True,
    rich_help_panel='rich',
    rich_markup_mode='rich'
)

@app.command(name="rm", help="Wipe existing cached information if it exists. Alias for `reset`.")
@app.command(name="wipe", help="Wipe existing cached information if it exists. Alias for `reset`.")
@app.command(name="empty", help="Wipe existing cached information if it exists. Alias for `reset`.")
@app.command(name="reset", help="Wipe existing cached information if it exists. Alias for `reset`.")
def reset_cache():
    di = DataIndex()
    di.wipe()
    console.print("[green]✅ Done: local cache wiped.")
    
@app.command(name="load", help="Load data from World Bank & GDIM to be used subsequently.")
def load_cache():
    di = DataIndex()
    console.print("[green]✅ Done: local cache loaded.[/green]")
    statres = DIMS_DB_PATH.stat()
    size = statres.st_size / 1e6
    console.print(f"[yellow]📦 Cache size: {size:.3f} Mb[/yellow]")
    console.print(f"[yellow]📦 Cache location: [dim]{DIMS_DB_PATH}[/dim][/yellow]")

    
@app.command(name="show", help="Show loaded data from World Bank & GDIM to be used subsequently.")
def show_cache(
    indicator: str = typer.Option(None, '-i', '--indicator', help="Filter the view on an indicator"),
    list_indicators: bool = typer.Option(False, '-li', '--list-indicators', help="List available indicators"),
    preprocess: bool = typer.Option(False, '-pp', '--pre-process', help="Whether to preprocess the raw cache data & display the results of the aggregation instead."),
    ygt: int = typer.Option(1990, '-ygt', '--year-greater', help="Whether to filter on years greater than {value}"),
    out: str = typer.Option(None, '-o', '--outfile', help="Output the result as a flat file. (Formats: .csv, .xlsx, .json)"),
    desc: bool = typer.Option(False, '-d', '--desc', help="Add description column to the resulting table.")
    ):
    di = DataIndex()
    df = di.to_df()
    if list_indicators:
        v = df.indicator.unique()
        v = ' (+) ' + '\n (+) '.join(v)
    elif indicator:
        v = df[df.indicator == indicator]
    else:
        v = df
        
    if preprocess:
        v = di.preprocess().aggs
    if not desc:
        cols = [c for c in df.columns if 'description' not in c]
        v = v.loc[:,cols].copy()
    if ygt:
        v.loc[:,'year'] = pd.to_datetime(v.year)
        ygt = pd.to_datetime(f"01-01-{ygt}", dayfirst=True)
        v = v.loc[v.year >= ygt, :].copy()
    
    console.print(v)
    console.print("\n[dim]Use [red]`show -i {indicator}`[/red] to filter on one of these values[/dim]")
    if out is not None:
        out = Path(out)
        match out.suffix:
            case '.csv':
                df.to_csv(out, index=False)
            case '.xlsx':
                df.to_excel(out, engine="openpyxl", index=False)
            case '.json':
                df.to_json(out, orient='records')
            case _:
                if str(out) == '':
                    out = Path('result.csv')
                else:
                    out = Path(out).with_suffix('.csv')
                df.to_csv(out, index=False)
                
    
@app.command(name="preprocess", help="Preprocess loaded data from World Bank & GDIM to be used subsequently.")
def preprocess(
    indicator: str = typer.Option(None, '-i', '--indicator', help="Filter the view on an indicator"),
    list_indicators: bool = typer.Option(False, '-li', '--list-indicators', help="List available indicators"),
    ygt: int = typer.Option(1990, '-ygt', '--year-greater', help="Whether to filter on years greater than {value}"),
    dropna: bool = typer.Option(False, '-dna', '--drop-na', help="Whether to drop NA values."),
    normalize: bool = typer.Option(False, '-n', '--norm', help="Whether to scale every metric to [0,1] using the per-country"),
    out: str = typer.Option(None, '-o', '--outfile', help="Output the result as a flat file. (Formats: .csv, .xlsx, .json)"),
    debug: bool = typer.Option(False, '-d', '--debug', help="Debug using log statements at each inner loop operation.")
    ):
    di = DataIndex()
    df = di.to_df()
    if ygt:
        df.year = pd.to_datetime(df.year)
        ygt = pd.to_datetime(f"01-01-{ygt}", dayfirst=True)
        v = df[df.year >= ygt].copy()
    if list_indicators:
        v = df.indicator.unique()
        v = ' (+) ' + '\n (+) '.join(v)
    elif indicator:
        v = df[df.indicator == indicator]
    else:
        v = df        

    if normalize:
        spinner.start()
        years = pd.date_range(v.year.min(), v.year.max(), freq='5Y')
        nints = len(years) - 1
        intervals = zip(years, years[1:])
        indicators = v.indicator.unique()
        normalizing = spinner.add_task("[bold red]Normalizing data 📊[/bold red]", total=len(indicators)*nints)
        newcols = ['min', 'max', 'mean', 'std', 'norm_value', 'minmax_value']
        
        for nc in newcols:
            v[nc] = pd.NA
        for start, stop in spinner.track(intervals, nints, description="[bold magenta]Normalizing per period..[/bold magenta]"):
            intv = spinner.add_task(f"[yellow] Interval: {start:%d.%m.%Y} <= dt <= {stop:%d.%m.%Y} [/yellow]", total=len(indicators))
            for ind in indicators:
                indt = spinner.add_task(f"Indicator: {ind}", total=None)
                colfilter = (v.year <= stop) & (v.year >= start) & (v.indicator == ind)
                indval = v.loc[colfilter, 'indicator_value']
                indval = indval.apply(lambda v: np.nan if v == '' else float(v)).dropna()

                vmax, vmin, mean, std = indval.max(), indval.min(), indval.mean(), indval.std()
                rg = vmax - vmin
                minmax = (indval - vmin) / (rg+1e-09)
                zscore = (indval - mean) / (std+1e-09)
                newvals = [vmin, vmax, mean, std, zscore, minmax]
                
                if debug:
                    console.log(f"Interval: {start} <= dt <= {stop} | Values: {vmin} <= v <= {vmax} | Z-score: v ≈ μ ± σ ≈ {mean:.2f} ± {std:.2f}")
                
                for nc, nv in zip(newcols, newvals):
                    v.loc[colfilter, nc] = nv
                spinner.update(normalizing, advance=1)
                spinner.update(intv, advance=1)
                spinner.refresh()
                spinner.remove_task(indt)
            spinner.remove_task(intv)
        spinner.remove_task(normalizing)
        
    if dropna:
        v = v.dropna()
        
    console.print(v)
    console.print("\n[dim]Use [red]`show -i {indicator}`[/red] to filter on one of these values[/dim]")
    if out is not None:
        out = Path(out)
        match out.suffix:
            case '.csv':
                df.to_csv(out, index=False)
            case '.xlsx':
                df.to_excel(out, engine="openpyxl", index=False)
            case '.json':
                df.to_json(out, orient='records')
            case _:
                if str(out) == '':
                    out = Path('result.csv')
                else:
                    out = Path(out).with_suffix('.csv')
                df.to_csv(out, index=False)