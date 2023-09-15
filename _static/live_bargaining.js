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

let acceptDropdown = document.getElementById('offer-select');

let totalShareable = document.getElementById('total-shareable');
let totalShared = document.getElementById('total-shared');

let pastOffersTable = document.getElementById('past-offers-table');

let totalShareableValue = 0;
let totalSharedValue = 0;
let pastOffers = []

let prod_fct = js_vars.prod_fct;
let P5IsDummy = prod_fct.length == 4;

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
    allocation2.value = Math.floor(Math.max(0, allocation2.value));
    updateTotalShared();
});
allocation2.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
        allocation2.value = Math.floor(Math.max(0, allocation2.value));
        updateTotalShared();
    }
});

allocation3.addEventListener('change', function () {
    allocation3.value = Math.floor(Math.max(0, allocation3.value));
    updateTotalShared();
});
allocation3.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
        allocation3.value = Math.floor(Math.max(0, allocation3.value));
        updateTotalShared();
    }
});

allocation4.addEventListener('change', function () {
    allocation4.value = Math.floor(Math.max(0, allocation4.value));
    updateTotalShared();
});
allocation4.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
        allocation4.value = Math.floor(Math.max(0, allocation4.value));
        updateTotalShared();
    }
});

allocation5.addEventListener('change', function () {
    allocation5.value = Math.floor(Math.max(0, allocation5.value));
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

    if (acceptDropdown.value === '') {
        alert('You must select an offer to accept');
        return;
    }
    
    acceptedOffer = parseInt(acceptDropdown.value);
    liveSend({ 'type': 'accept', 'offer_id': acceptedOffer })
    alert(`Offer ${acceptDropdown.value} marked as preferred`);
    return;

}

function sendRevert() {

    liveSend({ 'type': 'accept', 'offer_id': 0 })
    alert(`Preferred offer cleared`);

}

function liveRecv(data) {

    if (data['type'] === 'error') {
        alert(data['content']);
        return;
    }

    if (data['type'] === 'proposals_history') {
        updatePastOffers(data['proposals_history']);
        return;
    }

    if (data['type'] === 'acceptances') {
        updateAcceptances(data['acceptances'], data['coalition_members'], data['payoffs']);
        return;
    }

    if (data['type'] === 'reload') {
        updatePastOffers(data['proposals_history']);
        updateAcceptances(data['acceptances'], data['coalition_members'], data['payoffs']);
    }

}

function updateTotalShareable() {
    if (isMember1.checked) {
        let numMembers = isMember2.checked + isMember3.checked + isMember4.checked;
        if (P5IsDummy) {
            numMembers += isMember5.checked;
        }
        totalShareableValue = prod_fct[numMembers];
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
    } else {
        totalShared.style.color = 'black';
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
    pastOffers = newPastOffers
    pastOffersTable.innerHTML = '';
    acceptDropdown.innerHTML = '';

    default_option = document.createElement("option");
    default_option.text = '';
    default_option.disabled = true;
    default_option.selected = true;
    acceptDropdown.add(default_option);

    newPastOffers.forEach(function (offer) {
        let option = document.createElement("option");
        option.text = offer.offer_id;
        acceptDropdown.add(option);

        let row = pastOffersTable.insertRow();

        let from = row.insertCell();
        from.className = "offer-left-col";
        from.innerHTML = `P${offer.player}`;
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

function updateAcceptances(acceptances, coalition_members, payoffs) {
    for (let i = 0; i < 5; i++) {
        let thisAccepted = document.getElementById(`accepted-${i + 1}`);
        let thisPayoff = document.getElementById(`payoff-${i + 1}`);

        if (acceptances[i] === 0) {
            thisAccepted.innerHTML = '—';
        } else {
            thisAccepted.innerHTML = acceptances[i];
        }
        thisPayoff.innerHTML = payoffs[i];
        if (coalition_members[i]) {
            thisPayoff.style.color = 'green';
            thisPayoff.style.fontWeight = 'bold';
            thisAccepted.style.color = 'green';
            thisAccepted.style.fontWeight = 'bold';
        } else {
            thisPayoff.style.color = 'black';
            thisPayoff.style.fontWeight = 'normal';
            thisAccepted.style.color = 'black';
            thisAccepted.style.fontWeight = 'normal';
        }
    } 
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
                    text: "P1 + this many others in coalition" + (P5IsDummy ? " (excluding P5)" : ""),
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

// Instructions for the dummy case

if (P5IsDummy) {
    dummyInstructions = document.getElementsByClassName('dummy-instruction');
    for (dummyInstruction of dummyInstructions) {
        dummyInstruction.style.removeProperty('display');
    };
}
