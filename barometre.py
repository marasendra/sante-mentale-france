# %%
from math import pi
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

df_episodes_depressifs = pd.read_csv(
    Path(__file__).parent
    / "data"
    / "episodes-depressif-indicateurs-du-barometre-2024.csv",
)
df_episodes_depressifs.columns = df_episodes_depressifs.columns.str.lstrip(
    "\ufeff"
).str.strip()

df_trouble_anxieux = pd.read_csv(
    Path(__file__).parent
    / "data"
    / "trouble-anxieux-generalise-indicateurs-du-barometre-2024.csv",
)
df_trouble_anxieux.columns = df_trouble_anxieux.columns.str.lstrip("\ufeff").str.strip()

df_conduites_suicidaires = pd.read_csv(
    Path(__file__).parent
    / "data"
    / "conduites-sucidaires-indicateurs-du-barometre-2024.csv",
)
df_conduites_suicidaires.columns = df_conduites_suicidaires.columns.str.lstrip(
    "\ufeff"
).str.strip()

df_changement_climatique = pd.read_csv(
    Path(__file__).parent
    / "data"
    / "changement-climatique-indicateurs-du-barometre-2024.csv",
)
df_changement_climatique.columns = df_changement_climatique.columns.str.lstrip(
    "\ufeff"
).str.strip()
indicateur_climatique = "A souffert psychologiquement d'un évènement climatique extrême"
df_changement_climatique = df_changement_climatique.loc[
    (df_changement_climatique["Année"] == 2024)
    & (df_changement_climatique["Indicateur"] == indicateur_climatique)
].copy()
for dimension in ("Type de ménage", "Situation professionnelle"):
    df_changement_climatique[dimension] = "Tous"

df_synthese_mental = pd.concat(
    [
        df_conduites_suicidaires,
        df_trouble_anxieux,
        df_episodes_depressifs,
        df_changement_climatique,
    ],
    ignore_index=True,
)
libelles_synthese = {
    "Pensées suicidaires au cours des 12 derniers mois": "Conduites suicidaires : pensées\n(12 derniers mois, %)",
    "Tentative de suicide au cours de la vie": "Conduites suicidaires : tentatives\n(au cours de la vie, %)",
    "Trouble anxieux généralisé": "Trouble anxieux généralisé (%)",
    "Episode dépressif caractérisé": "Épisode dépressif caractérisé (%)",
    "A souffert psychologiquement d'un évènement climatique extrême": "A souffert psychologiquement\nd'un évènement climatique extrême (%)",
}
synthese_tous_ages = df_synthese_mental.loc[
    (df_synthese_mental["Année"] == 2024)
    & (df_synthese_mental["Classe d'âge"] == "Tous")
    & df_synthese_mental["Sexe"].isin(["Hommes", "Femmes"])
    & df_synthese_mental["Indicateur"].isin(libelles_synthese)
    & df_synthese_mental[
        [
            "Nouvelles régions",
            "PCS",
            "Diplôme",
            "Type de ménage",
            "Situation professionnelle",
            "Situation financière perçue",
        ]
    ]
    .eq("Tous")
    .all(axis=1)
]
estimations_synthese = synthese_tous_ages.pivot(
    index="Indicateur",
    columns="Sexe",
    values="Estimation",
).loc[list(libelles_synthese)]

fig_synthese, ax_synthese = plt.subplots(figsize=(14, 8), layout="constrained")
for sexe, couleur, signe in (
    ("Hommes", "#0072B2", -1),
    ("Femmes", "#D55E00", 1),
):
    barres_synthese = ax_synthese.barh(
        list(libelles_synthese.values()),
        signe * estimations_synthese[sexe],
        label=sexe,
        color=couleur,
        height=0.7,
    )
    ax_synthese.bar_label(
        barres_synthese,
        labels=[
            f"{estimation:.2f}"
            if indicateur == "Score moyen de satisfaction de vie actuelle"
            else f"{estimation:.1f} %"
            for indicateur, estimation in estimations_synthese[sexe].items()
        ],
        padding=4,
    )

