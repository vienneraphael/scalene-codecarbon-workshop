import polars as pl

def mean_nombre_etablissements(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
    pl.mean_horizontal(pl.col("^nombre_d_etablissements_.*$")).alias("mean_nombre_d_etablissements")
    ).select(pl.all().exclude("^nombre_d_etablissements.*$"))

def mean_effectifs_salaries(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
    pl.mean_horizontal(pl.col("^effectifs_salaries.*$")).alias("mean_effectifs_salaries"),
    ).select(pl.all().exclude("^effectifs_salaries.*$"))

def aggregate_regions(df: pl.DataFrame) -> pl.DataFrame:
    return df.group_by("region").agg(
    pl.col(["^nombre_d_etablissements_.*$", "^effectifs_salaries_.*$"]).sum(),
    pl.col("departement").unique().alias("departements_uniques"),
    pl.col("ape").value_counts(sort=True).head(3).alias("top_3_ape"),
    pl.col("commune").value_counts(sort=True).head(3).alias("top_3_commune")
    )

def main():
    df = pl.read_parquet("urssaf_data_x10.parquet")
    df.pipe(
        aggregate_regions
    ).pipe(
        mean_effectifs_salaries
    ).pipe(
        mean_nombre_etablissements
    )

if __name__ == "__main__":
    main()