# Consignes 

Dans cette activité, nous allons utiliser les données de l'Urssaf donnat accès au nombre d'établissements employeurs et effectifs salariés du secteur privé par commune x APE (2006-2022) : https://open.urssaf.fr/explore/dataset/etablissements-et-effectifs-salaries-au-niveau-commune-x-ape-last/api/


Voici un aperçu du jeu de données, filtré sur les colonnes qui nous intéressent particulièrement:

shape: (1_155_227, 38)
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┬───┬────────────┬────────────┬────────────┬────────────┬────────────┐
│ region      ┆ ape         ┆ departement ┆ commune     ┆ nombre_d_et ┆ … ┆ effectifs_ ┆ effectifs_ ┆ effectifs_ ┆ effectifs_ ┆ effectifs_ │
│ ---         ┆ ---         ┆ ---         ┆ ---         ┆ ablissement ┆   ┆ salaries_2 ┆ salaries_2 ┆ salaries_2 ┆ salaries_2 ┆ salaries_2 │
│ str         ┆ str         ┆ str         ┆ str         ┆ s_2006      ┆   ┆ 018        ┆ 019        ┆ 020        ┆ 021        ┆ 022        │
│             ┆             ┆             ┆             ┆ ---         ┆   ┆ ---        ┆ ---        ┆ ---        ┆ ---        ┆ ---        │
│             ┆             ┆             ┆             ┆ i64         ┆   ┆ i64        ┆ i64        ┆ i64        ┆ i64        ┆ i64        │
╞═════════════╪═════════════╪═════════════╪═════════════╪═════════════╪═══╪════════════╪════════════╪════════════╪════════════╪════════════╡
│ Bretagne    ┆ 4332A       ┆ Ille-et-Vil ┆ Moutiers    ┆ 1           ┆ … ┆ 10         ┆ 9          ┆ 9          ┆ 9          ┆ 9          │
│             ┆ Travaux de  ┆ aine        ┆             ┆             ┆   ┆            ┆            ┆            ┆            ┆            │
│             ┆ menuiserie  ┆             ┆             ┆             ┆   ┆            ┆            ┆            ┆            ┆            │
│             ┆ bo…         ┆             ┆             ┆             ┆   ┆            ┆            ┆            ┆            ┆            │
│ Pays de la  ┆ 4729Z       ┆ Loire-Atlan ┆ Pontchâteau ┆ null        ┆ … ┆ null       ┆ 1          ┆ 3          ┆ 6          ┆ 5          │
│ Loire       ┆ Autres      ┆ tique       ┆             ┆             ┆   ┆            ┆            ┆            ┆            ┆            │
│             ┆ commerces   ┆             ┆             ┆             ┆   ┆            ┆            ┆            ┆            ┆            │
│             ┆ de déta…    ┆             ┆             ┆             ┆   ┆            ┆            ┆            ┆            ┆            │
│ Bretagne    ┆ 4399C       ┆ Ille-et-Vil ┆ Moutiers    ┆ 1           ┆ … ┆ 1          ┆ 1          ┆ null       ┆ null       ┆ null       │
│             ┆ Travaux de  ┆ aine        ┆             ┆             ┆   ┆            ┆            ┆            ┆            ┆            │
│             ┆ maçonnerie  ┆             ┆             ┆             ┆   ┆            ┆            ┆            ┆            ┆            │
│             ┆ gé…         ┆             ┆             ┆             ┆   ┆            ┆            ┆            ┆            ┆            │
│ Pays de la  ┆ 4742Z Comm. ┆ Loire-Atlan ┆ Pontchâteau ┆ null        ┆ … ┆ 1          ┆ 2          ┆ 1          ┆ null       ┆ null       │
│ Loire       ┆ détail      ┆ tique       ┆             ┆             ┆   ┆            ┆            ┆            ┆            ┆            │
│             ┆ matériels   ┆             ┆             ┆             ┆   ┆            ┆            ┆            ┆            ┆            │
│             ┆ t…          ┆             ┆             ┆             ┆   ┆            ┆            ┆            ┆            ┆            │
│ Bretagne    ┆ 4519Z       ┆ Ille-et-Vil ┆ Moutiers    ┆ null        ┆ … ┆ null       ┆ null       ┆ null       ┆ 1          ┆ 1          │
...
│             ┆ Coiffure    ┆             ┆             ┆             ┆   ┆            ┆            ┆            ┆            ┆            │
│ La Réunion  ┆ 9602B Soins ┆ La Réunion  ┆ Cilaos      ┆ null        ┆ … ┆ null       ┆ null       ┆ null       ┆ null       ┆ null       │
│             ┆ de beauté   ┆             ┆             ┆             ┆   ┆            ┆            ┆            ┆            ┆            │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┴───┴────────────┴────────────┴────────────┴────────────┴────────────┘

L'objectif de cette activité est de créer les colonnes suivantes dans le jeu de données:
0. `region`: la région sur laquelle porte nos indicateurs.
1. `mean_nombre_d_etablissements`: moyenne temporelle sur toutes les années disponibles, du nombre d'établissements par région.
2. `mean_effectifs_salaries`: moyenne temporelle sur toutes les années disponibles, de l'effectif de salariés par région.
3. `departements_uniques`: départements uniques par région
4. `top_3_ape`: les 3 ape (catégories d'entreprises) les plus représentés, par région.
5. `top_3_commune`: les 3 communes les plus actives par région.