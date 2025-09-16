# Aplicação Web da Tabela Periódica - Backend

Um backend FastAPI para um projeto de aula de TI do ensino médio com uma tabela periódica interativa com cartões flip, informações dos elementos e futura integração de chat/IA.

**Atualização Dia 3.5**: Agora inclui autenticação baseada em JWT com controle de acesso baseado em funções. Usuários administradores podem realizar operações CRUD, enquanto estudantes podem apenas ler dados dos elementos.

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.8 ou superior
- pip (instalador de pacotes Python)

### Instalação e Configuração

1. **Clone o repositório** (se ainda não foi feito):
   ```bash
   git clone https://github.com/EnderPico/TabelaPeriodica.git
   cd TabelaPeriodica
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o servidor de desenvolvimento**:
   ```bash
   uvicorn main:app --reload
   ```

4. **Acesse a API**:
   - URL Base da API: http://localhost:8000
   - Documentação Interativa da API: http://localhost:8000/docs
   - Documentação Alternativa: http://localhost:8000/redoc

### Configuração do Banco de Dados

O banco de dados SQLite é criado e inicializado automaticamente quando você executa o servidor pela primeira vez. Nenhuma configuração adicional necessária!

- **Arquivo do banco**: `periodic_table.db` (criado no diretório do projeto)
- **Dados de exemplo**: Inclui automaticamente Hidrogênio e Hélio
- **Usuário admin**: Criado automaticamente (usuário: `admin`, senha: `admin123`)
- **Gerenciamento**: Use `python manage_db.py` para adicionar mais elementos

### Configuração de Autenticação

O sistema cria automaticamente um usuário administrador na primeira execução:
- **Nome de usuário**: `admin`
- **Senha**: `admin123`
- **Função**: `admin` (pode realizar todas as operações CRUD)

Você pode registrar usuários adicionais através do endpoint `/register`.

## 📚 Endpoints da API

### Dia 3.5 - Autenticação + Operações CRUD

#### Endpoints Públicos (Não Requer Autenticação)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Informações da API e endpoints disponíveis |
| GET | `/elements` | Obter todos os elementos do banco de dados SQLite |
| GET | `/elements/{symbol}` | Obter elemento específico por símbolo (não diferencia maiúsculas/minúsculas) |
| POST | `/register` | Registrar uma nova conta de usuário |
| POST | `/login` | Fazer login e obter token JWT |
| GET | `/health` | Endpoint de verificação de saúde |

#### Endpoints Apenas para Admin (Requer Token JWT + Função Admin)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/elements` | Criar um novo elemento (Apenas Admin) |
| PUT | `/elements/{symbol}` | Atualizar um elemento existente (Apenas Admin) |
| DELETE | `/elements/{symbol}` | Excluir um elemento por símbolo (Apenas Admin) |

### Exemplos de Respostas da API

**Obter todos os elementos** (`GET /elements`):
```json
[
  {
    "id": 1,
    "symbol": "H",
    "name": "Hidrogênio",
    "number": 1,
    "info": "O elemento mais leve e abundante do universo. Essencial para água e compostos orgânicos."
  },
  {
    "id": 2,
    "symbol": "He",
    "name": "Hélio",
    "number": 2,
    "info": "Um gás nobre que é mais leve que o ar. Usado em balões e como refrigerante para ímãs supercondutores."
  }
]
```

**Obter elemento específico** (`GET /elements/H`):
```json
{
  "id": 1,
  "symbol": "H",
  "name": "Hidrogênio",
  "number": 1,
  "info": "O elemento mais leve e abundante do universo. Essencial para água e compostos orgânicos."
}
```

**Criar elemento** (`POST /elements`):
```json
{
  "message": "Elemento 'O' criado com sucesso",
  "element": {
    "id": 3,
    "symbol": "O",
    "name": "Oxigênio",
    "number": 8,
    "info": "Essencial para respiração e combustão. Compõe cerca de 21% da atmosfera terrestre."
  }
}
```

**Atualizar elemento** (`PUT /elements/O`):
```json
{
  "message": "Elemento 'O' atualizado com sucesso",
  "element": {
    "id": 3,
    "symbol": "O",
    "name": "Oxigênio",
    "number": 8,
    "info": "Descrição atualizada: Essencial para vida e processos de combustão."
  }
}
```

