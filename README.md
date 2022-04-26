# K-means Navigation
Navegação robótica por identificação de estados a partir de clusterização de dados pelo algoritmo de K-means na plataforma Webots

1 - Instale a versão R2021a ou superior do Webots em https://cyberbotics.com/

2 - Inserir os controllers e os mapas deste repositório à plataforma;  
    Exemplo deste passo pode ser visualizado neste link: https://drive.google.com/file/d/1S0gy94EsnUAwoRAFdREzEXakfea2U5Px/view?usp=sharing
    
    
# Cluster Validation by K-means

Para validar a qualidade do agrupamento de dados pelo ARI de um determinado dataset, juntamente com sua representação gráfica do seu GroudTruth com PCA, basta executar o arquivo clusterValidationKmeans.py na pasta clustering_Validation_Kmeans  

Procedimentos a serem feitos manualmente:  
1 - Determinar o número de grupos a serem criados;  
2 - Selecionar o dataset a ser validado (caso for utilizado algum dataset deste projeto, selecionar um dos dataset contidos nas pastas csvCombined).

# datasetCollector controller

Este controlador permite coletar informações do ambiente. Para fazer os devidos ajustes de acordo com sua preferência, altere as variáveis de velocidade, quantidade de dados a serem coletados, o nome do estado a ser identificado, e o nome dos arquivos gerados com label e sem label.
