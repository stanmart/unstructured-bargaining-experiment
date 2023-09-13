let btnPropose = document.getElementById('btn-propose');
let btnAccept = document.getElementById('btn-accept');

let isMember1 = document.getElementById('is-member-1');
let isMember2 = document.getElementById('is-member-2');
let isMember3 = document.getElementById('is-member-3');
let isMember4 = document.getElementById('is-member-4');
let isMember5 = document.getElementById('is-member-5');

let allocation1 = document.getElementById('allocation-1');
let allocation2 = document.getElementById('allocation-2');
let allocation3 = document.getElementById('allocation-3');
let allocation4 = document.getElementById('allocation-4');
let allocation5 = document.getElementById('allocation-5');

let accepted1 = document.getElementById('accepted-1');
let accepted2 = document.getElementById('accepted-2');
let accepted3 = document.getElementById('accepted-3');
let accepted4 = document.getElementById('accepted-4');
let accepted5 = document.getElementById('accepted-5');

let payoff1 = document.getElementById('payoff-1');
let payoff2 = document.getElementById('payoff-2');
let payoff3 = document.getElementById('payoff-3');
let payoff4 = document.getElementById('payoff-4');
let payoff5 = document.getElementById('payoff-5');

let totalShareable = document.getElementById('total-shareable');
let totalShared = document.getElementById('total-shared');

let pastOffersTable = document.getElementById('past-offers-table');

let totalShareableValue = 0;
let pastOffers = []

isMember1.addEventListener('change', function () {
    allocation1.disabled = !isMember1.checked;
    allocation1.value = 0;
    updateTotalShareable();
    updateTotalShared();
    if (!allocation1.disabled) {
        allocation1.select()
    }
});

isMember2.addEventListener('change', function () {
    allocation2.disabled = !isMember2.checked;
    allocation2.value = 0;
    updateTotalShareable();
    updateTotalShared();
    if (!allocation2.disabled) {
        allocation2.select()
    }
});

isMember3.addEventListener('change', function () {
    allocation3.disabled = !isMember3.checked;
    allocation3.value = 0;
    updateTotalShareable();
    updateTotalShared();
    if (!allocation3.disabled) {
        allocation3.select()
    }
});

isMember4.addEventListener('change', function () {
    allocation4.disabled = !isMember4.checked;
    allocation4.value = 0;
    updateTotalShareable();
    updateTotalShared();
    if (!allocation4.disabled) {
        allocation4.select()
    }
});

isMember5.addEventListener('change', function () {
    allocation5.disabled = !isMember5.checked;
    allocation5.value = 0;
    updateTotalShareable();
    updateTotalShared();
    if (!allocation5.disabled) {
        allocation5.select()
    }
});

allocation1.addEventListener('change', function () {
    allocation1.value = Math.floor(Math.max(0, allocation1.value));
    updateTotalShared();
});
allocation1.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
        allocation1.value = Math.floor(Math.max(0, allocation1.value));
        updateTotalShared();
    }
});

allocation2.addEventListener('change', function () {
    allocation1.value = Math.floor(Math.max(0, allocation1.value));
    updateTotalShared();
});
allocation2.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
        allocation2.value = Math.floor(Math.max(0, allocation2.value));
        updateTotalShared();
    }
});

allocation3.addEventListener('change', function () {
    allocation1.value = Math.floor(Math.max(0, allocation1.value));
    updateTotalShared();
});
allocation3.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
        allocation3.value = Math.floor(Math.max(0, allocation3.value));
        updateTotalShared();
    }
});

allocation4.addEventListener('change', function () {
    allocation1.value = Math.floor(Math.max(0, allocation1.value));
    updateTotalShared();
});
allocation4.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
        allocation4.value = Math.floor(Math.max(0, allocation4.value));
        updateTotalShared();
    }
});

allocation5.addEventListener('change', function () {
    allocation1.value = Math.floor(Math.max(0, allocation1.value));
    updateTotalShared();
});
allocation5.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
        allocation5.value = Math.floor(Math.max(0, allocation5.value));
        updateTotalShared();
    }
});

function sendOffer() {
    if (totalSharedValue > totalShareableValue) {
        alert('You cannot offer more than the total shareable value');
        return;
    }
    members = [
        isMember1.checked,
        isMember2.checked,
        isMember3.checked,
        isMember4.checked,
        isMember5.checked,
    ];
    allocations = [
        allocation1.value,
        allocation2.value,
        allocation3.value,
        allocation4.value,
        allocation5.value,
    ];
    liveSend({ 'type': 'propose', 'members': members, 'allocations': allocations })
    alert('Offer submitted successfully');
}

