import polars as pl
import pandas as pd

# EN POLARS
def mean_nombre_etablissements_polars(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
    pl.mean_horizontal(pl.col("^nombre_d_etablissements_.*$")).alias("mean_nombre_d_etablissements")
    ).select(pl.all().exclude("^nombre_d_etablissements.*$"))

def mean_effectifs_salaries_polars(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
    pl.mean_horizontal(pl.col("^effectifs_salaries.*$")).alias("mean_effectifs_salaries"),
    ).select(pl.all().exclude("^effectifs_salaries.*$"))

def aggregate_regions_polars(df: pl.DataFrame) -> pl.DataFrame:
    return df.group_by("region").agg(
    pl.col(["^nombre_d_etablissements_.*$", "^effectifs_salaries_.*$"]).sum(),
    pl.col("departement").unique().alias("departements_uniques"),
    pl.col("ape").value_counts(sort=True).head(3).alias("top_3_ape"),
    pl.col("commune").value_counts(sort=True).head(3).alias("top_3_commune")
    )

def main1():
    df = pl.read_parquet("donnee_urssaf.parquet")
    df.pipe(
        aggregate_regions_polars
    ).pipe(
        mean_effectifs_salaries_polars
    ).pipe(
        mean_nombre_etablissements_polars
    )


        
# En PANDAS
def mean_nombre_etablissements_pandas(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function computes the mean number of etablissements.

    Args:
        df (pd.DataFrame): The urssaf dataframe.
    
    Returns:
        The urssaf dataframe with the mean number of etablissements computed
    """
    df['mean_nombre_d_etablissements'] = df.filter(regex='^nombre_d_etablissements_.*$').mean(axis=1)
    return df.drop(columns=df.filter(regex='^nombre_d_etablissements_.*$').columns)

def mean_effectifs_salaries_pandas(df: pd.DataFrame) -> pd.DataFrame:
    df['mean_effectifs_salaries'] = df.filter(regex='^effectifs_salaries.*$').mean(axis=1)
    return df.drop(columns=df.filter(regex='^effectifs_salaries.*$').columns)

def aggregate_regions_pandas(df: pd.DataFrame) -> pd.DataFrame:
    # Sélectionner les colonnes qui correspondent aux motifs avec des expressions régulières
    nombre_d_etablissements_cols = df.filter(regex='^nombre_d_etablissements_.*$').columns
    effectifs_salaries_cols = df.filter(regex='^effectifs_salaries_.*$').columns

    # Définir les fonctions d'agrégation pour chaque groupe de colonnes
    agg_dict = {col: 'sum' for col in nombre_d_etablissements_cols}
    agg_dict.update({col: 'sum' for col in effectifs_salaries_cols})
    agg_dict.update({
        'departement': lambda x: list(pd.unique(x)),
        'ape': lambda x: x.value_counts().head(3).to_dict(),
        'commune': lambda x: x.value_counts().head(3).to_dict()
    })

    # Appliquer l'agrégation
    aggregated_df = df.groupby('region').agg(agg_dict).reset_index()

    return aggregated_df

def main2():
    df = pd.read_parquet("donnee_urssaf.parquet")
    df = (df.pipe(aggregate_regions_pandas)
          .pipe(mean_effectifs_salaries_pandas)
          .pipe(mean_nombre_etablissements_pandas))
    return df

if __name__ == "__main__":
    #df = main1()
    df = main2()
    #display(df)