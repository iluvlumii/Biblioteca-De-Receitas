const API_URL = "http://127.0.0.1:8000";

const formLogin = document.getElementById("form-login");
const formCadastro = document.getElementById("form-cadastro-cliente");
const mensagemLogin = document.getElementById("mensagem");
const mensagemCadastro = document.getElementById("mensagem-cliente");
const botaoEntrar = document.getElementById("botao-Entrar");
const botaoCadastrar = document.getElementById("botao-cadastrar");

function mostrarMensagem(elemento, texto, erro) {
  elemento.textContent = texto;
  elemento.classList.toggle("erro", erro);
  elemento.hidden = false;
}

function textoDoErro(dados) {
  if (!dados || !dados.detail) {
    return "Não foi possível concluir a operação.";
  }
  if (typeof dados.detail === "string") {
    return dados.detail;
  }
  if (Array.isArray(dados.detail)) {
    return dados.detail
      .map(function (item) {
        const campo = item.loc[item.loc.length - 1];
        return campo + ": " + item.msg;
      })
      .join(" | ");
  }
  return "Não foi possível concluir a operação.";
}

async function enviar(caminho, corpo) {
  const resposta = await fetch(API_URL + caminho, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(corpo),
  });
  let dados = null;
  try {
    dados = await resposta.json();
  } catch (erro) {
    dados = null;
  }
  return { ok: resposta.ok, status: resposta.status, dados: dados };
}

formCadastro.addEventListener("submit", async function (evento) {
  evento.preventDefault();
  botaoCadastrar.disabled = true;
  try {
    const resultado = await enviar("/pessoa", {
      nome_pessoa: document.getElementById("nome-cadastro").value.trim(),
      email_pessoa: document.getElementById("email-cadastro").value.trim(),
      senha_pessoa: document.getElementById("senha-cadastro").value,
      datanasc_pessoa: document.getElementById("datanasc-cadastro").value,
    });
    if (resultado.ok) {
      mostrarMensagem(
        mensagemCadastro,
        "Conta criada com sucesso! Agora você já pode entrar.",
        false
      );
      formCadastro.reset();
    } else {
      mostrarMensagem(mensagemCadastro, textoDoErro(resultado.dados), true);
    }
  } catch (erro) {
    mostrarMensagem(
      mensagemCadastro,
      "Não foi possível falar com a API. Confira se o backend está rodando.",
      true
    );
  } finally {
    botaoCadastrar.disabled = false;
  }
});

formLogin.addEventListener("submit", async function (evento) {
  evento.preventDefault();
  botaoEntrar.disabled = true;
  try {
    const resultado = await enviar("/pessoa/login", {
      email_pessoa: document.getElementById("email").value.trim(),
      senha_pessoa: document.getElementById("senha").value,
    });
    if (resultado.ok) {
      sessionStorage.setItem("pessoa", JSON.stringify(resultado.dados));
      mostrarMensagem(
        mensagemLogin,
        "Bem-vindo(a), " + resultado.dados.nome_pessoa + "!",
        false
      );
      setTimeout(function () {
        window.location.href = "index.html";
      }, 1200);
    } else {
      mostrarMensagem(mensagemLogin, textoDoErro(resultado.dados), true);
    }
  } catch (erro) {
    mostrarMensagem(
      mensagemLogin,
      "Não foi possível falar com a API. Confira se o backend está rodando.",
      true
    );
  } finally {
    botaoEntrar.disabled = false;
  }
});

document
  .getElementById("botao-Entrar-no-Google")
  .addEventListener("click", function () {
    mostrarMensagem(
      mensagemLogin,
      "Entrar com Google ainda não está disponível.",
      true
    );
  });

document
  .getElementById("botao-Entrar-no-Apple")
  .addEventListener("click", function () {
    mostrarMensagem(
      mensagemLogin,
      "Entrar com Apple ainda não está disponível.",
      true
    );
  });