limite_synthese = estimations_synthese.max().max() * 1.2
ax_synthese.set_xlim(-limite_synthese, limite_synthese)
ax_synthese.invert_yaxis()
ax_synthese.xaxis.set_major_formatter(
    FuncFormatter(lambda valeur, position: f"{abs(valeur):g}"),
)
ax_synthese.axvline(0, color="#333333", linewidth=1)
ax_synthese.set_xlabel("Estimation (score ou %, selon l'indicateur)")
ax_synthese.set_title("Santé mentale en 2024 - Estimations nationales, tous âges")
ax_synthese.legend(title="Sexe", loc="upper left", bbox_to_anchor=(1.02, 1))
ax_synthese.grid(axis="x", alpha=0.25)
ax_synthese.set_axisbelow(True)
plt.show()
# %%
synthese_par_age = df_synthese_mental.loc[
    (df_synthese_mental["Année"] == 2024)
    & df_synthese_mental["Classe d'âge"].notna()
    & df_synthese_mental["Classe d'âge"].ne("Tous")
    & df_synthese_mental["Sexe"].isin(["Hommes", "Femmes"])
    & df_synthese_mental["Indicateur"].isin(libelles_synthese)
    & df_synthese_mental[
        [
            "Nouvelles régions",
            "PCS",
            "Diplôme",
            "Type de ménage",
            "Situation professionnelle",
            "Situation financière perçue",
        ]
    ]
    .eq("Tous")
    .all(axis=1)
]
estimations_radar_ages = synthese_par_age.pivot(
    index=["Sexe", "Classe d'âge"],
    columns="Indicateur",
    values="Estimation",
).loc[:, list(libelles_synthese)]
classes_age_radar = sorted(
    synthese_par_age["Classe d'âge"].unique(),
    key=lambda classe_age: int(classe_age.split("-")[0]),
)
couleurs_radar_ages = dict(
    zip(
        classes_age_radar,
        ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#333333", "#E69F00"],
    )
)
libelles_radar_ages = [
    "Pensées suicidaires\n(12 derniers mois)",
    "Tentative de suicide\n(au cours de la vie)",
    "Trouble anxieux\ngénéralisé",
    "Épisode dépressif\ncaractérisé",
    "A souffert psychologiquement\nd'un évènement climatique\nextrême",
]
angles_radar_ages = [
    2 * pi * position / len(libelles_radar_ages)
    for position in range(len(libelles_radar_ages))
]
angles_radar_fermes = angles_radar_ages + angles_radar_ages[:1]
limite_radar_ages = float(estimations_radar_ages.max().max()) * 1.15

fig_radar_ages, axes_radar_ages = plt.subplots(
    1,
    2,
    figsize=(18, 9),
    subplot_kw={"projection": "polar"},
    layout="constrained",
)
for axe_radar, sexe in zip(axes_radar_ages, ("Hommes", "Femmes")):
    for classe_age in classes_age_radar:
        valeurs_age = estimations_radar_ages.loc[(sexe, classe_age)].tolist()
        axe_radar.plot(
            angles_radar_fermes,
            valeurs_age + valeurs_age[:1],
            label=classe_age,
            color=couleurs_radar_ages[classe_age],
            marker="o",
            linewidth=2,
            markersize=4,
        )
    axe_radar.set_theta_offset(pi / 2)
    axe_radar.set_theta_direction(-1)
    axe_radar.set_xticks(angles_radar_ages, libelles_radar_ages)
    axe_radar.tick_params(axis="x", pad=20, labelsize=10)
    axe_radar.set_ylim(0, limite_radar_ages)
    axe_radar.yaxis.set_major_formatter(
        FuncFormatter(lambda valeur, position: f"{valeur:g} %"),
    )
    axe_radar.set_title(sexe, pad=45)
    axe_radar.grid(alpha=0.3)
    axe_radar.spines["polar"].set_color("#BBBBBB")

fig_radar_ages.suptitle(
    "Santé mentale en 2024 - Estimations nationales par classe d'âge"
)
axes_radar_ages[0].legend(
    title="Classe d'âge",
    loc="upper center",
    bbox_to_anchor=(0.5, -0.18),
    ncol=3,
)
plt.show()

