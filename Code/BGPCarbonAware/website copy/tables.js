console.log("✅ tables.js loaded");

function loadAsTable() {
  console.log("✅ loadAsTable called");

  fetch("asn_emissions_with_org.csv")
    .then(res => res.text())
    .then(text => {
      const rows = text.trim().split("\n").slice(1);
      const tbody = document.querySelector("#as-table tbody");
      tbody.innerHTML = "";

      rows.map(row => row.split(","))
        .filter(r => r.length === 3 && !isNaN(parseFloat(r[2])))
        .sort((a, b) => parseFloat(a[2]) - parseFloat(b[2]))
        .forEach(([asn, org, co2]) => {
          const tr = document.createElement("tr");
          tr.innerHTML = `<td>${asn}</td><td>${org}</td><td>${parseFloat(co2).toFixed(2)}</td>`;
          tbody.appendChild(tr);
        });

      if ($.fn.DataTable.isDataTable("#as-table")) {
        $('#as-table').DataTable().clear().destroy();
      }

      $('#as-table').DataTable({
        pageLength: 10,
        lengthChange: false
      });
    });
}

function loadLinkTable() {
  console.log("✅ loadLinkTable called");

  fetch("as_links_sorted.csv")
    .then(res => res.text())
    .then(text => {
      const rows = text.trim().split("\n").slice(1);
      const data = rows
        .map(row => row.split(","))
        .filter(r => r.length === 3 && !isNaN(parseFloat(r[2])));

      const tbody = document.querySelector("#link-table tbody");
      tbody.innerHTML = "";

      data.forEach(([as1, as2, total]) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `<td>${as1}</td><td>${as2}</td><td>${parseFloat(total).toFixed(2)}</td>`;
        tbody.appendChild(tr);
      });

      if ($.fn.DataTable.isDataTable("#link-table")) {
        $('#link-table').DataTable().clear().destroy();
      }

      $('#link-table').DataTable({
        pageLength: 10,
        lengthChange: false,
        order: [[2, 'asc']],
        searching: true,
        paging: true,
        info: true
      });

      console.log("✅ DataTable initialized");
    })
    .catch(err => console.error("❌ Error loading link table:", err));
}

document.addEventListener("DOMContentLoaded", () => {
  loadAsTable();
  //loadLinkTable();
});