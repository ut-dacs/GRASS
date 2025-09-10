console.log("✅ tables.js loaded");

function loadAsTable() {
  console.log("✅ loadAsTable called");

  fetch("as_co2_final_filtered_sorted.csv")
    .then(res => res.text())
    .then(text => {
      const rows = text.trim().split("\n").slice(1); // salta intestazione

      const data = rows
        .map(row => row.split(","))
        .filter(r => r.length === 4 && !isNaN(parseFloat(r[3])))
        .map(r => [
          r[0],                // ASnumber
          r[2],                // AS_Organization
          parseFloat(r[3]).toFixed(2)  // CO2_Intensity
        ]);

      // Distruggi solo se già esiste
      if ($.fn.DataTable.isDataTable("#as-table")) {
        $('#as-table').DataTable().clear().destroy();
      }

      // Crea la tabella con DataTables
      $('#as-table').DataTable({
        data: data,
        columns: [
          { title: "ASN" },
          { title: "Organization" },
          { title: "CO₂ Emissions" }
        ],
        pageLength: 10,
        lengthChange: false,
        order: [[2, 'asc']],
        searching: true,
        paging: true,
        info: true
      });

      console.log("✅ AS DataTable initialized");
    })
    .catch(err => console.error("❌ Error loading AS table:", err));
}



function loadLinkTable() {
  console.log("✅ loadLinkTable called");

  fetch("enriched_as_links.csv")
    .then(res => res.text())
    .then(csvText => {
      // ✅ Parse CSV with quotes/commas using PapaParse
      const parsed = Papa.parse(csvText, {
        header: true,
        skipEmptyLines: true
      });

      // ✅ Filter and format data
      const data = parsed.data
        .filter(row => 
          !isNaN(parseFloat(row.Total_CO2)) && 
          parseFloat(row.Total_CO2) > 0
        )
        .map(row => [
          row.AS1,
          row.AS1_org_name,
          row.AS2,
          row.AS2_org_name,
          parseFloat(row.Total_CO2).toFixed(2)
        ]);

      // ✅ Destroy existing table if present
      if ($.fn.DataTable.isDataTable("#link-table")) {
        $('#link-table').DataTable().clear().destroy();
      }

      // ✅ Create new table
      $('#link-table').DataTable({
        data: data,
        columns: [
          { title: "AS1" },
          { title: "AS1 Organization" },
          { title: "AS2" },
          { title: "AS2 Organization" },
          { title: "Total CO₂" }
        ],
        pageLength: 10,
        order: [[4, 'asc']],
        searching: true,
        paging: true,
        info: true
      });

      console.log("✅ link-table initialized");
    })
    .catch(err => console.error("❌ Error loading link table:", err));
}




document.addEventListener("DOMContentLoaded", function () {
  loadAsTable();     
  loadLinkTable();  
});
