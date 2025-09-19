export function jsonOut(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

export function getOldObject(webhookEventData) {
  const { custom_fields } = webhookEventData;
  let newObject = Object.assign({}, webhookEventData, custom_fields);
  delete newObject.custom_fields;

  Object.keys(newObject).forEach(key => {
    const value = newObject[key];
    if (value && typeof value === "object") {
      newObject[key] = value.value;
    }
  });

  return newObject;
}
