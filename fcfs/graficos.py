import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dados_completos = []

# Mapeamento exato dos dois arquivos que estão na sua pasta
arquivos_alvo = {
    'resultados_minixlongo100.txt': 'Minix (Padrão)',
    'resultados_fcfslongo100.txt': 'FCFS'
}

# Lendo apenas os arquivos especificados
for arquivo, algoritmo_nome in arquivos_alvo.items():
    if os.path.exists(arquivo):
        # Lê o TXT
        df_temp = pd.read_csv(arquivo, sep=r'\s+', header=None, names=['Tipo', 'PID', 'Tempo'])
        
        # Adiciona colunas identificadoras
        df_temp['Algoritmo'] = algoritmo_nome
        # Como o minix não tem número no nome, padronizamos como 100 para ambos
        # aparecerem juntos na mesma coluna do gráfico
        df_temp['Número de processos'] = 100 
        
        dados_completos.append(df_temp)
    else:
        print(f"Aviso: O arquivo {arquivo} não foi encontrado no diretório.")

# Verifica se os dados foram carregados antes de plotar
if dados_completos:
    df = pd.concat(dados_completos, ignore_index=True)

    df['Tipo'] = df['Tipo'].replace({'CPU': 'CPU-bound', 'IO': 'IO-bound'})

    sns.set_theme(style="white")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    cores = sns.color_palette("tab10")[0:4]

    ordem_processos = sorted(df['Número de processos'].unique())
    ordem_algoritmos = ['Minix (Padrão)', 'FCFS']

    # --- Gráfico 1: CPU-bound ---
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

    # --- Gráfico 2: IO-bound ---
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

    # Legendas inferiores
    fig.text(0.28, -0.05, '(a) Resultado para processos CPU-Bound.', ha='center', fontsize=11)
    fig.text(0.75, -0.05, '(b) Resultado para processos IO-Bound.', ha='center', fontsize=11)

    plt.tight_layout()

    # Salva e exibe
    plt.savefig('meu_grafico_resultados_longos.png', dpi=300, bbox_inches='tight')
    plt.show()
else:
    print("Nenhum dado foi carregado. Verifique os nomes dos arquivos.")