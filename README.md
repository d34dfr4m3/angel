# Angel
A ideia é ter um Bot para interação em channeis IRC, por hora, apenas algumas funcionalidades básicas como identificar URLS estão implementadas. 
O nome Angel é referente à uma hacker em BorderLands-2 cujo nickname é Angel, ela se sacrifica para salvar o mundo, achei do caralho e quis dar o nome em homenagem.

#### Dependencias:
Algumas que eu ainda não mapiei, mas tem uma porrada de coisa no código, como ainda é um esboço, não vou citar todos pois vou remover muita coisa pra enxutar o código.
 - tor ( localhost:9050 )
 - python3.5

#### Utilização:
Bom, o script não está pronto. Mas para a utilização básica, ele conecta no servidor irc através da onion. Todas as opções necessárias são passadas via argumentos, todas são necessárias para que a angel funcione. 
Ela acessa o irc atráves da onion, as requisições para identificar um site também são feitas pela onion para preservar a localização do bot.
  
#### To Do
  - Problemas de desempenho precisam ser corrigidos.
  - Melhorar o tratamento do regex, se possvel utilizar outra forma de reconhecer os links.
  
###### yes, i know, the source are a shit
###### Paper
 - https://linuxacademy.com/blog/geek/creating-an-irc-bot-with-python3/