function sendAccept() {
    liveSend({ 'type': 'accept', 'amount': otherProposal })
}

function cu(amount) {
    return `${amount} points`;
}

function liveRecv(data) {
    if ('proposals' in data) {
        for (let [id_in_group, proposal] of data.proposals) {

            if (id_in_group === js_vars.my_id) {
                msgMyProposal.innerHTML = cu(proposal)
            } else {
                msgOtherProposal.innerHTML = cu(proposal);
                otherProposal = proposal;
                btnPropose.style.display = 'block';
            }
        }
    }
    if ('finished' in data) {
        document.getElementById('form').submit();
    }
}

function updateTotalShareable() {
    if (isMember1.checked) {
        total = isMember2.checked + isMember3.checked + isMember4.checked + isMember5.checked;
        totalShareableValue = prod_fct[total];
    } else {
        totalShareableValue = 0;
    }
    totalShareable.innerHTML = totalShareableValue;
}

function updateTotalShared() {
    totalSharedValue = parseInt(allocation1.value) + parseInt(allocation2.value) + parseInt(allocation3.value) + parseInt(allocation4.value) + parseInt(allocation5.value);
    totalShared.innerHTML = totalSharedValue;
    if (totalSharedValue > totalShareableValue) {
        totalShared.style.color = 'red';
    } else if (totalSharedValue < totalShareableValue) {
        totalShared.style.color = 'black';
    } else {
        totalShared.style.color = 'green';
    }
}

function updatePastOffers(newPastOffers) {
    if (newPastOffers.length < pastOffers.length) {
        pastOffersTable.innerHTML = '';
        pastOffers = [];
    }
    if (!(JSON.stringify(newPastOffers.slice(0, pastOffers.length)) === JSON.stringify(pastOffers))) {
        pastOffersTable.innerHTML = '';
        pastOffers = [];
    }
    newPastOffers.slice(pastOffers.length).forEach(function (offer) {
        pastOffers.push(offer);
        let row = pastOffersTable.insertRow();

        let from = row.insertCell();
        from.className = "offer-left-col";
        from.innerHTML = `P${offer.from}`;
        from.style.fontWeight = 'bold';

        let id = row.insertCell();
        id.className = "offer-id-col";
        id.innerHTML = offer.offer_id;
        id.style.fontWeight = 'bold';

        for (let i = 0; i < 5; i++) {
            let cell = row.insertCell();
            cell.className = "offer-player-col";
            if (!offer.members[i]) {
                cell.innerHTML = '—';
            } else {
                cell.innerHTML = offer.allocations[i]
            }
            if (i === js_vars.my_id - 1) {
                cell.style.fontWeight = 'bold';
                cell.style.color = '#056fb7';
            }
        }

    });
}

// Setup
window.addEventListener('DOMContentLoaded', (event) => {
    liveSend({});
});
document.getElementById(`accepted-${js_vars.my_id}`).disabled = false;
let thisPlayerHeaders = document.getElementsByClassName(`player-${js_vars.my_id}`);
for (let i = 0; i < thisPlayerHeaders.length; i++) {
    thisPlayerHeaders[i].style.color = '#056fb7';
}

// Temp code for testing:

let prod_fct = [0, 50, 80, 95, 100];

let newPastOffers = [
    {
        "from": 1,
        "offer_id": 1,
        "members": [true, false, true, true, false],
        "allocations": [50, 0, 20, 10, 0],
    },
    {
        "from": 2,
        "offer_id": 2,
        "members": [true, true, true, true, true],
        "allocations": [50, 10, 20, 10, 10],
    }
];
updatePastOffers(newPastOffers);

// Payoff chart
const ctx = document.getElementById('payoff-chart');

let chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: Array.from(Array(prod_fct.length).keys()),
        datasets: [{
            label: "Coalition's payoff",
            data: prod_fct,
            borderWidth: 1,
            borderColor: "#056fb7",
            backgroundColor: "#5994c7"
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            },
            x: {
                title: {
                    text: "P1 + this many others in coalition",
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
chart.canvas.parentNode.style.height = '200px';
chart.canvas.parentNode.style.width = '400px';

// Payoff table
payoffTableRow = document.getElementById('payoff-table-values');
prod_fct.forEach(function (payoff) {
    let cell = payoffTableRow.insertCell();
    cell.innerHTML = payoff;
    cell.style.textAlign = 'center';
});
