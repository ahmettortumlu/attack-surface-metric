const tabLabels = document.querySelectorAll(".tab-label");
const tabs = document.querySelectorAll(".tab-content");

tabLabels.forEach(label => {
    label.addEventListener('click', function() {

        tabLabels.forEach(lbl => lbl.classList.remove('border-b-black'));
        this.classList.add( 'border-b-black');

        tabs.forEach(tab => {
            tab.classList.add('w-0');
            tab.classList.remove('w-screen');
        });
     
        const tabId = label.id.replace('-label', '');
      
        document.querySelector(`#${tabId}`).classList.add('w-screen');
        document.querySelector(`#${tabId}`).classList.remove('w-0');
    });
});


////////////////////// result tab

const chartContext = document.getElementById("radial-chart").getContext("2d");
let myChart = null;
let chartType = "radar";

const parameters = [
  "ddis",
  "dyn",
  "security",
  "input",
  "active",
  "cookie",
  "role",
  "rights",
  "infra",
];

function createDataSetLabels(count) {
  return Array.from({ length: count }, (_, i) => `DataSet ${i + 1}`);
}

function initializeChart(chartType, parameters, dataSets) {
  if (myChart) {
    myChart.destroy();
  }

  myChart = new Chart(chartContext, {
    type: chartType,
    data: {
      labels: parameters,
      datasets: dataSets,
    },
    options: {
      scales: {
        r: {
          beginAtZero: true,
        },
      },
    },
  });
}

function generateDatasets(labels, parameters) {
  return labels.map((label) => ({
    label: label,
    data: new Array(parameters.length).fill(0),
    fill: true,
    // borderColor: `rgb(${randomColorValue()}, ${randomColorValue()}, ${randomColorValue()})`,
    // backgroundColor: `rgba(${randomColorValue()}, ${randomColorValue()}, ${randomColorValue()}, 0.5)`,
  }));
}

function createTable(containerId, dataSetLabels, parameters, dataSets) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";

  const table = document.createElement("table");
  const thead = document.createElement("thead");
  const tbody = document.createElement("tbody");

  const headerRow = document.createElement("tr");
  headerRow.appendChild(createCell("th", "Parameters"));
  dataSetLabels.forEach((label) =>
    headerRow.appendChild(createCell("th", label))
  );
  thead.appendChild(headerRow);

  parameters.forEach((parameter, qIndex) => {
    const row = document.createElement("tr");
    row.appendChild(createCell("td", parameter));

    dataSets.forEach((dataSet, dsIndex) => {
      const cell = createCell("td");
      const input = document.createElement("input");
      input.type = "number";
      input.classList.add("w-16", "text-center", "border");
      input.value = dataSet.data[qIndex];
      input.addEventListener("input", (e) => {
        dataSet.data[qIndex] = Number(e.target.value);
        initializeChart(chartType, parameters, dataSets);
        localStorage.setItem("chart_data", JSON.stringify(dataSets));
      });
      cell.appendChild(input);
      row.appendChild(cell);
    });

    tbody.appendChild(row);
  });

  table.appendChild(thead);
  table.appendChild(tbody);
  container.appendChild(table);
}

function createCell(type, text = "") {
  const cell = document.createElement(type);
  cell.textContent = text;
  return cell;
}

function randomColorValue() {
  return Math.floor(Math.random() * 256);
}

let countDatasetLabel = 4;
if (localStorage.getItem("chart_number-of-datasets")) {
  countDatasetLabel = Number(localStorage.getItem("chart_number-of-datasets"));
  document.querySelector("#number-of-datasets").value = countDatasetLabel;
}

let dataSetLabels = createDataSetLabels(countDatasetLabel);
let dataSets = [];

if (localStorage.getItem("chart_data")) {
  dataSets = JSON.parse(localStorage.getItem("chart_data"));
  dataSets = dataSets.slice(0, countDatasetLabel);
  while (dataSets.length < countDatasetLabel) {
    dataSets.push(
      generateDatasets([`DataSet ${dataSets.length + 1}`], parameters)[0]
    );
  }
} else {
  dataSets = generateDatasets(dataSetLabels, parameters);
  localStorage.setItem("chart_data", JSON.stringify(dataSets));
}

if (localStorage.getItem("chart_type")) {
  chartType = localStorage.getItem("chart_type");
  document.querySelector("#chart-type").value = chartType;
}
initializeChart(chartType, parameters, dataSets);
createTable("table-container", dataSetLabels, parameters, dataSets);

document.getElementById("chart-type").addEventListener("change", (e) => {
  chartType = e.target.value;
  initializeChart(chartType, parameters, dataSets);
  localStorage.setItem("chart_type", chartType);
});

document
  .getElementById("number-of-datasets")
  .addEventListener("change", (e) => {
    const newLabelCount = Number(e.target.value);

    const newDataSetLabels = createDataSetLabels(newLabelCount);
    let newDataSets = JSON.parse(localStorage.getItem("chart_data")) || [];
    newDataSets = newDataSets.slice(0, newLabelCount);
    while (newDataSets.length < newLabelCount) {
      newDataSets.push(
        generateDatasets([`DataSet ${newDataSets.length + 1}`], parameters)[0]
      );
    }

    createTable("table-container", newDataSetLabels, parameters, newDataSets);
    initializeChart(chartType, parameters, newDataSets);
    localStorage.setItem("chart_number-of-datasets", newLabelCount);
    localStorage.setItem("chart_data", JSON.stringify(newDataSets));
  });

document.querySelector("#delete").onclick = () => {
  localStorage.removeItem("chart_number-of-datasets");
  localStorage.removeItem("chart_data");
  localStorage.removeItem("chart_type");
  window.location.reload();
};

