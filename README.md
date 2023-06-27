# Twitch_Categorie_Query
Projeto de automação, utilizando ChromeDriver, Python, Airflow e Selenium e Docker com o intuito de, a cada 2 horas, dados das Categorias mais assistidas da Twitch.

Para instalação do Projeto é preciso além da instalação de webdriver_manager, selenium, pandas, openpyxl, dash. é preciso intalar as imagens:
https://drive.google.com/drive/folders/1UHqU79LrJWqMI3FJx-9xqgX2mq_ZMfEg

utilizando:
docker build . -f Dockerfile --pull --tag 'caminho/da/imagem'
