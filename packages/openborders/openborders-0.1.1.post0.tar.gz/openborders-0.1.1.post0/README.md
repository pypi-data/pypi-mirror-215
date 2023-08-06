# Open Borders Toolbox

## A python toolbox making open-borders metrics easier !

![](https://i.imgur.com/4UCAuYd.png)

## One-liner CLI

If you just want a CSV/JSON/Excel file with the metrics, don't bother, just go

```bash
opbd preprocess -n -o open-borders-index.csv
```

* `-n` means normalize actross countries
* `-o` means output to file, extension is detected (`.csv`|`.xlsx`|`.json`)


## Example result

A sample CSV file can be found [here](tests/open-borders-index.csv)

## Credits

This toolbox heavily relies on the work from the folks at [wbdata](https://github.com/OliverSherouse/wbdata) and overall APIs of
international organisations:

- [World Bank API](https://data.worldbank.org/)
- [World Bank's GDIM][1] which is the Global Database on Intergenerational Mobility


[1]:https://datacatalog.worldbank.org/search/dataset/0050771/Global-Database-on-Intergenerational-Mobility