**Excluir elemento** (`DELETE /elements/O`):
```json
{
  "message": "Elemento 'O' excluído com sucesso",
  "symbol": "O"
}
```

**Registrar usuário** (`POST /register`):
```json
{
  "message": "Usuário 'estudante1' registrado com sucesso",
  "user": {
    "id": 2,
    "username": "estudante1",
    "role": "student"
  }
}
```

**Login do usuário** (`POST /login`):
```json
{
  "message": "Login realizado com sucesso para o usuário 'admin'",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

## 🧪 Testando Autenticação e Operações CRUD

### Teste de Autenticação

**1. Registrar um novo usuário**:
```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "estudante1",
    "password": "senha123",
    "role": "student"
  }'
```

**2. Fazer login como admin**:
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**3. Salvar o token JWT da resposta de login**:
```bash
# Copie o valor "access_token" da resposta de login
# Exemplo: TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Endpoints Públicos (Sem Autenticação)

**4. Obter todos os elementos**:
```bash
curl -X GET http://localhost:8000/elements
```

**5. Obter elemento específico**:
```bash
curl -X GET http://localhost:8000/elements/H
curl -X GET http://localhost:8000/elements/he  # Não diferencia maiúsculas/minúsculas
```

### Endpoints Apenas para Admin (Requer Token JWT)

**6. Criar novo elemento (Apenas Admin)**:
```bash
curl -X POST http://localhost:8000/elements \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_JWT_AQUI" \
  -d '{
    "symbol": "O",
    "name": "Oxigênio",
    "number": 8,
    "info": "Essencial para respiração e combustão. Compõe cerca de 21% da atmosfera terrestre."
  }'
```

**7. Atualizar elemento existente (Apenas Admin)**:
```bash
curl -X PUT http://localhost:8000/elements/O \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_JWT_AQUI" \
  -d '{
    "info": "Descrição atualizada: Essencial para vida e processos de combustão."
  }'
```

**8. Excluir elemento (Apenas Admin)**:
```bash
curl -X DELETE http://localhost:8000/elements/O \
  -H "Authorization: Bearer SEU_TOKEN_JWT_AQUI"
```

### Teste de Erros

**Tentar criar elemento sem autenticação**:
```bash
curl -X POST http://localhost:8000/elements \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "O",
    "name": "Oxigênio",
    "number": 8,
    "info": "Isso falhará - sem token"
  }'
```

**Tentar criar elemento com token inválido**:
```bash
curl -X POST http://localhost:8000/elements \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer token_invalido" \
  -d '{
    "symbol": "O",
    "name": "Oxigênio",
    "number": 8,
    "info": "Isso falhará - token inválido"
  }'
```

**Tentar fazer login com credenciais erradas**:
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "senhaerrada"
  }'
```

**Tentar registrar nome de usuário duplicado**:
```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "senha123",
    "role": "student"
  }'
```

**Tentar obter elemento inexistente**:
```bash
curl -X GET http://localhost:8000/elements/X
```

## 🔗 Integração com Frontend

### Exemplos de JavaScript Fetch

**Auxiliar de Autenticação**:
```javascript
// Armazenar token JWT no localStorage
function setAuthToken(token) {
    localStorage.setItem('authToken', token);
}

function getAuthToken() {
    return localStorage.getItem('authToken');
}

function clearAuthToken() {
    localStorage.removeItem('authToken');
}

// Função de login
async function login(username, password) {
    try {
        const response = await fetch('http://localhost:8000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            setAuthToken(data.access_token);
            console.log('Login realizado com sucesso:', data);
            return data;
        } else {
            const error = await response.json();
            console.error('Falha no login:', error);
            throw new Error(error.detail);
        }
    } catch (error) {
        console.error('Erro no login:', error);
        throw error;
    }
}

