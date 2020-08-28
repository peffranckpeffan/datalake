# Desafio Parte 1

A parte do desafio em que mais desprendi tempo (além de ficar horas tentando arrumar o dual boot do meu notebook para conseguir acessar o linux :( ) foi em enteder como poderia construir um cluster local para poder rodar a aplicação. Confesso que toda essa parte foi nova para mim, mas após alguns testes iniciais usando o kubernetes e o minikube, resolvi utilizar o docker-machine e o swarm, pois achei mais faceis de configurar. Quanto a aplicação, desenvolvi utilzando Python e MongoDB. O Python é uma linguagem que ja conheci do periodo em que fazia iniciação cientifica, e que agora estou buscando me aprofundar mais e o MongoDB foi a ferramenta de NoSQL que escolhi para estudar atualmente. Infelizmente não consegui iniciar a parte 2 do desafio, apesar de te-la compreendida e acreditar nao ser complicada de desenvolve-la, foquei mais em compreender o funcionamento do Docker e Docker Swarm. Com certeza fiz algumas coisas que em um ambiente de produção não devem ser feitas, pois tentei manter tudo da maneira mais simples possivel.

Qualquer dúvida fico a disposição e se possivel gostaria de pedir algumas dicas sobre a área de Big Data em questão, eu estou me formando em Física e é um campo no qual me interesso e que pretendo buscar um entendimento melhor.

## Pré-requisitos

- Docker: https://docs.docker.com/engine/install/
- Docker Machine: https://docs.docker.com/machine/install-machine/
- Virtualbox: https://www.virtualbox.org/wiki/Linux_Downloads

## Testes

Primeiramente deve-se criar as maquinas virtuais que rodarão nosso cluster:
```bash
docker-machine create --driver virtualbox manager
docker-machine create --driver virtualbox worker1
docker-machine create --driver virtualbox worker2
```
Esses comandos criarão trẽs maquinas que irão hospedar nosso cluster, a primeira sera o node master onde o Swarm será inicializado e as outras duas serão nodes workers.

Após criadas deve-se acessar a máquina que será nossa master, podemos ver seu ip:
```bash
docker-machine ip manager
docker-machine ssh manager 
```
Depois de acessa-la inicia-se o Swarm, substituindo <MANAGER-IP> pelo ip retornado no primeiro comando acima.
```bash
docker swarm init --advertise-addr <MANAGER-IP>
```
Ainda na maquina manager digita-se o comando:
 ```bash
docker swarm join-token worker
```
Esse comando terá um retorno parecido com esse:
```bash
docker swarm join --token SWMTKN-1-0unpyl3rkly2romb7dd35lsqqpyoyka5162i0tt3um7b4lvjwd-638gmvjgct104hrcp7pvdti5t 192.168.99.100:2377
```
Depois de copiar o retorno do comando anterior basta acessar as outras duas maquinas e digita-lo para que elas juntem-se ao nosso cluster:
 ```bash
docker-machine ssh manager worker1
docker swarm join --token SWMTKN-1-0unpyl3rkly2romb7dd35lsqqpyoyka5162i0tt3um7b4lvjwd-638gmvjgct104hrcp7pvdti5t 192.168.99.100:2377

docker-machine ssh manager worker2
docker swarm join --token SWMTKN-1-0unpyl3rkly2romb7dd35lsqqpyoyka5162i0tt3um7b4lvjwd-638gmvjgct104hrcp7pvdti5t 192.168.99.100:2377
```

Agora nosso cluster está criado e podemos criar nossos serviços. Para faze-lo basta copiar o arquivo docker-compose.yml para nossa maquina manager (a senha é 'tcuser'):
 ```bash
 scp docker-compose.yml docker@$(docker-machine ip manager):/home/docker/
 ```

 Com o arquivo copiado, basta acessar a máquina manager novamente e rodar o comando:
```bash
docker stack deploy --with-registry-auth -c docker-compose.yml app
```

Ainda na maquina manager podemos ver o serviçoes rodando (o mongodb pode demorar alguns minutos para ficar pronto):
```bash
docker service ls
```

As imagens dos serviços já estão criadas e hospedadas em um repositorio publico no Docker Hub.
Assim pode-se fazer requisições para o nosso cluster:
```bash
curl -XPOST http://$(docker-machine ip manager):/v1/products/ -d '[{"id": "123", "name": "mesa"}]'
```