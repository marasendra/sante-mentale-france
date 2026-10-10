# %%
from pathlib import Path
from textwrap import wrap

import matplotlib.pyplot as plt
import pandas as pd
import squarify
from matplotlib.colors import to_rgb
from matplotlib.patches import Rectangle

df_suicides_moyens = pd.read_csv(
    Path(__file__).parent / "data" / "suicides-moyens-utilises-france.csv"
)

df_national = df_suicides_moyens.loc[
    (df_suicides_moyens["Sexe"] == "Hommes et Femmes")
    & (df_suicides_moyens["Moyen utilisé"] != "Total")
]
deces_par_moyen = df_national.pivot(
    index="Année", columns="Moyen utilisé", values="Nombre de décès"
).sort_index()


deces_2023 = deces_par_moyen.loc[2023].sort_values(ascending=False)
deces_2023 = deces_2023.loc[deces_2023 > 0]
palette_treemap = (
    "#332288",
    "#88CCEE",
    "#44AA99",
    "#117733",
    "#999933",
    "#DDCC77",
    "#CC6677",
    "#882255",
    "#AA4499",
    "#DDDDDD",
    "#EE7733",
    "#EE3377",
)
couleurs_par_moyen = {
    moyen: palette_treemap[index] for index, moyen in enumerate(deces_par_moyen.columns)
}
couleurs_2023 = [couleurs_par_moyen[moyen] for moyen in deces_2023.index]


def ajouter_libelles_rectangles(ax, rectangles_par_moyen):
    fig = ax.figure
    font_size = 14
    textes = []
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    for moyen, rectangle in rectangles_par_moyen:
        coin_bas_gauche = ax.transData.transform((rectangle["x"], rectangle["y"]))
        coin_haut_droit = ax.transData.transform(
            (
                rectangle["x"] + rectangle["dx"],
                rectangle["y"] + rectangle["dy"],
            )
        )
        largeur_px = coin_haut_droit[0] - coin_bas_gauche[0] - 10
        hauteur_px = coin_haut_droit[1] - coin_bas_gauche[1] - 8
        largeur_caracteres = max(
            1,
            int(largeur_px / (font_size * fig.dpi / 72 * 0.55)),
        )
        lignes = wrap(
            moyen,
            width=largeur_caracteres,
            break_long_words=True,
            break_on_hyphens=True,
        )
        if hauteur_px < len(lignes) * font_size * fig.dpi / 72 * 1.25:
            continue

        couleur = to_rgb(couleurs_par_moyen[moyen])
        luminance = sum(
            poids * composante
            for poids, composante in zip((0.2126, 0.7152, 0.0722), couleur)
        )
        texte = ax.text(
            rectangle["x"] + rectangle["dx"] / 2,
            rectangle["y"] + rectangle["dy"] / 2,
            "\n".join(lignes),
            ha="center",
            va="center",
            fontsize=font_size,
            fontweight="bold",
            color="#222222" if luminance > 0.55 else "white",
        )
        textes.append((texte, coin_bas_gauche, coin_haut_droit))

    fig.canvas.draw()
    for texte, coin_bas_gauche, coin_haut_droit in textes:
        limites_texte = texte.get_window_extent(fig.canvas.get_renderer())
        if (
            limites_texte.x0 < coin_bas_gauche[0] + 4
            or limites_texte.x1 > coin_haut_droit[0] - 4
            or limites_texte.y0 < coin_bas_gauche[1] + 4
            or limites_texte.y1 > coin_haut_droit[1] - 4
        ):
            texte.remove()


# %%
deces_sexes_2023 = df_suicides_moyens.loc[
    (df_suicides_moyens["Année"] == 2023)
    & df_suicides_moyens["Sexe"].isin(["Hommes", "Femmes"])
    & (df_suicides_moyens["Moyen utilisé"] != "Total")
    & (df_suicides_moyens["Nombre de décès"] > 0)
]
totaux_par_sexe = deces_sexes_2023.groupby("Sexe")["Nombre de décès"].sum()
tableau_suicides_par_moyen_2023 = (
    deces_sexes_2023.pivot(
        index="Moyen utilisé",
        columns="Sexe",
        values="Nombre de décès",
    )
    .reindex(columns=["Hommes", "Femmes"])
    .fillna(0)
)
tableau_suicides_par_moyen_2023["Total"] = tableau_suicides_par_moyen_2023.sum(axis=1)
tableau_suicides_par_moyen_2023 = tableau_suicides_par_moyen_2023.sort_values(
    "Total",
    ascending=False,
)
tableau_suicides_par_moyen_2023.loc["Total"] = [
    totaux_par_sexe["Hommes"],
    totaux_par_sexe["Femmes"],
    totaux_par_sexe.sum(),
]
print("Décès par suicide en France en 2023 selon le moyen et le sexe :")
print(
    tableau_suicides_par_moyen_2023.to_string(
        float_format=lambda valeur: f"{valeur:,.1f}".replace(",", " ").replace(
            ".", ","
        ),
    )
)
fig_sexes, ax_sexes = plt.subplots(figsize=(14, 7), layout="constrained")
fig_sexes.set_facecolor("#F5F6F3")
ax_sexes.set_facecolor("#F5F6F3")
position_x = 0.0
rectangles_suicides = []

