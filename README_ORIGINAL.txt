
Feito em python pela facilidade de escrever, ler e executar.
A única dependência do projeto é o próprio python. Testado na versão 3.11

Dividi em alguns arquivos, o suficiente pra manter
a manipulação de IO separada da lógica do problema.

Sobre a "arquitetura" do programa, não tem segredo.
O código é procedural e eu tentei impor o mínimo de estrutura/abstração
porque não sei que tipo de mudança pode acontecer.

Testes unitários escritos com o pacote unittest
que já vem integrado no python. test_cli.py é um teste um pouco
mais abrangente para simular stdin/stdout.

<raíz>
  |--- capital_gains
  |--- test

Para executar, estando na <raíz> do projeto:
    python -m capital_gains < seu/arquivo.json

Para executar os testes:
    python -m unittest

Atenção ao formato de saída do programa. Se a avaliação do stdout
for feita apenas por comparação de strings pode haver diferenças.
Ver o test_cli.py para entender o formato exato.