# %%
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

df_hospitalisations_france = pd.read_csv(
    Path(__file__).parent / "data" / "gestes-auto-infliges-hospitalisations-france.csv",
)
df_hospitalisations_france.columns = df_hospitalisations_france.columns.str.lstrip(
    "\ufeff"
).str.strip()
sejours_femmes_ages = (
    df_hospitalisations_france.loc[
        df_hospitalisations_france["Sexe"].eq("Femmes")
        & df_hospitalisations_france["Classe d'âge"].ne("Tous")
    ]
    .pivot(
        index="Année",
        columns="Classe d'âge",
        values="Nombre de séjours pour geste auto-infligé",
    )
    .sort_index()
)
sejours_femmes_ages["11-17 ans"] = sejours_femmes_ages[["11-14 ans", "15-17 ans"]].sum(
    axis=1
)
sejours_femmes_ages = sejours_femmes_ages.drop(
    columns=["11-14 ans", "15-17 ans"],
)
ordre_ages_hospitalisations = [
    "00-10 ans",
    "11-17 ans",
    "18-24 ans",
    "25-44 ans",
    "45-64 ans",
    "65-84 ans",
    "85 ans et plus",
]

fig_hospitalisations_femmes_ages, ax_hospitalisations_femmes_ages = plt.subplots(
    figsize=(12, 6),
    layout="constrained",
)

for classe_age in ordre_ages_hospitalisations:
    mis_en_evidence = classe_age == "11-17 ans"
    ax_hospitalisations_femmes_ages.plot(
        sejours_femmes_ages.index,
        sejours_femmes_ages[classe_age],
        label=classe_age,
        color="#D62728" if mis_en_evidence else "#A0A0A0",
        marker="o" if mis_en_evidence else None,
        linewidth=3 if mis_en_evidence else 1.5,
        zorder=3 if mis_en_evidence else 2,
    )

ax_hospitalisations_femmes_ages.set_xlabel("Année")
ax_hospitalisations_femmes_ages.set_ylabel("Nombre de séjours hospitaliers")
ax_hospitalisations_femmes_ages.set_title(
    "Évolution des hospitalisations chez les femmes par classe d'âge",
)
ax_hospitalisations_femmes_ages.set_xticks(sejours_femmes_ages.index)
ax_hospitalisations_femmes_ages.set_ylim(bottom=0)
ax_hospitalisations_femmes_ages.legend(title="Classe d'âge")
ax_hospitalisations_femmes_ages.grid(axis="y", alpha=0.25)
ax_hospitalisations_femmes_ages.set_axisbelow(True)
plt.show()
tableau_hospitalisations_femmes = sejours_femmes_ages[
    ordre_ages_hospitalisations
].copy()

tableau_hospitalisations_femmes.index.name = "Année"
tableau_hospitalisations_femmes.columns.name = "Classe d'âge"

print("Nombre de séjours hospitaliers pour geste auto-infligé chez les femmes")
print(tableau_hospitalisations_femmes.to_string())

# %%
df_suicides_france = pd.read_csv(
    Path(__file__).parent / "data" / "suicides-deces-france.csv",
)
df_suicides_france.columns = df_suicides_france.columns.str.lstrip("\ufeff").str.strip()
deces_hommes_ages = (
    df_suicides_france.loc[
        df_suicides_france["Sexe"].eq("Hommes")
        & df_suicides_france["Classe d'âge"].ne("Tous")
    ]
    .pivot(
        index="Année",
        columns="Classe d'âge",
        values="Nombre de décès",
    )
    .sort_index()
)
ordre_ages_suicides = [
    "00-10 ans",
    "11-14 ans",
    "15-17 ans",
    "18-24 ans",
    "25-44 ans",
    "45-64 ans",
    "65-84 ans",
    "85 ans et plus",
]

fig_suicides_hommes_ages, ax_suicides_hommes_ages = plt.subplots(
    figsize=(12, 6),
    layout="constrained",
)

for classe_age in ordre_ages_suicides:
    ax_suicides_hommes_ages.plot(
        deces_hommes_ages.index,
        deces_hommes_ages[classe_age],
        label=classe_age,
        marker="o",
        linewidth=2,
    )

ax_suicides_hommes_ages.set_xlabel("Année")
ax_suicides_hommes_ages.set_ylabel("Nombre de décès par suicide")
ax_suicides_hommes_ages.set_title(
    "Évolution des décès par suicide chez les hommes par classe d'âge",
)
ax_suicides_hommes_ages.set_xticks(deces_hommes_ages.index)
ax_suicides_hommes_ages.set_ylim(bottom=0)
ax_suicides_hommes_ages.legend(title="Classe d'âge")
ax_suicides_hommes_ages.grid(axis="y", alpha=0.25)
ax_suicides_hommes_ages.set_axisbelow(True)
plt.show()

# %%
