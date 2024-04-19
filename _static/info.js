let numPlayers = 3;

let prod_fct = js_vars.prod_fct;
let prod_fct_labels = js_vars.prod_fct_labels;
let lastPlayerIsDummy = prod_fct.length == numPlayers - 1;

// Payoff chart
const ctx = document.getElementById('payoff-chart');

let chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: prod_fct_labels,
        datasets: [{
            label: "Group's value",
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
                    text: "Group members",
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

prod_fct.forEach(function (payoff, i) {
    let headerCell = document.createElement("th");
    headerCell.innerHTML = prod_fct_labels[i];
    headerCell.style.textAlign = 'center';
    payoffTableHeader.appendChild(headerCell)

    let valueCell = payoffTableRow.insertCell();
    valueCell.innerHTML = payoff;
    valueCell.style.textAlign = 'center';
});

