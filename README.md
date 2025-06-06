# GPT

Exemplo simples demonstrando cadastro de colaboradores e usuarios em um banco SQLite.

Dependencias: `bcrypt` para armazenamento seguro de senhas, `fpdf` para gerar PDFs e `ofxparse` para importar extratos bancários.

```bash
pip install bcrypt fpdf ofxparse
```

## Uso

Adicionar colaborador:

```bash
python3 cli.py add "Nome" "Setor"
```

Listar colaboradores:

```bash
python3 cli.py list
```

O comando agora exibe também o login do usuário vinculado e o caminho da foto do colaborador.

Exibir detalhes de um colaborador específico:

```bash
python3 cli.py show ID
```

Atualizar colaborador:

```bash
python3 cli.py update ID --nome "Novo Nome" --setor "Novo Setor"
```

Remover colaborador:

```bash
python3 cli.py delete ID
```

### Gerenciamento de usuarios

Adicionar usuario com perfil (padrao `usuario`):

```bash
python3 cli.py useradd login senha --perfil gestor
```

Listar usuarios cadastrados:

```bash
python3 cli.py userlist
```

Atualizar um usuario existente:

```bash
python3 cli.py userupdate ID --login novo_login --senha nova_senha --perfil admin
```

Remover um usuario:

```bash
python3 cli.py userdel ID
```

Verificar credenciais de um usuario:

```bash
python3 cli.py login usuario senha
```

### Gerenciamento de clientes

Adicionar cliente:

```bash
python3 cli.py clientadd "Nome" --cnpj 123456789
```

Listar clientes:

```bash
python3 cli.py clientlist
```

Atualizar cliente:

```bash
python3 cli.py clientupdate ID --nome "Novo" --cnpj 987654321
```

Remover cliente:

```bash
python3 cli.py clientdel ID
```

Ao criar um colaborador use o parametro `--usuario` com o login para
associa-lo a um usuario existente.

### Controle de estoque

Adicionar quantidade a um item (cria se nao existir):

```bash
python3 cli.py stockadd "Produto" 10
```

Registrar saida do estoque:

```bash
python3 cli.py stockout "Produto" 5
```

Definir exatamente a quantidade de um item (cria se nao existir):

```bash
python3 cli.py stockset "Produto" 20
```

Listar estoque:

```bash
python3 cli.py stocklist
```

Verificar itens com estoque baixo:

```bash
python3 cli.py stockalert 3
```

Registrar discrepancias ou materiais adicionais em uma OP:

```bash
python3 cli.py discadd 1 "Produto" 2 adicional
```

Listar discrepancias registradas (opcional filtrar por OP):

```bash
python3 cli.py disclist --op 1
```

Gerar relatorio resumido de discrepancias por OP:

```bash
python3 cli.py discreport --op 1
```

### Ordens de Producao

Criar uma nova OP (pode informar horas estimadas de montagem):

```bash
python3 cli.py opadd "Montagem Quadro X" --montador 2 --estimativa 5
```

Listar OPs (opcional filtrar por status ou montador):

```bash
python3 cli.py oplist --status "Aguardando Separacao" --montador 2
```
O resultado exibe o montador associado e as horas estimadas/realizadas.

Atualizar dados de uma OP (status, montador ou estimativa):

```bash
python3 cli.py opupdate 1 --status "Em Producao" --montador 3 --estimativa 6
```

Iniciar e finalizar a montagem registrando o tempo real:

```bash
python3 cli.py opstart 1
# ... apos concluir
python3 cli.py opfinish 1
```

Consultar eficiencia de uma OP:

```bash
python3 cli.py opkpi 1
```

Monitorar tempo decorrido de uma OP em andamento:

```bash
python3 cli.py opprogress 1
```

Consultar media de eficiencia de um montador:

```bash
python3 cli.py montkpi 1
```

Verificar OPs aguardando separacao ha muitos dias:

```bash
python3 cli.py opalert 5
```

### Orcamentos e revisoes

Criar um novo orcamento (REV00):

```bash
python3 cli.py budgetadd "Descricao" --cliente "Nome" --motivo "Inicial"
```

Registrar uma revisao:

```bash
python3 cli.py budgetrev 1 "Ajuste de valores"
```

Listar orcamentos (pode filtrar por resultado, aprovacao ou cliente):

```bash
python3 cli.py budgetlist --resultado vendido --aprovado 1 --cliente "ACME"
```

Ver historico de revisoes:

```bash
python3 cli.py budgethist 1
```

Calcular tempos do orcamento:

```bash
python3 cli.py budgettime 1
```

Aprovar um orcamento e criar uma OP automaticamente:

```bash
python3 cli.py budgetapprove 1 --montador 2
```

Definir o resultado final (venda ou perda) e qualificação do cliente:

```bash
python3 cli.py budgetresult 1 vendido --motivo "Fechou negocio" --qualificacao "A"
```

Exportar dados de orcamentos em JSON para dashboards de KPI:

```bash
python3 cli.py kpiexport dados.json
```

Exportar apenas um orcamento especifico:

```bash
python3 cli.py kpiexport dados.json --orcamento 1
```

### Importar Extratos OFX

Para registrar transações financeiras a partir de um arquivo OFX:

```bash
python3 cli.py ofximport extrato.ofx
```

Listar as transações importadas (opcional limitar a N registros):

```bash
python3 cli.py ofxlist --limit 10
```

### Etiquetas de Expedição

Para gerar uma etiqueta simples em PDF para uma OP:

```bash
python3 cli.py label 1
```

O arquivo `etiqueta_OP1.pdf` sera criado no diretorio atual e exibe uma nota de
que o sistema utiliza IA e é exclusivo da ER Elétrica.
