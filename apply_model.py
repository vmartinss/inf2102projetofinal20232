import pandas as pd
from joblib import load

# Carregar os dados
data = pd.read_csv('result.csv')

# Nome do modelo
model_name = 'model_featureenvy3_f9.pkl'  # Substitua pelo nome do modelo desejado

# Selecionar as características com base no modelo
if model_name == 'model_longmethod3_f9.pkl':
    features = data[['smell_Designite_num_aglomeration', 'smell_PMD_num_aglomeration',
                     'LOC', 'Stars', 'Number_of_Contributors', 'Commits', 'smell_Organic_longmethod',
                     'smell_Designite_longmethod', 'smell_PMD_longmethod']]
elif model_name == 'model_featureenvy3_f9.pkl':
    features = data[['smell_Designite_num_aglomeration', 'smell_PMD_num_aglomeration',
                     'LOC', 'Stars', 'Number_of_Contributors', 'Commits', 'smell_Organic_featureenvy',
                     'smell_Designite_aglomeration', 'smell_Designite_longmethod']]

# Carregar o modelo
model = load(model_name)

# Fazer previsões
predictions = model.predict(features)

# Salvar os resultados
output = pd.DataFrame({'Type Name': data['Type Name'], 'Prediction': predictions})
output.to_csv('prediction_results.csv', index=False)