import CONFIG from "./config.js";

export function logError(event, error = null, functionName = "Não adicionado") {
  const planilhaLog = SpreadsheetApp.openById(CONFIG.SHEET_ID);
  planilhaLog.getSheetByName("Erros").appendRow([
    new Date(),
    JSON.stringify(event),
    error?.message || "Sem dados",
    error?.stack || "Sem dados",
    functionName,
  ]);
}

export function salvarLogEmPlanilha(deal, alteracoes) {
  const ss = SpreadsheetApp.openById(CONFIG.SHEET_ID);
  const sheet = ss.getSheetByName("Logs") || ss.insertSheet("Logs");

  if (sheet.getLastRow() === 0) {
    sheet.appendRow(["Data", "ID Negócio", "Nome", "Alterações", "JSON"]);
  }

  const alteracoesTexto =
    alteracoes.length > 0 ? alteracoes.join(", ") : "Nenhuma alteração";

  sheet.appendRow([new Date(), deal.id, deal.title, alteracoesTexto, JSON.stringify(deal)]);
}