// Função de registro
async function register(username, password, role = 'student') {
    try {
        const response = await fetch('http://localhost:8000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password, role })
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('Registro realizado com sucesso:', data);
            return data;
        } else {
            const error = await response.json();
            console.error('Falha no registro:', error);
            throw new Error(error.detail);
        }
    } catch (error) {
        console.error('Erro no registro:', error);
        throw error;
    }
}
```

**Endpoints Públicos (Não Requer Autenticação)**:

**Obter todos os elementos**:
```javascript
async function fetchAllElements() {
    try {
        const response = await fetch('http://localhost:8000/elements');
        const elements = await response.json();
        console.log('Todos os elementos:', elements);
        return elements;
    } catch (error) {
        console.error('Erro ao buscar elementos:', error);
    }
}
```

**Obter elemento específico**:
```javascript
async function fetchElement(symbol) {
    try {
        const response = await fetch(`http://localhost:8000/elements/${symbol}`);
        if (response.ok) {
            const element = await response.json();
            console.log('Dados do elemento:', element);
            return element;
        } else {
            console.error('Elemento não encontrado');
        }
    } catch (error) {
        console.error('Erro ao buscar elemento:', error);
    }
}
```

**Endpoints Apenas para Admin (Requer Autenticação)**:

**Criar novo elemento (Apenas Admin)**:
```javascript
async function createElement(elementData) {
    const token = getAuthToken();
    if (!token) {
        throw new Error('Nenhum token de autenticação. Por favor, faça login primeiro.');
    }
    
    try {
        const response = await fetch('http://localhost:8000/elements', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(elementData)
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log('Elemento criado:', result);
            return result;
        } else {
            const error = await response.json();
            console.error('Erro ao criar elemento:', error);
            throw new Error(error.detail);
        }
    } catch (error) {
        console.error('Erro ao criar elemento:', error);
        throw error;
    }
}

// Exemplo de uso:
// Primeiro faça login como admin, depois crie elemento
async function exampleCreateElement() {
    try {
        await login('admin', 'admin123');
        await createElement({
            symbol: "N",
            name: "Nitrogênio",
            number: 7,
            info: "Compõe 78% da atmosfera terrestre. Essencial para proteínas e DNA."
        });
    } catch (error) {
        console.error('Falha ao criar elemento:', error);
    }
}
```

**Atualizar elemento (Apenas Admin)**:
```javascript
async function updateElement(symbol, updateData) {
    const token = getAuthToken();
    if (!token) {
        throw new Error('Nenhum token de autenticação. Por favor, faça login primeiro.');
    }
    
    try {
        const response = await fetch(`http://localhost:8000/elements/${symbol}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(updateData)
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log('Elemento atualizado:', result);
            return result;
        } else {
            const error = await response.json();
            console.error('Erro ao atualizar elemento:', error);
            throw new Error(error.detail);
        }
    } catch (error) {
        console.error('Erro ao atualizar elemento:', error);
        throw error;
    }
}

// Exemplo de uso:
// Primeiro faça login como admin, depois atualize elemento
async function exampleUpdateElement() {
    try {
        await login('admin', 'admin123');
        await updateElement("N", { info: "Descrição atualizada para Nitrogênio" });
    } catch (error) {
        console.error('Falha ao atualizar elemento:', error);
    }
}
```

**Excluir elemento (Apenas Admin)**:
```javascript
async function deleteElement(symbol) {
    const token = getAuthToken();
    if (!token) {
        throw new Error('Nenhum token de autenticação. Por favor, faça login primeiro.');
    }
    
    try {
        const response = await fetch(`http://localhost:8000/elements/${symbol}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log('Elemento excluído:', result);
            return result;
        } else {
            const error = await response.json();
            console.error('Erro ao excluir elemento:', error);
            throw new Error(error.detail);
        }
    } catch (error) {
        console.error('Erro ao excluir elemento:', error);
        throw error;
    }
}

