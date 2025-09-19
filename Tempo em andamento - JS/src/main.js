import CONFIG from "./config.js";
import { callPipedrive } from "./pipedrive.js";
import { getOldObject, jsonOut } from "./utils.js";
import { salvarLogEmPlanilha, logError } from "./log.js";

function doPost(e) {
  try {
    const raw = e?.postData?.contents || "";
    if (!raw || raw === "{}") throw Error("Evento sem corpo postData");

    let payload = JSON.parse(raw);
    const { meta = {}, data = {}, previous = {} } = payload;
    const { action = "", entity = "" } = meta;

    const customFieldChanged = Object.keys(previous?.custom_fields || {});
    const systemFieldChanged = Object.keys(previous || {}).filter(f => f !== "custom_fields");
    const changedKeys = customFieldChanged.concat(systemFieldChanged);

    const oldPayload = getOldObject(data);

    if (entity === "deal") {
      if (!data?.id) {
        salvarLogEmPlanilha({ id: data?.id || "", title: "" }, ["Evento não é de um deal"]);
        throw Error("Evento não é de um deal");
      }

      salvarLogEmPlanilha(data, changedKeys);
    }

    return jsonOut({ ok: true });
  } catch (error) {
    logError(e, error, "doPost");
    return jsonOut({ ok: false, error: error.message });
  }
}
