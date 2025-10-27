console.log("✅ tables.js loaded");

let currentMonth = "may";

// Mappa dei CSV per mese
const csvFiles = {
  may: {
    as: "as_co2_final_filtered_sorted_may.csv",
    links: "enriched_as_links_may.csv"
  },
  june: {
    as: "as_co2_final_filtered_sorted_june.csv",
    links: "enriched_as_links_june.csv"
  },
  july: {
    as: "as_co2_final_filtered_sorted_july.csv",
    links: "enriched_as_links_July.csv"
  }
};

// Mappa dei plot per mese
const plotFiles = {
  may: [
    "Plots/co2_pie_interactive copy.html",
    "Plots/co2_violin_popularity_groups_interactive.html",
    "Plots/co2_vs_cc_interactive.html",
    "Plots/interactive_cdf_co2_intensity.html",
    "Plots/interactive_heatmap_top10_orgs_with_x.html"
  ],
  june: [
    "Plots/co2_pie_interactive copy.html",
    "Plots/co2_violin_popularity_groups_interactive.html",
    "Plots/co2_vs_cc_interactive.html",
    "Plots/interactive_cdf_co2_intensity.html",
    "Plots/interactive_heatmap_top10_orgs_with_x.html"
  ],
  july: [
    "Plots/co2_pie_interactive copy.html",
    "Plots/co2_violin_popularity_groups_interactive.html",
    "Plots/co2_vs_cc_interactive.html",
    "Plots/interactive_cdf_co2_intensity.html",
    "Plots/interactive_heatmap_top10_orgs_with_x.html"
  ]
};

// Load AS Table
function loadAsTable(month = currentMonth) {
  fetch(csvFiles[month].as)
    .then(res => res.text())
    .then(text => {
      const rows = text.trim().split("\n").slice(1);
      const data = rows
        .map(r => r.split(","))
        .filter(r => r.length === 4 && !isNaN(parseFloat(r[3])))
        .map(r => [r[0], r[2], parseFloat(r[3]).toFixed(2)]);

      if ($.fn.DataTable.isDataTable("#as-table")) {
        $('#as-table').DataTable().clear().destroy();
      }

      $('#as-table').DataTable({
        data,
        columns: [{ title: "ASN" }, { title: "Organization" }, { title: "CO₂ Emissions" }],
        pageLength: 10,
        order: [[2, 'asc']]
      });
    })
    .catch(err => console.error(err));
}

// Load Link Table
function loadLinkTable(month = currentMonth) {
  fetch(csvFiles[month].links)
    .then(res => res.text())
    .then(csvText => {
      const parsed = Papa.parse(csvText, { header: true, skipEmptyLines: true });
      const data = parsed.data
        .filter(r => !isNaN(parseFloat(r.Total_CO2)) && parseFloat(r.Total_CO2) > 0)
        .map(r => [r.AS1, r.AS1_org_name, r.AS2, r.AS2_org_name, parseFloat(r.Total_CO2).toFixed(2)]);

      if ($.fn.DataTable.isDataTable("#link-table")) {
        $('#link-table').DataTable().clear().destroy();
      }

      $('#link-table').DataTable({
        data,
        columns: [
          { title: "AS1" },
          { title: "AS1 Organization" },
          { title: "AS2" },
          { title: "AS2 Organization" },
          { title: "Total CO₂" }
        ],
        pageLength: 10,
        order: [[4, 'asc']]
      });
    })
    .catch(err => console.error(err));
}

// Update plots
function updatePlots(month = currentMonth) {
  const plotIds = ["plot1", "plot2", "plot3", "plot4", "plot5"];
  plotIds.forEach((id, i) => {
    const iframe = document.getElementById(id);
    if (iframe) iframe.src = plotFiles[month][i];
  });
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  // Load initial month
  loadAsTable(currentMonth);
  loadLinkTable(currentMonth);
  updatePlots(currentMonth);

  // Listen for month selection
  const monthSelect = document.getElementById("monthSelect");
  if (monthSelect) {
    monthSelect.addEventListener("change", function() {
      currentMonth = this.value;
      loadAsTable(currentMonth);
      loadLinkTable(currentMonth);
      updatePlots(currentMonth);
    });
  }
});