// Exemplo de uso:
// Primeiro faça login como admin, depois exclua elemento
async function exampleDeleteElement() {
    try {
        await login('admin', 'admin123');
        await deleteElement("N");
    } catch (error) {
        console.error('Falha ao excluir elemento:', error);
    }
}
```

## 📅 Roadmap de Desenvolvimento

- **Dia 1** ✅: API básica com dados simulados
- **Dia 2** ✅: Integração com banco de dados SQLite com dados reais da tabela periódica
- **Dia 3.0** ✅: Operações CRUD completas para gerenciamento de elementos
- **Dia 3.5** ✅: Autenticação JWT com controle de acesso baseado em funções (ATUAL)
- **Dia 4**: Integração de chat/bot de IA
- **Dia 5**: Testes de integração e polimento
- **Dia 6**: Preparação para apresentação

## 🧪 Testes

### Testes Automatizados com pytest

O projeto inclui testes automatizados abrangentes usando pytest. Todos os testes estão organizados no diretório `tests/`.

#### Executando Testes

**Executar todos os testes**:
```bash
pytest -v
```

**Executar módulos de teste específicos**:
```bash
# Testar operações de banco de dados
pytest tests/test_database.py -v

# Testar endpoints da API
pytest tests/test_elements.py -v

# Testar sistema de autenticação
pytest tests/test_auth.py -v

# Testar funções de usuário e permissões
pytest tests/test_user_roles.py -v

# Testar casos extremos e tratamento de erros
pytest tests/test_edge_cases.py -v
```

**Executar testes com cobertura**:
```bash
# Instalar ferramenta de cobertura
pip install pytest-cov

# Executar testes com relatório de cobertura
pytest --cov=. --cov-report=html

# Visualizar relatório de cobertura
open htmlcov/index.html
```

#### Estrutura dos Testes

A suíte de testes está organizada em módulos focados:

- **`tests/conftest.py`**: Configurações e fixtures compartilhadas dos testes
- **`tests/test_database.py`**: Testes do banco de dados SQLite e modelos SQLAlchemy
- **`tests/test_elements.py`**: Testes dos endpoints da API de elementos (GET, POST, PUT, DELETE)
- **`tests/test_auth.py`**: Testes do sistema de autenticação (registro, login, JWT)
- **`tests/test_user_roles.py`**: Testes de controle de acesso baseado em funções (admin vs estudante)
- **`tests/test_edge_cases.py`**: Casos extremos, condições de limite e tratamento de erros

#### Recursos dos Testes

✅ **Testes de Banco de Dados**:
- Criação e validação de modelos
- Restrições únicas (símbolo, nome de usuário)
- Teste de funções auxiliares
- Operações de consulta

✅ **Testes de API**:
- Todas as operações CRUD
- Requisitos de autenticação
- Tratamento de erros
- Buscas que não diferenciam maiúsculas/minúsculas

✅ **Testes de Autenticação**:
- Hash e verificação de senhas
- Criação e validação de tokens JWT
- Registro e login de usuários
- Controle de acesso baseado em tokens

✅ **Testes de Controle de Acesso Baseado em Funções**:
- Permissões de admin (acesso CRUD completo)
- Permissões de estudante (acesso apenas leitura)
- Restrições de acesso não autenticado

✅ **Testes de Casos Extremos**:
- Teste de valores de limite
- Tratamento de entrada inválida
- Operações concorrentes
- Recuperação de erros

#### Configuração dos Testes

Os testes usam um banco de dados SQLite em memória para isolamento e velocidade. Cada teste executa em um ambiente limpo com:
- Tabelas de banco de dados frescas
- Fixtures de dados de exemplo
- Contas de usuário admin e estudante
- Tokens JWT para teste de autenticação

### Testes Manuais

#### Teste Rápido da API

**Testar funcionalidade básica**:
```bash
# Obter todos os elementos
curl http://localhost:8000/elements

# Obter elemento específico
curl http://localhost:8000/elements/H

# Registrar novo usuário
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "usuarioteste", "password": "senha123", "role": "student"}'

# Fazer login como admin
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

#### Teste Interativo

**Usar a documentação interativa da API**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🛠️ Comandos de Desenvolvimento

```bash
# Executar servidor de desenvolvimento com recarregamento automático
uvicorn main:app --reload

# Executar em host e porta específicos
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Executar todos os testes
pytest -v

# Executar testes com cobertura
pytest --cov=. --cov-report=html

# Executar arquivo de teste específico
pytest tests/test_elements.py -v

# Testar funcionalidade básica da API (legado)
python tests/test_api.py

# Testar operações CRUD abrangentes (legado)
python tests/test_crud.py

# Instalar novas dependências
pip install nome-do-pacote
pip freeze > requirements.txt
```

