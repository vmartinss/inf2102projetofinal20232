# Modelo ML para Detecção de Code Smell Long Method e Feature Envy em projetos Open-Source no GitHub

## Preparação do Ambiente para rodar o modelo

### Seleção do repositório do projeto no GitHub

Para utilizar o modelo é necessário que o usuário selecione um projeto desenvolvido em java no GitHub e faça o download do repositório.

Abra o código "get_repository_info.py" e insira o endereço do repositório e o token da sua conta no GitHub.

```python
token = "insira_seu_token_aqui" #Insira seu token do GitHub aqui
repository_urls = ["https://github.com/weblegacy/struts1", "https://github.com/r5v9/persist"]  # Adicione as URLs dos repositórios aqui
```

Execute o código e o arquivo "repository\_info.csv" será criado. Ele contém os dados para a extração das seguintes features: commits, stars, LOC e number\_of\_contributors.

### Ferramentas

Antes da utilização das ferramentas, o usuário deve copiar todos os arquivos .java para uma pasta única.

#### PMD

Para utilizar a ferramenta PMD e obter os dados, o usuário deve fazer o download através do site https://pmd.github.io/ e, em seguida, realizar as seguintes etapas:

1. Extair o arquivo para, por exemplo, C:\pmd-bin-7.0.0-rc4
2. Executar a linha de comando:
3. "<caminho_para_pmd.bat_pasta_bin_na_pasta_raiz_pmd> check -d <caminho_para_a_pasta_com_os_códigos> -R rulesets/java/design.xml -f csv -r <caminho_do_arquivo_csv/report.csv>"

Após executar a linha de comando, o arquivo "report.csv" é criado. Ele contém os dados para a extração das seguinte features: smell_PMD_num_agglomeration e smell_PMD_longmethod.

### Organic

Para utilizar a ferramenta Organic e obter os dados, o usuário deve acessar o repositório do OPUS através do link https://github.com/opus-research/organic e baixar o arquivo .jar.

Para executar a ferramenta, deve executar o seguinte comando:

– "java -jar <caminho_para_o_organic-v0.1.2.jar> -src <CAMINHO_PROS_ARQUIVOS_DE_CODIGO> -sf output.json"

O arquivo "output.json" é criado. Ele contém os dados para a extração das seguintes features: smell_Organic_featureenvy e smell_Organic_longmethod.

#### Designate

A ferramenta Designate apresenta diversas versões, a necessária para obter os dados é a DesignateJava e pode ser obtida através do endereço https://www.designite-tools.com/.

Com o DesignateJava.jar, execute o seguinte comando:

– "java -jar <caminho_para_o_DesigniteJava.jar> -i <caminho_com_os_arquivos> -o <caminho_saida_com_os_smells>"

O Designate gera diversas saídas, mas, para o treinamento do modelo, somente foi utilizado as seguintes: ImplementationSmells.csv e DesignSmells.csv.

Através desses dois csvs, iremos obter os dados para a extração das seguintes features: smell_Designite_longmethod, smell_Designite_num_aglomeration e smell_Designite_agglomeration.

### Preparação e unificação dos dados

Para preparar e unificar os dados que vão ser utilizados no modelo, crie uma pasta com todas as saídas e execute o código "merge.py".

O arquivo "result.csv" é criado com o merge dos dados e pronto para execução do modelo.

Caso o usuário tenha alterado algum nome das saídas geradas anteriormente, será necessário alterar o caminho no código.

### Utilização do modelo

Para utilizar o modelo, abra o código "apply_model.py" e edite o nome do modelo para qual modelo vai utilizar (model_featureenvy3_f9.pkl ou model_longmethod3_f9.pkl). Execute o código.

```Python
model_name = 'model_featureenvy3_f9.pkl'  # Substitua pelo nome do modelo desejado
```

O modelo é carregado e faz as previsões, gerando uma arquivo "prediction_results.csv" com a previsão se possui ou não o code smell do modelo para cada arquivo java.

## Observações

Caso apresente dificuldade para rodar algum dos códigos, utlize o Google Colab.
