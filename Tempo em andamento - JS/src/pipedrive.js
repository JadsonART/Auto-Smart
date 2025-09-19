import CONFIG from "./config.js";

export function callPipedrive(endpoint, method = "GET", payload = null) {
  const sep = endpoint.includes("?") ? "&" : "?";
  const url = `${CONFIG.BASE_URL}/${endpoint}${sep}api_token=${CONFIG.API_KEY}`;

  const opts = {
    method: method.toUpperCase(),
    headers: { "Content-Type": "application/json" },
    muteHttpExceptions: true,
  };

  if (payload) opts.payload = JSON.stringify(payload);

  const res = UrlFetchApp.fetch(url, opts);
  const json = JSON.parse(res.getContentText());

  if (!json.success) throw new Error(json.error || res.getContentText());
  return json.data;
}
