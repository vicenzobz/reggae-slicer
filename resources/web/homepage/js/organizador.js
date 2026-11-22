// Reggae Slicer: seção "Organizador 3D" da página inicial.
// Pede ao programa o resumo que o Organizador 3D grava (reggae-slicer.json: fila, projetos e
// estoque) e mostra as próximas peças, os projetos ativos e os rolos. Clicar numa peça abre o
// arquivo dela no fatiador. Atualiza a cada 30 s, então reflete o que mudou no Organizador.

var Reggae = { dados: null };

function ReggaePedir() {
	SendWXMessage(JSON.stringify({ sequence_id: Math.round(new Date() / 1000), command: "reggae_get_organizador" }));
}

function ReggaeAbrir(caminho) {
	SendWXMessage(JSON.stringify({ sequence_id: Math.round(new Date() / 1000), command: "reggae_open_file", data: { path: caminho } }));
}

function ReggaeEsc(t) {
	return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) {
		return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
	});
}

function ReggaeCor(hex) {
	return /^#[0-9a-fA-F]{6}$/.test(hex || "") ? hex : "#888888";
}

function ReggaeMostrar(msg) {
	let area = document.getElementById("ReggaeArea");
	if (!area)
		return;
	if (!msg["ok"]) {
		area.innerHTML = '<div class="ReggaeTitulo TextS1">Organizador 3D</div>' +
			'<div class="ReggaeVazio">Abra o Organizador 3D uma vez para os seus projetos, a fila e o estoque aparecerem aqui.</div>';
		return;
	}
	let d = msg["response"] || {};
	Reggae.dados = d;
	let html = '<div class="ReggaeCabecalho"><div class="ReggaeTitulo TextS1">Organizador 3D</div>' +
		'<div class="ReggaeHora">atualizado ' + ReggaeEsc(d["gerado"] || "") + '</div></div>';

	// fila
	let fila = d["fila"] || [];
	html += '<div class="ReggaeSecao">Fila de impressão <span>' + fila.length + ' peças</span></div>';
	if (!fila.length)
		html += '<div class="ReggaeVazio">Nada na fila.</div>';
	html += '<div class="ReggaeFila">';
	fila.slice(0, 14).forEach(function (p, i) {
		let cores = (p["cores"] || []).map(function (c) {
			return '<span class="ReggaeBolinha" title="' + ReggaeEsc(c["nome"]) + '" style="background:' + ReggaeCor(c["hex"]) + '"></span>';
		}).join("");
		let abrir = p["arquivo"] ? '<div class="ReggaeAbrir" data-i="' + i + '">Abrir</div>' : '<div class="ReggaeSemArquivo">sem arquivo</div>';
		html += '<div class="ReggaePeca">' +
			'<div class="ReggaeId">' + ReggaeEsc(p["id"]) + '</div>' +
			'<div class="ReggaeNome"><div>' + ReggaeEsc(p["peca"]) + '</div><small>' + ReggaeEsc(p["projeto"] || "") + '</small></div>' +
			'<div class="ReggaeCores">' + cores + '</div>' +
			'<div class="ReggaeStatus">' + ReggaeEsc(p["status"]) + '</div>' + abrir + '</div>';
	});
	html += '</div>';

	// projetos
	let projetos = d["projetos"] || [];
	html += '<div class="ReggaeSecao">Projetos ativos <span>' + projetos.length + '</span></div><div class="ReggaeProjetos">';
	projetos.forEach(function (p) {
		let prazo = p["prazo"] ? '<small>prazo ' + ReggaeEsc(p["prazo"]) + '</small>' : '';
		html += '<div class="ReggaeProjeto"><div class="ReggaeNome"><div>' + ReggaeEsc(p["nome"]) + '</div>' + prazo + '</div>' +
			'<div class="ReggaeConta">' + ReggaeEsc(p["pendentes"]) + ' a imprimir</div></div>';
	});
	html += '</div>';

	// estoque
	let rolos = d["estoque"] || [];
	html += '<div class="ReggaeSecao">Estoque de filamento <span>' + rolos.length + ' rolos</span></div><div class="ReggaeEstoque">';
	rolos.forEach(function (r) {
		let resto = (r["restante"] === null || r["restante"] === undefined) ? "?" : r["restante"] + " g";
		html += '<div class="ReggaeRolo" title="' + ReggaeEsc((r["material"] || "") + " " + (r["marca"] || "")) + '">' +
			'<span class="ReggaeBolinha Grande" style="background:' + ReggaeCor(r["hex"]) + '"></span>' +
			'<div><div>' + ReggaeEsc(r["cor"]) + '</div><small>' + ReggaeEsc(resto) + '</small></div></div>';
	});
	html += '</div>';

	area.innerHTML = html;
	$(area).find(".ReggaeAbrir").on("click", function () {
		let p = (Reggae.dados["fila"] || [])[parseInt($(this).attr("data-i"))];
		if (p && p["arquivo"])
			ReggaeAbrir(p["arquivo"]);
	});
}

(function () {
	let anterior = window.postMessage;
	window.postMessage = function (pVal) {
		if (pVal && pVal["command"] == "reggae_organizador") {
			ReggaeMostrar(pVal);
			return;
		}
		return anterior.apply(this, arguments);
	};
	window.addEventListener("load", function () {
		ReggaePedir();
		setInterval(ReggaePedir, 30000);
	});
})();
