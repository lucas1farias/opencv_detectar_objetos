

# opencv_detectar_objetos
Atividade avaliativa da disciplina de Engenharia de Software

### Vídeo de referência e referências
```
https://www.youtube.com/watch?v=hg4oVgNq7Do
https://github.com/ultralytics/ultralytics
https://github.com/DAVIDNYARKO123/yolov8-silva/tree/main
```

# --o Baixar o repositório
#### . Usar git clone ou download zip do link
`OBS: por padrão, ao baixar um repositório no github, o nome dado ao repositório virtual vira uma pasta que guarda a pasta do projeto em si. Isso deve ser corrigido.
`
# --o Maneiras que eu conheço
`(1) ao baixar o repositório, entre na pasta aninhada (que é a do projeto, de fato) e recorte o conteúdo inteiro para o local da pasta principal (a pasta anterior). Em seguida, delete a pasta que ficou vazia.
`
<br><br>
`(2) recorte o conteúdo inteiro da pasta do projeto (que é a pasta aninhada) e cole em uma outra pasta fora da pasta principal, no local que você planeja que ela vá ficar. Em seguida, pode deletar a pasta que ficou vazia.
`

# --o Instalar um ambiente virtual 
#### . Abra a pasta do projeto numa IDE, e nela abra o terminal integrado 
#### . O terminal deve estar aberto na raiz do projeto
#### . Executar o comando abaixo p/ iniciar as instalações das dependências
`. OBS: O comando abaixo pode funcionar ou não dependendo das configurações do seu interpretador python. Se não funcionar, tente "python3 -m venv venv", e se persistir, procure um tutorial de como instalar ambiente virtual no python
`

```
python -m venv venv
```

# --o Logar no ambiente virtual
#### . Com o terminal aberto na raiz do projeto, fazer:

```
venv\scripts\activate
```

# --o Instalação de dependências
#### . O ambiente virtual deve estar ativado
#### . As bibliotecas instaladas são muito grandes, então a instalação levará algum tempo
#### . Usa o primeiro comando abaixo (caso não funcione, tentar o segundo)

```
pip install -r libs.txt
pip install ultralytics
```

# --o Habilitar conexão com a câmera
#### . Baixar e instalar o aplicativo "DroidCam" no seu celular
#### . Baixar e instalar o aplicativo desktop "DroidCam Client" no seu computador 
`pesquisa: droidcam client (site dev47Apps)`
 #### . Abrir o aplicativo desktop, e iniciar o servidor wifi (opção 3 na tela)
#### . Iniciar o aplicativo do celular, que lhe fornecerá:
`Wifi IP ou IP Cam Access (escolher IP Cam Access)`
#### . Copiar o endereço de IP que têm "/video" no final
`OBS: copiar somente o endereço de IP (pois o algoritmo já trata do resto)`

# --o Arquivo: object_detection.py
#### . Vá ao final do documento (CTRL + End ou use o CTRL + F na IDE), onde encontrará a variável: `ip_address`
#### . Cole o endereço de IP gerado pelo seu celular no valor de "ip_address" 
#### . OPCIONAL
`OBS: a variável "monitor" contêm as dimensões da tela que o "opencv" abrirá a câmera. Caso queira mudar o tamanho da sua tela, modifique estes valores.
`

# --o Pasta: weights
#### . Pasta programada no algoritmo p/ receber o arquivo de "weights" do YOLOv8
#### . Ao executar o algoritmo "object_detection.py", o arquivo pertinente será baixado

# --o Arquivo: yolov8n.pt (dentro da pasta weights)
#### . Baixado automaticamente quando o algoritmo "object_detection.py" é executado

# --o Arquivo: cls.txt
#### . Arquivo que contêm as classes treinadas pelo YOLOV8
`OBS: o nome das classes podem ser alvos usados no algoritmo`
