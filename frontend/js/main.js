const switchEl = document.getElementById("modeSwitch");
const titleGroup = document.getElementById("titleGroup");
const fileGroup = document.getElementById("fileGroup");
const textGroup = document.getElementById("textGroup");

const fileInput = document.getElementById("fileInput");
const titleInput = document.getElementById("titleInput");
const textInput = document.getElementById("textInput");

const loading = document.getElementById("loading");
const resultsContainer = document.getElementById("resultsContainer");
const resultsList = document.getElementById("resultsList");

switchEl.addEventListener("change", () => {
  if (switchEl.checked) {
    titleGroup.classList.add("d-none");
    textGroup.classList.add("d-none");
    fileGroup.classList.remove("d-none");
  } else {
    titleGroup.classList.remove("d-none");
    textGroup.classList.remove("d-none");
    fileGroup.classList.add("d-none");
  }
  titleInput.value = "";
  textInput.value = "";
  fileInput.value = null;
});

document.getElementById("emailForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  loading.classList.remove("d-none");

  const formData = new FormData();
  let displayTitle = "";

  if (switchEl.checked) {
    if (!fileInput.files[0]) {
      alert("Selecione um arquivo antes de enviar.");
      loading.classList.add("d-none");
      return;
    }
    formData.append("emailFile", fileInput.files[0]);
    displayTitle = fileInput.files[0].name;
  } else {
    const title = titleInput.value.trim();
    const body = textInput.value.trim();
    if (!title) {
      alert("Preencha o campo de título antes de enviar.");
      loading.classList.add("d-none");
      return;
    }
    if (!body) {
      alert("Cole o texto do email antes de enviar.");
      loading.classList.add("d-none");
      return;
    }
    formData.append("emailTitle", title);
    formData.append("emailText", body);
    displayTitle = title;
  }

  try {
    const resp = await fetch("/classificar", {
      method: "POST",
      body: formData,
    });
    if (!resp.ok) throw new Error(`Status ${resp.status}`);
    const data = await resp.json();

    const li = document.createElement("li");
    li.classList.add("list-group-item", "result-item");
    li.style.cursor = "pointer";

    const linha = document.createElement("div");
    linha.classList.add("d-flex", "align-items-center", "gap-2");

    const tag = document.createElement("span");
    tag.classList.add("result-tag");
    tag.textContent = data.categoria.toUpperCase();

    if (data.categoria.toLowerCase() === "produtivo") {
      tag.classList.add("produtivo");
    } else {
      tag.classList.add("improdutivo");
    }

    const titleSpan = document.createElement("span");
    titleSpan.textContent = displayTitle || "Sem título";

    linha.appendChild(tag);
    linha.appendChild(titleSpan);
    li.appendChild(linha);

    if (data.resposta && data.resposta.trim() !== "") {
      const resposta = document.createElement("div");
      resposta.classList.add("resposta-sugerida");

      // Container flexível para alinhar botão e texto
      const container = document.createElement("div");
      container.classList.add("d-flex", "align-items-start", "gap-3");

      // Botão de copiar (vai ficar à esquerda)
      const copyBtn = document.createElement("button");
      copyBtn.textContent = "📋 Copiar";
      copyBtn.classList.add("btn", "btn-sm", "btn-outline-success");

      // Texto da resposta
      const texto = document.createElement("div");
      texto.innerHTML = `<em>Resposta sugerida:</em><br><strong>${data.resposta}</strong>`;

      // Adicionar ao container
      container.appendChild(copyBtn);
      container.appendChild(texto);
      resposta.appendChild(container);

      // Evento de cópia
      copyBtn.addEventListener("click", async (e) => {
        e.stopPropagation(); // evita abrir/fechar ao clicar no botão
        try {
          await navigator.clipboard.writeText(data.resposta);
          copyBtn.textContent = "✅ Copiado!";
          setTimeout(() => (copyBtn.textContent = "📋 Copiar"), 2000);
        } catch (err) {
          console.error("Erro ao copiar:", err);
          alert("Não foi possível copiar o texto.");
        }
      });

      resposta.style.display = "none";
      li.appendChild(resposta);

      li.addEventListener("click", (e) => {
        if (e.target !== copyBtn) {
          resposta.style.display =
            resposta.style.display === "none" ? "block" : "none";
        }
      });
    }

    resultsList.prepend(li);
    resultsContainer.classList.remove("d-none");
  } catch (err) {
    console.error(err);
    alert("Ocorreu um erro ao classificar o email.");
  } finally {
    loading.classList.add("d-none");
  }
});
