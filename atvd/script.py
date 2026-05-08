import pandas as pd
import random
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


TOTAL_ALUNOS = 40

alunos = []

for i in range(1, TOTAL_ALUNOS + 1):

    nome = f"Aluno_{i}"

    # Simulação de presença/falta
    presencas = random.randint(40, 100)
    faltas = random.randint(0, 60)

    total = presencas + faltas
    frequencia = (presencas / total) * 100

    alunos.append({
        "Aluno": nome,
        "Presencas": presencas,
        "Faltas": faltas,
        "Frequencia (%)": round(frequencia, 2)
    })

df = pd.DataFrame(alunos)

# Dados usados no agrupamento
X = df[["Presencas", "Faltas"]]

# Criando modelo K-Means
kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

# Criando grupos
df["Grupo"] = kmeans.fit_predict(X)

medias = df.groupby("Grupo")[["Presencas", "Faltas"]].mean()

ordem = medias.sort_values("Faltas").index.tolist()

nomes_grupos = {
    ordem[0]: "Alta Frequência",
    ordem[1]: "Frequência Média",
    ordem[2]: "Risco de Faltas"
}

df["Categoria"] = df["Grupo"].map(nomes_grupos)

def verificar_risco(freq):
    if freq < 60:
        return "ALTO RISCO"
    elif freq < 75:
        return "ATENÇÃO"
    else:
        return "OK"

df["Status"] = df["Frequencia (%)"].apply(verificar_risco)

print("\n=================================================")
print("      RELATÓRIO COMPLETO DA TURMA")
print("=================================================\n")

print(df[
    [
        "Aluno",
        "Presencas",
        "Faltas",
        "Frequencia (%)",
        "Categoria",
        "Status"
    ]
])

print("\n=================================================")
print("      TOP 10 ALUNOS COM MAIS FALTAS")
print("=================================================\n")

top_faltas = df.sort_values(
    by="Faltas",
    ascending=False
).head(10)

print(top_faltas[
    ["Aluno", "Faltas", "Frequencia (%)", "Status"]
])

print("\n=================================================")
print("      TOP 10 MELHORES FREQUÊNCIAS")
print("=================================================\n")

top_presenca = df.sort_values(
    by="Frequencia (%)",
    ascending=False
).head(10)

print(top_presenca[
    ["Aluno", "Presencas", "Frequencia (%)"]
])

print("\n=================================================")
print("      ESTATÍSTICAS DOS GRUPOS")
print("=================================================\n")

estatisticas = df.groupby("Categoria")[
    ["Presencas", "Faltas", "Frequencia (%)"]
].mean().round(2)

print(estatisticas)

arquivo_excel = "relatorio_alunos.xlsx"

df.to_excel(
    arquivo_excel,
    index=False
)

print(f"\nArquivo Excel salvo como: {arquivo_excel}")

cores = {
    "Alta Frequência": "green",
    "Frequência Média": "orange",
    "Risco de Faltas": "red"
}

plt.figure(figsize=(12, 7))

for categoria in df["Categoria"].unique():

    grupo = df[df["Categoria"] == categoria]

    plt.scatter(
        grupo["Presencas"],
        grupo["Faltas"],
        c=cores[categoria],
        label=categoria,
        s=100
    )

for i in range(len(df)):
    plt.text(
        df["Presencas"][i],
        df["Faltas"][i],
        df["Aluno"][i],
        fontsize=8
    )

plt.title("Agrupamento Inteligente de Alunos")
plt.xlabel("Presenças")
plt.ylabel("Faltas")
plt.legend()
plt.grid(True)

plt.show()

print("\n=================================================")
print("      RESUMO FINAL")
print("=================================================\n")

print(
    df["Categoria"]
    .value_counts()
)

print("\nSistema finalizado com sucesso.")