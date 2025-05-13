let registros = [];

document.getElementById('registroForm').addEventListener('submit', function (e) {
  e.preventDefault();
  const formData = new FormData(e.target);
  const registro = Object.fromEntries(formData);
  registros.push(registro);
  atualizarTabela();
  e.target.reset();
  alert("Saída registrada com sucesso!");
});

function atualizarTabela() {
  const tbody = document.getElementById('tabelaRegistros');
  tbody.innerHTML = '';
  registros.forEach((r, i) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${r.nome}</td>
      <td>${r.serie}</td>
      <td>${r.responsavel}</td>
      <td>${r.data_saida}</td>
      <td>${r.motivo}</td>
      <td>
        <button class="btn btn-sm btn-danger" onclick="excluirRegistro(${i})">Excluir</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function excluirRegistro(index) {
  if (confirm("Deseja excluir este registro?")) {
    registros.splice(index, 1);
    atualizarTabela();
  }
}

function filtrarRegistros() {
  const termo = document.getElementById('filtroNome').value.toLowerCase();
  const linhas = document.querySelectorAll('#tabelaRegistros tr');
  linhas.forEach(linha => {
    const nome = linha.children[0].textContent.toLowerCase();
    linha.style.display = nome.includes(termo) ? '' : 'none';
  });
}

function gerarRegistrosTeste() {
  for (let i = 1; i <= 5; i++) {
    registros.push({
      nome: `Aluno ${i}`,
      serie: `${i}º ano`,
      responsavel: `Responsável ${i}`,
      data_saida: new Date().toISOString().slice(0, 16),
      motivo: "Consulta médica"
    });
  }
  atualizarTabela();
}

async function gerarPDF() {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();
  let y = 20;

  doc.setFontSize(16);
  doc.text("Relatório de Saídas Antecipadas", 105, y, { align: 'center' });
  y += 10;
  doc.setFontSize(10);

  const nomeFiltro = document.getElementById('filtroNome').value.toLowerCase();

  const filtrados = registros.filter(r => r.nome.toLowerCase().includes(nomeFiltro));

  if (filtrados.length === 0) {
    alert("Nenhum registro para exportar.");
    return;
  }

  filtrados.forEach((r, i) => {
    const linha = `${r.data_saida} | ${r.nome} | ${r.serie} | ${r.responsavel} | ${r.motivo}`;
    doc.text(linha, 10, y);
    y += 8;

    if (y > 280) {
      doc.addPage();
      y = 20;
    }
  });

  doc.save("relatorio-saidas.pdf");
}