## 📁 Estrutura do Projeto

```
TabelaPeriodica/
├── main.py              # Aplicação FastAPI com autenticação e CRUD
├── models.py            # Modelos de banco de dados SQLAlchemy (Element, User)
├── schemas.py           # Schemas Pydantic para validação
├── auth.py              # Funções de autenticação e JWT
├── manage_db.py         # Script de gerenciamento do banco de dados
├── requirements.txt     # Dependências Python
├── periodic_table.db    # Banco de dados SQLite (criado automaticamente)
├── tests/               # Suíte de testes abrangente
│   ├── conftest.py      # Configurações e fixtures compartilhadas dos testes
│   ├── test_database.py # Testes do banco de dados e modelos SQLAlchemy
│   ├── test_elements.py # Testes dos endpoints da API de elementos
│   ├── test_auth.py     # Testes do sistema de autenticação
│   ├── test_user_roles.py # Testes de controle de acesso baseado em funções
│   ├── test_edge_cases.py # Testes de casos extremos e tratamento de erros
│   ├── test_api.py      # Script de teste básico da API (legado)
│   └── test_crud.py     # Script de teste CRUD (legado)
└── README.md           # Este arquivo
```

## 🗄️ Gerenciamento do Banco de Dados

### Adicionando Elementos

Use o script de gerenciamento do banco de dados para adicionar mais elementos:

```bash
python manage_db.py
```

Este script interativo permite:
- Adicionar elementos de exemplo (Lítio, Carbono, Nitrogênio, Oxigênio, Flúor)
- Adicionar elementos personalizados com seus próprios dados
- Listar todos os elementos no banco de dados
- Redefinir o banco de dados se necessário

### Adicionando Elementos Programaticamente

Você também pode adicionar elementos diretamente em Python:

```python
from models import add_element

# Adicionar um novo elemento
add_element(
    symbol="Na",
    name="Sódio", 
    number=11,
    info="Essencial para função nervosa e contração muscular."
)
```

### Esquema do Banco de Dados

A tabela `Element` tem a seguinte estrutura:
- `id`: Chave primária (auto-incremento)
- `symbol`: Símbolo químico (único, ex: "H", "He")
- `name`: Nome completo do elemento (ex: "Hidrogênio", "Hélio")
- `number`: Número atômico (ex: 1, 2)
- `info`: Descrição/informações sobre o elemento

## 🤝 Colaboração em Equipe

Este backend foi projetado para funcionar com a implementação HTML/CSS/JS da equipe de frontend. A API fornece respostas JSON limpas que podem ser facilmente consumidas por chamadas JavaScript fetch.

**Para Desenvolvedores de Frontend**: Use os exemplos JavaScript acima para integrar com esta API. O middleware CORS está configurado para permitir solicitações de qualquer origem durante o desenvolvimento.

## 🐛 Solução de Problemas

**Porta já em uso**:
```bash
# Matar processo usando porta 8000
lsof -ti:8000 | xargs kill -9

# Ou usar uma porta diferente
uvicorn main:app --port 8001 --reload
```

**Erros de módulo não encontrado**:
```bash
# Certifique-se de estar no diretório do projeto
cd TabelaPeriodica

# Reinstalar dependências
pip install -r requirements.txt
```

## 📝 Notas

- Esta é a implementação do Dia 3.5 com autenticação JWT e controle de acesso baseado em funções
- CORS está configurado para desenvolvimento (permite todas as origens)
- O banco de dados é criado e inicializado automaticamente na primeira execução
- Busca de símbolo de elemento que não diferencia maiúsculas/minúsculas (ex: "h", "H", "he", "He" funcionam)
- Validação Pydantic garante integridade dos dados
- Prevenção de símbolo/número atômico duplicado
- Tokens JWT expiram após 30 minutos
- Usuários admin podem realizar operações CRUD, estudantes podem apenas ler
- Conta admin padrão: usuário="admin", senha="admin123"
- Use `python manage_db.py` para facilmente adicionar mais elementos
- SQLAlchemy 2.0.43 para compatibilidade com Python 3.13