for sexe in ("Hommes", "Femmes"):
    deces_par_sexe_2023 = (
        deces_sexes_2023.loc[deces_sexes_2023["Sexe"] == sexe]
        .set_index("Moyen utilisé")["Nombre de décès"]
        .sort_values(ascending=False)
    )
    largeur = 100 * totaux_par_sexe[sexe] / totaux_par_sexe.sum()
    rectangles = squarify.squarify(
        squarify.normalize_sizes(deces_par_sexe_2023.to_numpy(), largeur, 92),
        position_x,
        0,
        largeur,
        92,
    )
    for moyen, rectangle in zip(deces_par_sexe_2023.index, rectangles):
        rectangles_suicides.append((moyen, rectangle))
        ax_sexes.add_patch(
            Rectangle(
                (rectangle["x"], rectangle["y"]),
                rectangle["dx"],
                rectangle["dy"],
                facecolor=couleurs_par_moyen[moyen],
                edgecolor="white",
                linewidth=1.5,
            )
        )
    ax_sexes.add_patch(
        Rectangle(
            (position_x, 92),
            largeur,
            8,
            facecolor="#eeeeee",
            edgecolor="white",
        )
    )
    ax_sexes.text(
        position_x + largeur / 2,
        96,
        f"{sexe}\n{totaux_par_sexe[sexe]:.0f} suicides",
        ha="center",
        va="center",
        fontsize=18,
    )
    ax_sexes.add_patch(
        Rectangle(
            (position_x, 0),
            largeur,
            100,
            fill=False,
            edgecolor="#333333",
            linewidth=2,
        )
    )
    position_x += largeur

ax_sexes.set_xlim(0, 100)
ax_sexes.set_ylim(0, 100)
ajouter_libelles_rectangles(ax_sexes, rectangles_suicides)
ax_sexes.set_axis_off()
plt.savefig("treemap_suicides_2023.svg")

# %%
df_hospit = pd.read_csv(
    Path(__file__).parent
    / "data"
    / "gestes-auto-infliges-moyens-utilises-ayant-mene-a-une-hospitalisation-france.csv"
)
df_hospit.columns = df_hospit.columns.str.lstrip("\ufeff")
hospit_2023 = df_hospit.loc[
    (df_hospit["Année"] == 2023) & df_hospit["Sexe"].isin(["Hommes", "Femmes"])
]
sejours_sexes_2023 = hospit_2023.loc[
    (hospit_2023["Moyen utilisé"] != "Total") & (hospit_2023["Nombre de séjours"] > 0)
]
totaux_hospit_par_sexe = hospit_2023.loc[
    hospit_2023["Moyen utilisé"] == "Total"
].set_index("Sexe")["Nombre de séjours"]
tableau_hospitalisations_par_moyen_2023 = (
    sejours_sexes_2023.pivot(
        index="Moyen utilisé",
        columns="Sexe",
        values="Nombre de séjours",
    )
    .reindex(columns=["Hommes", "Femmes"])
    .fillna(0)
)
tableau_hospitalisations_par_moyen_2023["Total"] = (
    tableau_hospitalisations_par_moyen_2023.sum(axis=1)
)
tableau_hospitalisations_par_moyen_2023 = (
    tableau_hospitalisations_par_moyen_2023.sort_values("Total", ascending=False)
)
tableau_hospitalisations_par_moyen_2023.loc["Total"] = [
    totaux_hospit_par_sexe["Hommes"],
    totaux_hospit_par_sexe["Femmes"],
    totaux_hospit_par_sexe.sum(),
]
print("Hospitalisations en France en 2023 selon le moyen utilisé et le sexe :")
print(
    tableau_hospitalisations_par_moyen_2023.to_string(
        float_format=lambda valeur: f"{valeur:,.1f}".replace(",", " ").replace(
            ".", ","
        ),
    )
)
fig_hospit, ax_hospit = plt.subplots(figsize=(14, 7), layout="constrained")
fig_hospit.set_facecolor("#F5F6F3")
ax_hospit.set_facecolor("#F5F6F3")
position_x_hospit = 0.0
rectangles_hospitalisations = []

for sexe in ("Hommes", "Femmes"):
    sejours_par_sexe_2023 = (
        sejours_sexes_2023.loc[sejours_sexes_2023["Sexe"] == sexe]
        .set_index("Moyen utilisé")["Nombre de séjours"]
        .sort_values(ascending=False)
    )
    largeur_hospit = 100 * totaux_hospit_par_sexe[sexe] / totaux_hospit_par_sexe.sum()
    rectangles_hospit = squarify.squarify(
        squarify.normalize_sizes(sejours_par_sexe_2023.to_numpy(), largeur_hospit, 92),
        position_x_hospit,
        0,
        largeur_hospit,
        92,
    )
    for moyen, rectangle in zip(sejours_par_sexe_2023.index, rectangles_hospit):
        rectangles_hospitalisations.append((moyen, rectangle))
        ax_hospit.add_patch(
            Rectangle(
                (rectangle["x"], rectangle["y"]),
                rectangle["dx"],
                rectangle["dy"],
                facecolor=couleurs_par_moyen[moyen],
                edgecolor="white",
                linewidth=1.5,
            )
        )
    ax_hospit.add_patch(
        Rectangle(
            (position_x_hospit, 92),
            largeur_hospit,
            8,
            facecolor="#eeeeee",
            edgecolor="white",
        )
    )
    ax_hospit.text(
        position_x_hospit + largeur_hospit / 2,
        96,
        f"{sexe}\n{totaux_hospit_par_sexe[sexe]:.0f} hospitalisations",
        ha="center",
        va="center",
        fontsize=15,
    )
    ax_hospit.add_patch(
        Rectangle(
            (position_x_hospit, 0),
            largeur_hospit,
            100,
            fill=False,
            edgecolor="#333333",
            linewidth=2,
        )
    )
    position_x_hospit += largeur_hospit


ax_hospit.set_xlim(0, 100)
ax_hospit.set_ylim(0, 100)
ajouter_libelles_rectangles(ax_hospit, rectangles_hospitalisations)

ax_hospit.set_axis_off()
plt.savefig("treemap_hospitalisations_2023.svg")
