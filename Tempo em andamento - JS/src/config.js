const CONFIG = {
  PIPEDRIVE_TOKEN: process.env.PIPEDRIVE_TOKEN,
  API_KEY: process.env.API_KEY,
  SHEET_ID: process.env.SHEET_ID,
  PIPELINE_ID: process.env.PIPELINE_ID || 1,
  EMAIL_DESTINO: process.env.EMAIL_DESTINO || "",
  BASE_URL: "https://api.pipedrive.com/v1",
  PAGE_SIZE: 50,
  PROP_KEY: "pipedrive_offset",
  LAST_RESET_KEY: "last_reset_date",
};

export default CONFIG;
