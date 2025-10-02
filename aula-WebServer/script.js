const lis = document.querySelector('#filmes');

if (lis) {
  fetch('http://localhost:8000/listarfilmes')
    .then((res) => res.json())
    .then((data) => {
      data.map((lista) => {
        lis.innerHTML += `
          <li>
            <img src="${lista.capa || ''}"/> </br>
            <strong>Nome do filme:</strong> ${lista.nome} </br>
            <strong>Atores:</strong> ${lista.atores} </br>
            <strong>Diretor(a):</strong> ${lista.diretor} </br>
            <strong>Data:</strong> ${lista.ano} </br>
            <strong>Gênero:</strong> ${lista.genero} </br>
            <strong>Produtora:</strong> ${lista.produtora} </br>
            <strong>Sinopse:</strong> ${lista.sinopse} </br>
            <button onclick='deleteFilme(${lista.id})'>Excluir</button>
            <button onclick="window.location.href='editar.html?id=${lista.id}'">Editar</button>
          </li>
        `;
      });
    });
}



document.getElementById("formEditar").addEventListener("submit", function(e) {
    e.preventDefault();

    const id = document.getElementById('id').value;

    const filme = {
        id: id,
        nome: document.getElementById('nome').value || undefined,
        atores: document.getElementById('atores').value || undefined,
        diretor: document.getElementById('diretor').value || undefined,
        ano: document.getElementById('ano').value || undefined,
        genero: document.getElementById('genero').value || undefined,
        produtora: document.getElementById('produtora').value || undefined,
        sinopse: document.getElementById('sinopse').value || undefined,
    };

    fetch('http://localhost:8000/editarfilme', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(filme).toString(),
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            window.location.href = '/lista';
        } else {
            alert('Erro ao atualizar o filme.');
        }
    })
    .catch(err => console.error("Erro:", err));
});



function deleteFilme(id) {
  if (confirm('Tem certeza que deseja excluir este filme?')) {
    fetch(`http://localhost:8000/deletarfilme`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ id }).toString() 
    })
    .then(res => res.json())
    .then(data => {
      alert(data.message || "Filme excluído com sucesso!");
        location.reload(); 
    })
    .catch(err => console.error(err));
  }
}

// --- Novo código para carregar e preencher o formulário de edição ---

// Função para obter o parâmetro 'id' da URL
function getFilmeIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

// Função para buscar os dados de todos os filmes e encontrar o filme pelo ID
function preencherFormularioEdicao() {
    const filmeId = getFilmeIdFromUrl();
    const form = document.getElementById('formEditar');

    // Se a página não for a de edição (ou o ID não estiver na URL), não faz nada.
    if (!form || filmeId === null) {
        return;
    }
    
    // Busca os dados de todos os filmes do servidor
    fetch('http://localhost:8000/listarfilmes')
        .then(res => res.json())
        .then(filmes => {
            // Encontra o filme com o ID correspondente
            const filmeParaEditar = filmes.find(f => f.id === parseInt(filmeId));

            if (filmeParaEditar) {
                // Preenche os campos do formulário
                document.getElementById('id').value = filmeParaEditar.id;
                document.getElementById('nome').value = filmeParaEditar.nome;
                document.getElementById('atores').value = filmeParaEditar.atores;
                document.getElementById('diretor').value = filmeParaEditar.diretor;
                document.getElementById('ano').value = filmeParaEditar.ano;
                document.getElementById('genero').value = filmeParaEditar.genero;
                document.getElementById('produtora').value = filmeParaEditar.produtora;
                document.getElementById('sinopse').value = filmeParaEditar.sinopse;
            } else {
                alert("Filme não encontrado para edição.");
                window.location.href = '/lista'; // Redireciona de volta
            }
        })
        .catch(err => console.error("Erro ao buscar filmes para edição:", err));
}

// Chama a função ao carregar a página
preencherFormularioEdicao();