# %%
synthese_par_diplome = df_synthese_mental.loc[
    (df_synthese_mental["Année"] == 2024)
    & df_synthese_mental["Diplôme"].notna()
    & df_synthese_mental["Diplôme"].ne("Tous")
    & df_synthese_mental["Sexe"].isin(["Hommes", "Femmes"])
    & df_synthese_mental["Indicateur"].isin(libelles_synthese)
    & df_synthese_mental[
        [
            "Classe d'âge",
            "Nouvelles régions",
            "PCS",
            "Type de ménage",
            "Situation professionnelle",
            "Situation financière perçue",
        ]
    ]
    .eq("Tous")
    .all(axis=1)
]
estimations_radar_diplomes = synthese_par_diplome.pivot(
    index=["Sexe", "Diplôme"],
    columns="Indicateur",
    values="Estimation",
).loc[:, list(libelles_synthese)]
couleurs_radar_diplomes = {
    "Aucun diplôme ou inférieur au Bac": "#0072B2",
    "Bac": "#D55E00",
    "Supérieur au Bac": "#009E73",
}
limite_radar_diplomes = float(estimations_radar_diplomes.max().max()) * 1.15

fig_radar_diplomes, axes_radar_diplomes = plt.subplots(
    1,
    2,
    figsize=(18, 9),
    subplot_kw={"projection": "polar"},
    layout="constrained",
)
for axe_radar, sexe in zip(axes_radar_diplomes, ("Hommes", "Femmes")):
    for diplome, couleur in couleurs_radar_diplomes.items():
        valeurs_diplome = estimations_radar_diplomes.loc[(sexe, diplome)].tolist()
        axe_radar.plot(
            angles_radar_fermes,
            valeurs_diplome + valeurs_diplome[:1],
            label=diplome,
            color=couleur,
            marker="o",
            linewidth=2,
            markersize=4,
        )
    axe_radar.set_theta_offset(pi / 2)
    axe_radar.set_theta_direction(-1)
    axe_radar.set_xticks(angles_radar_ages, libelles_radar_ages)
    axe_radar.tick_params(axis="x", pad=20, labelsize=10)
    axe_radar.set_ylim(0, limite_radar_diplomes)
    axe_radar.yaxis.set_major_formatter(
        FuncFormatter(lambda valeur, position: f"{valeur:g} %"),
    )
    axe_radar.set_title(sexe, pad=45)
    axe_radar.grid(alpha=0.3)
    axe_radar.spines["polar"].set_color("#BBBBBB")

fig_radar_diplomes.suptitle(
    "Santé mentale en 2024 - Estimations nationales par diplôme"
)
axes_radar_diplomes[0].legend(
    title="Diplôme",
    loc="upper center",
    bbox_to_anchor=(0.5, -0.18),
    ncol=1,
)
plt.show()

# %%
dimensions_socioeconomiques = {
    "Type de ménage": {
        "Couple sans enfant": "Couple sans enfant",
        "Couple avec enfant(s)": "Couple avec enfant(s)",
        "Famille monoparentale": "Famille monoparentale",
        "Ménage d'une seule personne": "Ménage d'une seule personne",
        "Autres": "Autres",
    },
    "Situation financière perçue": {
        "Vous êtes à l’aise": "À l'aise",
        "Ça va": "Ça va",
        "C’est juste, il faut faire attention": "C'est juste, il faut faire attention",
        "Vous y arrivez difficilement ou vous ne pouvez pas y arriver sans faire de dette": "Difficultés financières / endettement",
    },
}
dimensions_filtrage = [
    "Classe d'âge",
    "Nouvelles régions",
    "PCS",
    "Diplôme",
    "Type de ménage",
    "Situation professionnelle",
    "Situation financière perçue",
]
libelles_axes_socioeconomiques = dict(zip(libelles_synthese, libelles_radar_ages))
palette_socioeconomique = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#333333"]
radars_socioeconomiques = {}

