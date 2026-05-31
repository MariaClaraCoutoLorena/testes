import os
import glob
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dados_completos = []

arquivos = glob.glob("resultados_*.txt")

mapa_algoritmos = {
    'minix': 'Minix (Padrão)',
    'fcfs': 'FCFS',
    'round': 'Round Robin',
    'lottery': 'Lottery'
}

for arquivo in arquivos:
    nome_arquivo = os.path.basename(arquivo)
    
   
    match = re.match(r"resultados_([a-zA-Z]+)(\d+)\.txt", nome_arquivo)
    
    if match:
        algoritmo_str = match.group(1).lower()
        num_processos = int(match.group(2))
        
        algoritmo_nome = mapa_algoritmos.get(algoritmo_str, algoritmo_str.capitalize())
        
        df_temp = pd.read_csv(arquivo, sep=r'\s+', header=None, names=['Tipo', 'PID', 'Tempo'])
        
        df_temp['Algoritmo'] = algoritmo_nome
        df_temp['Número de processos'] = num_processos
        
        dados_completos.append(df_temp)

df = pd.concat(dados_completos, ignore_index=True)

df['Tipo'] = df['Tipo'].replace({'CPU': 'CPU-bound', 'IO': 'IO-bound'})

sns.set_theme(style="white")
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

cores = sns.color_palette("tab10")[0:4]

ordem_processos = sorted(df['Número de processos'].unique())
ordem_algoritmos = ['Minix (Padrão)', 'FCFS', 'Round Robin', 'Lottery']

sns.barplot(
    data=df[df['Tipo'] == 'CPU-bound'],
    x='Número de processos',
    y='Tempo', 
    hue='Algoritmo',
    ax=axes[0],
    palette=cores,
    edgecolor='black',
    linewidth=1,
    order=ordem_processos,
    hue_order=ordem_algoritmos,
    errorbar=None 
)

axes[0].set_title('Processos CPU-bound', fontsize=14)
axes[0].set_xlabel('Número de processos', fontsize=12)
axes[0].set_ylabel('Tempo médio (s)', fontsize=12)
axes[0].grid(True, linestyle='--', alpha=0.3)
axes[0].tick_params(labelsize=12)
axes[0].legend(ncol=2, loc='upper center', frameon=True, edgecolor='black')

sns.barplot(
    data=df[df['Tipo'] == 'IO-bound'],
    x='Número de processos',
    y='Tempo',
    hue='Algoritmo',
    ax=axes[1],
    palette=cores,
    edgecolor='black',
    linewidth=1,
    order=ordem_processos,
    hue_order=ordem_algoritmos,
    errorbar=None
)

axes[1].set_title('Processos IO-bound', fontsize=14)
axes[1].set_xlabel('Número de processos', fontsize=12)
axes[1].set_ylabel('Tempo médio (s)', fontsize=12)
axes[1].grid(True, linestyle='--', alpha=0.3)
axes[1].tick_params(labelsize=12)
axes[1].legend(ncol=2, loc='upper center', frameon=True, edgecolor='black')

fig.text(0.28, -0.05, '(a) Resultado para processos CPU-Bound.', ha='center', fontsize=11)
fig.text(0.75, -0.05, '(b) Resultado para processos IO-Bound.', ha='center', fontsize=11)

plt.tight_layout()

plt.savefig('meu_grafico_resultados_longos.png', dpi=300, bbox_inches='tight')

plt.show()
