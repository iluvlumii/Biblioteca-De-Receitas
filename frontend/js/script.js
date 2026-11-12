// O navegador conversa somente com a API. Não armazene a senha no navegador.
const API_URL = 'http://127.0.0.1:8000/clientes';
const LOGIN_API_URL = 'http://127.0.0.1:8000/login';

const formularioLogin = document.querySelector('#form-login');
const campoEmailLogin = document.querySelector('#email');
const campoSenhaLogin = document.querySelector('#senha');
const botaoEntrar = document.querySelector('#botao-Entrar');
const mensagemLogin = document.querySelector('#mensagem');
const formulario = document.querySelector('#form-cadastro-cliente');
const campoNome = document.querySelector('#nome-cadastro');
const campoEmail = document.querySelector('#email-cadastro');
const campoSenha = document.querySelector('#senha-cadastro');
const botaoCadastrar = document.querySelector('#botao-cadastrar');
const mensagemCadastro = document.querySelector('#mensagem-cliente');

function mostrarMensagem(elemento, texto, erro = false) {
  elemento.textContent = texto;
  elemento.className = erro ? 'mensagem erro' : 'mensagem';
  elemento.hidden = false;
}

async function requisicao(url, dados, mensagemErro) {
  let resposta;
  try {
    resposta = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dados)
    });
  } catch {
    throw new Error('Não foi possível acessar a API. Confira o backend e a configuração de CORS.');
  }

  const texto = await resposta.text();
  let conteudo = null;
  if (texto) {
    try {
      conteudo = JSON.parse(texto);
    } catch {
      throw new Error('A API retornou uma resposta inválida.');
    }
  }

  if (!resposta.ok) {
    let detalhe = conteudo?.detail;
    if (Array.isArray(detalhe)) {
      detalhe = detalhe.map(item => `${item.loc.join('.')}: ${item.msg}`).join(' | ');
    }
    throw new Error(detalhe || mensagemErro);
  }

  return conteudo;
}

formularioLogin.addEventListener('submit', async evento => {
  evento.preventDefault();

  const email = campoEmailLogin.value.trim();
  const senha = campoSenhaLogin.value;
  if (!email || !senha) {
    mostrarMensagem(mensagemLogin, 'Informe seu email e sua senha.', true);
    return;
  }

  botaoEntrar.disabled = true;
  try {
    await requisicao(
      LOGIN_API_URL,
      { email, senha },
      'Email ou senha inválidos.'
    );
    mostrarMensagem(mensagemLogin, 'Login realizado com sucesso.');
  } catch (erro) {
    mostrarMensagem(mensagemLogin, erro.message, true);
  } finally {
    botaoEntrar.disabled = false;
  }
});

formulario.addEventListener('submit', async evento => {
  evento.preventDefault();

  const nome = campoNome.value.trim();
  const email = campoEmail.value.trim();
  const senha = campoSenha.value;

  if (!nome || !email || !senha) {
    mostrarMensagem(mensagemCadastro, 'Preencha nome, email e senha.', true);
    return;
  }

  botaoCadastrar.disabled = true;
  try {
    await requisicao(API_URL, { nome_cliente: nome, email, senha }, 'Não foi possível cadastrar. Confira os dados e tente novamente.');
    formulario.reset();
    mostrarMensagem(mensagemCadastro, 'Cadastro realizado com sucesso.');
  } catch (erro) {
    mostrarMensagem(mensagemCadastro, erro.message, true);
  } finally {
    botaoCadastrar.disabled = false;
  }
});