for dimension, categories in dimensions_socioeconomiques.items():
    autres_dimensions = [
        colonne for colonne in dimensions_filtrage if colonne != dimension
    ]
    synthese_dimension = df_synthese_mental.loc[
        df_synthese_mental["Année"].eq(2024)
        & df_synthese_mental[dimension].isin(categories)
        & df_synthese_mental["Sexe"].isin(["Hommes", "Femmes"])
        & df_synthese_mental["Indicateur"].isin(libelles_synthese)
        & df_synthese_mental[autres_dimensions].eq("Tous").all(axis=1)
    ]
    estimations_dimension = (
        synthese_dimension.pivot(
            index=["Sexe", dimension],
            columns="Indicateur",
            values="Estimation",
        )
        .reindex(columns=list(libelles_synthese))
        .dropna(axis=1, how="all")
    )
    libelles_dimension = [
        libelles_axes_socioeconomiques[indicateur]
        for indicateur in estimations_dimension.columns
    ]
    angles_dimension = [
        2 * pi * position / len(libelles_dimension)
        for position in range(len(libelles_dimension))
    ]
    angles_dimension_fermes = angles_dimension + angles_dimension[:1]
    limite_dimension = float(estimations_dimension.max().max()) * 1.15
    fig_dimension, axes_dimension = plt.subplots(
        1,
        2,
        figsize=(18, 9),
        subplot_kw={"projection": "polar"},
        layout="constrained",
    )
    for axe_radar, sexe in zip(axes_dimension, ("Hommes", "Femmes")):
        for (categorie, libelle), couleur in zip(
            categories.items(), palette_socioeconomique
        ):
            valeurs_categorie = estimations_dimension.loc[(sexe, categorie)].tolist()
            axe_radar.plot(
                angles_dimension_fermes,
                valeurs_categorie + valeurs_categorie[:1],
                label=libelle,
                color=couleur,
                marker="o",
                linewidth=2,
                markersize=4,
            )
        axe_radar.set_theta_offset(pi / 2)
        axe_radar.set_theta_direction(-1)
        axe_radar.set_xticks(angles_dimension, libelles_dimension)
        axe_radar.tick_params(axis="x", pad=20, labelsize=10)
        axe_radar.set_ylim(0, limite_dimension)
        axe_radar.yaxis.set_major_formatter(
            FuncFormatter(lambda valeur, position: f"{valeur:g} %"),
        )
        axe_radar.set_title(sexe, pad=45)
        axe_radar.grid(alpha=0.3)
        axe_radar.spines["polar"].set_color("#BBBBBB")
    fig_dimension.suptitle(
        f"Santé mentale en 2024 - Estimations nationales par {dimension.lower()}",
    )
    axes_dimension[0].legend(
        title=dimension,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.18),
        ncol=1,
    )
    radars_socioeconomiques[dimension] = {
        "estimations": estimations_dimension,
        "figure": fig_dimension,
        "axes": axes_dimension,
    }
    plt.show()

# %%
tableaux_radars = {
    "Classe d'âge": estimations_radar_ages,
    "Diplôme": estimations_radar_diplomes,
    **{
        dimension: resultat["estimations"]
        for dimension, resultat in radars_socioeconomiques.items()
    },
}
ordre_categories_tableaux = {
    "Classe d'âge": classes_age_radar,
    "Diplôme": list(couleurs_radar_diplomes),
    **{
        dimension: list(categories)
        for dimension, categories in dimensions_socioeconomiques.items()
    },
}
libelles_colonnes_tableaux = dict(
    zip(
        libelles_synthese,
        [
            "Pensées suicidaires (12 mois)",
            "Tentative de suicide (vie)",
            "Trouble anxieux généralisé",
            "Épisode dépressif caractérisé",
            "A souffert psychologiquement d'un évènement climatique extrême",
        ],
    )
)

for dimension, estimations_tableau in tableaux_radars.items():
    print(f"\nSanté mentale en 2024 - {dimension} - Valeurs en %")
    if dimension == "Type de ménage":
        print("Indicateur climatique non disponible par type de ménage.")
    for sexe in ("Hommes", "Femmes"):
        tableau_sexe = (
            estimations_tableau.loc[sexe]
            .reindex(ordre_categories_tableaux[dimension])
            .rename(columns=libelles_colonnes_tableaux)
        )
        print(f"\n{sexe}")
        print(
            tableau_sexe.to_string(
                float_format=lambda valeur: f"{valeur:.1f}".replace(".", ","),
            )
        )

# %%
