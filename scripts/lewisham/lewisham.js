const path = require("path");
const fetch = require("node-fetch");
const readXlsxFile = require("read-excel-file/node");
const createCsvWriter = require("csv-writer").createArrayCsvWriter;

const PUBLIC_REGISTER_URL =
  "https://lewisham.gov.uk/-/media/files/imported/pshapublicregister.ashx";
const CSV_PATH = path.join(__dirname, "..", "..", "data", "lewisham.csv");

(async () => {
  try {
    const res = await fetch(PUBLIC_REGISTER_URL);

    if (!res.ok) {
      throw new Error(`unexpected response ${res.statusText}`);
    }

    const [header, ...rows] = await readXlsxFile(res.body);

    const csvWriter = createCsvWriter({
      header,
      path: CSV_PATH,
    });

    await csvWriter.writeRecords(rows);

    console.log(`\nScript completed successfully, see output at: ${CSV_PATH}`);
  } catch (error) {
    console.error(JSON.stringify(error, null, 2));
    console.log("\n\nScript failed, see details above.\n");
  }
})();
