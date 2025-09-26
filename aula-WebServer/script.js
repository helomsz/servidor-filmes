const lis = document.querySelector('#filmes');
 
fetch('http://localhost:8000/get_lista').then((res) => {
    return res.json();
}).then ((data) => {
    data.map((lista) => {
        console.log(lista)
        lis.innerHTML +=
        `
        <li>
        <img src="${lista.capa}"/> </br>
        <strong>Nome do filme:</strong> ${lista.nome} </br>
        <strong>Atores:</strong> ${lista.atores} </br>
        <strong>Diretor(a):</strong> ${lista.diretor} </br>
        <strong>Data:</strong> ${lista.data} </br>
        <strong>Gênero:</strong> ${lista.genero} </br>
        <strong>Produtora:</strong> ${lista.produtora} </br>
        <strong>Sinopse:</strong> ${lista.sinopse} </br>
        </li>
        `
    })
})
 