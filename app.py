import streamlit as st
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import pandas as pd
import numpy as np
from matplotlib.lines import Line2D

# Configuração da página do Streamlit
st.set_page_config(page_title="Pass Map", layout="wide")

# --- Exemplo de DataFrame (Remova isso e use o seu df original) ---
data = {
    'x_start': [20, 40, 60, 30],
    'y_start': [30, 50, 20, 70],
    'x_end': [45, 85, 90, 35],
    'y_end': [35, 60, 10, 65],
    'errado': [False, False, False, True],
    'progressivo': [False, True, True, False]
}
df = pd.DataFrame(data)
# -----------------------------------------------------------------

st.title("Visualização de Passes")

# Encapsulando o plot em uma função para manter o cache/organização
def draw_pass_map(df):
    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color='#f5f5f5',
        line_color='#4a4a4a'
    )

    # Definimos explicitamente o facecolor da figura para bater com o do pitch
    fig, ax = pitch.draw(figsize=(12, 8))
    fig.set_facecolor('#f5f5f5')

    # Linha de referência Final Third (x=80)
    ax.axvline(x=80, color='#4a4a4a', linestyle='--', linewidth=1, alpha=0.3)

    for _, row in df.iterrows():
        if row["errado"]:
            color = (0.9, 0.1, 0.1, 0.6)  # Vermelho
            width = 1.8
        elif row["progressivo"]:
            color = (0.1, 0.4, 0.9, 0.9)  # Azul
            width = 2.4
        else:
            color = (0.6, 0.6, 0.6, 0.4)  # Cinza
            width = 1.4

        pitch.arrows(
            row.x_start, row.y_start,
            row.x_end, row.y_end,
            color=color, width=width,
            headwidth=3.5, headlength=3.5,
            ax=ax
        )

    # Legenda Elegante
    legend_elements = [
        Line2D([0], [0], color=(0.1, 0.4, 0.9, 0.9), lw=2.5, label='Progressive Passes'),
        Line2D([0], [0], color=(0.6, 0.6, 0.6, 0.5), lw=2, label='Successful Passes'),
        Line2D([0], [0], color=(0.9, 0.1, 0.1, 0.7), lw=2, label='Unsuccessful Passes')
    ]

    ax.legend(
        handles=legend_elements, 
        loc='upper left', 
        fontsize=10, 
        frameon=True, 
        facecolor='#ffffff', 
        edgecolor='#cccccc', 
        shadow=True,
        bbox_to_anchor=(0.01, 0.99)
    )

    # Direção de Ataque
    pitch.arrows(50, 85, 70, 85, color='#4a4a4a', width=1.5, 
                 headwidth=4, headlength=5, ax=ax, clip_on=False)

    ax.text(60, 88, 'ATTACK DIRECTION', color='#4a4a4a', 
            va='center', ha='center', fontsize=9, fontweight='bold', alpha=0.8)

    plt.title("Pass Map | Opta Progressive Passes Definition", 
              fontsize=16, pad=20, fontweight='bold', color='#333333')
    
    return fig

# Exibindo no Streamlit
mapa_passes = draw_pass_map(df)
st.pyplot(mapa_passes, use_container_width=True)
