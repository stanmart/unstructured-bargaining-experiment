let numPlayers = 3;

let isMemberCheckboxes = Array.from(Array(numPlayers).keys()).map(
    i => document.getElementById(`is-member-${i + 1}`)
);
let allocationTextBoxes = Array.from(Array(numPlayers).keys()).map(
    i => document.getElementById(`allocation-${i + 1}`)
);

let acceptDropdown = document.getElementById('offer-select');

let totalShareable = document.getElementById('total-shareable');
let totalShared = document.getElementById('total-shared');

let pastOffersTable = document.getElementById('past-offers-table');

let totalShareableValue = 0;
let totalSharedValue = 0;
let pastOffers = []

let prod_fct = js_vars.prod_fct;
let prod_fct_labels = js_vars.prod_fct_labels;
let lastPlayerIsDummy = prod_fct.length == numPlayers - 1;
let player_names = js_vars.player_names;

let popupFull = document.getElementById('popup-full');
let popupTitle = document.getElementById('popup-title');
let popupContent = document.getElementById('popup-content');

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

for (let i = 0; i < numPlayers; i++) {
    isMemberCheckboxes[i].addEventListener('change', function () {
        allocationTextBoxes[i].disabled = !isMemberCheckboxes[i].checked;
        if (!isMemberCheckboxes[i].checked) {
            allocationTextBoxes[i].value = 0;
        } else {
            allocationTextBoxes[i].value = 1;
        }
        updateTotalShareable();
        updateTotalShared();
        if (!allocationTextBoxes[i].disabled) {
            allocationTextBoxes[i].select()
        }
    });

    allocationTextBoxes[i].addEventListener('change', function () {
        allocationTextBoxes[i].value = Math.floor(Math.max(1, allocationTextBoxes[i].value));
        updateTotalShared();
    });
    allocationTextBoxes[i].addEventListener("keyup", function (event) {
        if (event.key === "Enter") {
            allocationTextBoxes[i].value = Math.floor(Math.max(1, allocationTextBoxes[i].value));
            updateTotalShared();
        }
    });
}

function sendOffer() {
    if (!lastPlayerIsDummy && totalSharedValue > 0 && !isMemberCheckboxes[0].checked) {
        openPopup(`Invalid proposal: the budget is zero when Player ${player_names['P1']} is not included in the group`, 'error');
        return;
    }
    if (lastPlayerIsDummy && totalSharedValue > 0 && !(isMemberCheckboxes[0].checked && isMemberCheckboxes[1].checked)) {
        openPopup(`Invalid proposal: the budget is zero when Players ${player_names['P1']} and ${player_names['P2']} are not included in the group`, 'error');
        return;
    }
    if (totalSharedValue > totalShareableValue) {
        openPopup('Invalid proposal: total amount exceeds the budget available to this group', 'error');
        return;
    }
    for (let i = 0; i < numPlayers; i++) {
        if (isMemberCheckboxes[i].checked && allocationTextBoxes[i].value === '0') {
            openPopup('Invalid proposal: all group members must receive a positive amount', 'error');
            return;
        }
    }
    members = isMemberCheckboxes.map(member => member.checked);
    allocations = allocationTextBoxes.map(alloc => alloc.value);
    liveSend({ 'type': 'propose', 'members': members, 'allocations': allocations })
    openPopup('Proposal submitted successfully', 'success');
}

function sendAccept() {

    if (acceptDropdown.value === '') {
        openPopup('You must select a proposal to accept', 'error');
        return;
    }

    acceptedOffer = parseInt(acceptDropdown.value);
    liveSend({ 'type': 'accept', 'offer_id': acceptedOffer })
    openPopup(`Offer ${acceptDropdown.value} marked as preferred`, 'success');
    return;

}

function sendRevert() {

    liveSend({ 'type': 'accept', 'offer_id': 0 })
    openPopup('Preferred proposal cleared', 'success');

}

function liveRecv(data) {

    if (data['type'] === 'error') {
        openPopup(data['content'], 'error');
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
    if (isMemberCheckboxes[0].checked) {
        let numMembers = isMemberCheckboxes.slice(1, isMemberCheckboxes.length - 1).reduce(
            (acc, curr) => acc + curr.checked, 0
        );
        if (!lastPlayerIsDummy) {
            numMembers += isMemberCheckboxes[isMemberCheckboxes.length - 1].checked;
        }
        totalShareableValue = prod_fct[numMembers];
    } else {
        totalShareableValue = 0;
    }
    totalShareable.innerHTML = totalShareableValue;
}

function updateTotalShared() {
    totalSharedValue = allocationTextBoxes.reduce((acc, curr) => acc + (curr.disabled ? 0 : parseInt(curr.value)), 0);
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
        acceptDropdown.innerHTML = '';
        pastOffers = [];

        default_option = document.createElement("option");
        default_option.text = '';
        default_option.disabled = true;
        default_option.selected = true;
        acceptDropdown.add(default_option);

        numOldOffers = 0;
    }

    pastOffers = newPastOffers

    newPastOffers.slice(numOldOffers).forEach(function (offer) {
        let option = document.createElement("option");
        option.text = offer.offer_id;
        acceptDropdown.add(option);

        let row = pastOffersTable.insertRow();

        let id = row.insertCell();
        id.className = "offer-id-col";
        id.innerHTML = offer.offer_id;

        let from = row.insertCell();
        from.className = "offer-proposer-col";
        from.innerHTML = player_names[`P${offer.player}`];

        for (let i = 0; i < numPlayers; i++) {
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

function updateAcceptances(acceptances, coalition_members, payoffs) {
    for (let i = 0; i < numPlayers; i++) {
        let thisAccepted = document.getElementById(`accepted-${i + 1}`);
        let thisPayoff = document.getElementById(`payoff-${i + 1}`);

        let oldThisAccepted = thisAccepted.innerHTML;
        let oldThisPayoff = thisPayoff.innerHTML;

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

        if (oldThisAccepted !== thisAccepted.innerHTML) {
            thisAccepted.classList.add("highlight");
            let timeout = setTimeout(
                function () {
                    thisAccepted.classList.remove("highlight");
                },
                5000
            )
        }

        if (oldThisPayoff !== thisPayoff.innerHTML) {
            thisPayoff.classList.add("highlight");
            let timeout = setTimeout(
                function () {
                    thisPayoff.classList.remove("highlight");
                },
                5000
            )
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

// Timer

let timer = document.getElementsByClassName('otree-timer')[0];
timer.getElementsByTagName('p')[0].innerHTML += ' — decisions become final after time expires';
document.addEventListener("DOMContentLoaded", function (event) {
    $('.otree-timer__time-left').on('update.countdown', function (event) {
        if (event.offset.totalSeconds <= 30) {
            timer.style.backgroundColor = '#b70505';
            timer.style.color = 'white';
        }
    });
});

// Payoff chart
const ctx = document.getElementById('payoff-chart');

let chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: prod_fct_labels.map(s => s.split('<br>')),
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

$('html').bind('keypress', function (e) {
    if (e.keyCode === 13 || e.key == 'Enter') {
        return false;
    }
});
