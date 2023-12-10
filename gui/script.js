const chartContext = document.getElementById("radial-chart").getContext("2d");
let myChart = null;
let chartType = "radar";

const questions = [
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

function initializeChart(chartType, questions, dataSets) {
  if (myChart) {
    myChart.destroy();
  }

  myChart = new Chart(chartContext, {
    type: chartType,
    data: {
      labels: questions,
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

function generateDatasets(labels, questions) {
  return labels.map((label) => ({
    label: label,
    data: new Array(questions.length).fill(0),
    fill: true,
    // borderColor: `rgb(${randomColorValue()}, ${randomColorValue()}, ${randomColorValue()})`,
    // backgroundColor: `rgba(${randomColorValue()}, ${randomColorValue()}, ${randomColorValue()}, 0.5)`,
  }));
}

function createTable(containerId, dataSetLabels, questions, dataSets) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";

  const table = document.createElement("table");
  const thead = document.createElement("thead");
  const tbody = document.createElement("tbody");

  const headerRow = document.createElement("tr");
  headerRow.appendChild(createCell("th", "Questions"));
  dataSetLabels.forEach((label) =>
    headerRow.appendChild(createCell("th", label))
  );
  thead.appendChild(headerRow);

  questions.forEach((question, qIndex) => {
    const row = document.createElement("tr");
    row.appendChild(createCell("td", question));

    dataSets.forEach((dataSet, dsIndex) => {
      const cell = createCell("td");
      const input = document.createElement("input");
      input.type = "number";
      input.classList.add("w-16", "text-center", "border");
      input.value = dataSet.data[qIndex];
      input.addEventListener("input", (e) => {
        dataSet.data[qIndex] = Number(e.target.value);
        initializeChart(chartType, questions, dataSets);
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
      generateDatasets([`DataSet ${dataSets.length + 1}`], questions)[0]
    );
  }
} else {
  dataSets = generateDatasets(dataSetLabels, questions);
  localStorage.setItem("chart_data", JSON.stringify(dataSets));
}

if (localStorage.getItem("chart_type")) {
  chartType = localStorage.getItem("chart_type");
  document.querySelector("#chart-type").value = chartType;
}
initializeChart(chartType, questions, dataSets);
createTable("table-container", dataSetLabels, questions, dataSets);

document.getElementById("chart-type").addEventListener("change", (e) => {
  chartType = e.target.value;
  initializeChart(chartType, questions, dataSets);
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
        generateDatasets([`DataSet ${newDataSets.length + 1}`], questions)[0]
      );
    }

    createTable("table-container", newDataSetLabels, questions, newDataSets);
    initializeChart(chartType, questions, newDataSets);
    localStorage.setItem("chart_number-of-datasets", newLabelCount);
    localStorage.setItem("chart_data", JSON.stringify(newDataSets));
  });

document.querySelector("#delete").onclick = () => {
  localStorage.removeItem("chart_number-of-datasets");
  localStorage.removeItem("chart_data");
  localStorage.removeItem("chart_type");
  window.location.reload();
};
