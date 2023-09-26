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

let totalShareable = document.getElementById('total-shareable');
let totalShared = document.getElementById('total-shared');

let pastOffersTable = document.getElementById('past-offers-table');

let totalShareableValue = 0;
let totalSharedValue = 0;
let pastOffers = []

let prod_fct = js_vars.prod_fct;
let P5IsDummy = prod_fct.length == 4;

let popupFull = document.getElementById('popup-full');
let popupTitle = document.getElementById('popup-title');
let popupContent = document.getElementById('popup-content');

let tasks ={
    "grand-coalition": false,
    "sub-coalition": false,
    "efficient": false,
    "inefficient": false,
}

closePopup = function () {
    popupFull.classList.remove('show');
}

openPopup = function (content, type) {
    // popupFull.style.visibility = "visible";
    popupContent.innerHTML = content;
    if (type === 'error') {
        popupFull.classList = 'error';
        popupTitle.innerHTML = 'Error';
    } else {
        popupFull.classList = 'success';
        popupTitle.innerHTML = 'Success';
    }
   popupFull.classList.add('show');
}

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
    let newPastOffers = pastOffers.slice();

    let members = [
        isMember1.checked,
        isMember2.checked,
        isMember3.checked,
        isMember4.checked,
        isMember5.checked,
    ];
    let allocations = [
        allocation1.value,
        allocation2.value,
        allocation3.value,
        allocation4.value,
        allocation5.value,
    ];
    let newOffer = {
        'offer_id': newPastOffers.length + 1,
        'player': js_vars.my_id,
        'members': members,
        'allocations': allocations,
    };

    if (totalSharedValue > 0 && !isMember1.checked) {
        openPopup('Invalid allocation: allocation has to be zero when Player 1 is not included', 'error');
        return;
    }
    if (totalSharedValue > totalShareableValue) {
        openPopup('Invalid allocation: allocations exceed value available to this coalition', 'error');
        return;
    }

    newPastOffers.push(newOffer);
    updatePastOffers(newPastOffers);
    openPopup('Offer submitted successfully', 'success');
    updateTasks(newOffer);
}

function updateTotalShareable() {
    if (isMember1.checked) {
        let numMembers = isMember2.checked + isMember3.checked + isMember4.checked;
        if (!P5IsDummy) {
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
    let numOldOffers = pastOffers.length;

    if (newPastOffers.length < numOldOffers ||
        !(JSON.stringify(newPastOffers.slice(0, numOldOffers)) === JSON.stringify(pastOffers))) {
        pastOffersTable.innerHTML = '';
        pastOffers = [];
        numOldOffers = 0;
    }

    pastOffers = newPastOffers

    newPastOffers.slice(numOldOffers).forEach(function (offer) {
        let row = pastOffersTable.insertRow();

        let id = row.insertCell();
        id.className = "offer-id-col";
        id.innerHTML = offer.offer_id;

        let from = row.insertCell();
        from.className = "offer-proposer-col";
        from.innerHTML = `P${offer.player}`;

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

        row.classList.add("highlight");
        let timeout = setTimeout(
            function () {
                row.classList.remove("highlight");
            },
            5000
        )

    });
}

function updateTasks(newOffer) {



    if (newOffer.members.every((member) => member)) {
        tasks["grand-coalition"] = true;
        document.getElementById('proposal-grand-coalition').style.color = 'green';
    }

    if (!(newOffer.members.every((member) => member))) {
        tasks["sub-coalition"] = true;
        document.getElementById('proposal-sub-coalition').style.color = 'green';
    }

    if (totalShareableValue == totalSharedValue) {
        tasks["efficient"] = true;
        document.getElementById('proposal-efficient').style.color = 'green';
    }

    if (totalShareableValue > totalSharedValue) {
        tasks["inefficient"] = true;
        document.getElementById('proposal-inefficient').style.color = 'green';
    }


    if (Object.values(tasks).every(element => element)) {
        let next_buttons = document.getElementsByClassName('otree-btn-next');
        for (let i = 0; i < next_buttons.length; i++) {
            next_buttons[i].style.visibility = '';
        }
        openPopup('You have completed all tasks. Please click "Next" to continue.', 'success');
    }
}

document.addEventListener("DOMContentLoaded", function() {
    // Setup
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
                        text: "P1 + this many others in group" + (P5IsDummy ? " (excluding P5)" : ""),
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

    let next_buttons = document.getElementsByClassName('otree-btn-next');
    for (let i = 0; i < next_buttons.length; i++) {
        next_buttons[i].style.visibility = 'hidden';
    }
})