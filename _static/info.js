let prod_fct = js_vars.prod_fct;
let P5IsDummy = prod_fct.length == 4;

// Payoff chart
const ctx = document.getElementById('payoff-chart');

let chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: Array.from(Array(prod_fct.length).keys()),
        datasets: [{
            label: "Subgroup's value",
            data: prod_fct,
            borderWidth: 1,
            borderColor: "#056fb7",
            backgroundColor: "#5994c7"
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            },
            x: {
                title: {
                    text: "P1 + this many others in subgroup" + (P5IsDummy ? " (excluding P5)" : ""),
                    display: true
                }
            }
        },
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            },
        }
    }
});

// Payoff table
payoffTableHeader = document.getElementById('payoff-table-header');
payoffTableRow = document.getElementById('payoff-table-values');

if (P5IsDummy) {
    let coalitionSizeHeader = document.getElementById('payoff-table-header-title');
    coalitionSizeHeader.innerHTML += " (excluding P5)";
}

prod_fct.forEach(function (payoff, i) {
    let headerCell = document.createElement("th");
    headerCell.innerHTML = i;
    headerCell.style.textAlign = 'center';
    payoffTableHeader.appendChild(headerCell)

    let valueCell = payoffTableRow.insertCell();
    valueCell.innerHTML = payoff;
    valueCell.style.textAlign = 'center';
});

