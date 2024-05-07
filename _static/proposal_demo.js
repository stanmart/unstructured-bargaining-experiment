let numPlayers = 3;

let isMemberCheckboxes = Array.from(Array(numPlayers).keys()).map(
    i => document.getElementById(`is-member-${i + 1}`)
);
let allocationTextBoxes = Array.from(Array(numPlayers).keys()).map(
    i => document.getElementById(`allocation-${i + 1}`)
);

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

let tasks = {
    "grand-coalition": false,
    "sub-coalition": false,
    "efficient": false,
    "inefficient": false,
}

let canContinue = false;

closePopup = function () {
    popupFull.classList.remove('show');
}

openPopup = function (content, type) {
    // popupFull.style.visibility = "visible";
    if (popupFull.classList.contains('show')) {
        new_content = popupContent.innerHTML + `<p>${content}</p>`;
    } else {
        new_content = `<p>${content}</p>`;
    }
    popupContent.innerHTML = new_content;
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
            allocationTextBoxes[i].value = '';
        }
        updateTotalShareable();
        updateTotalShared();
        if (!allocationTextBoxes[i].disabled) {
            allocationTextBoxes[i].select()
        }
    });

    allocationTextBoxes[i].addEventListener('change', function () {
        allocationTextBoxes[i].value = Math.floor(Math.max(0, allocationTextBoxes[i].value));
        updateTotalShared();
    });
    allocationTextBoxes[i].addEventListener("keyup", function (event) {
        if (event.key === "Enter") {
            allocationTextBoxes[i].value = Math.floor(Math.max(0, allocationTextBoxes[i].value));
            updateTotalShared();
        }
    });
}

function sendOffer() {
    let newPastOffers = pastOffers.slice();

    let members = isMemberCheckboxes.map((checkbox) => checkbox.checked);
    let allocations = allocationTextBoxes.map((textbox) => parseInt(textbox.value));
    let newOffer = {
        'offer_id': newPastOffers.length + 1,
        'player': js_vars.my_id,
        'members': members,
        'allocations': allocations,
    };

    if (!lastPlayerIsDummy && totalSharedValue > 0 && !isMemberCheckboxes[0].checked) {
        openPopup(`Invalid proposal: the group budget is zero when Player ${player_names['P1']} is not included`, 'error');
        return;
    }
    if (lastPlayerIsDummy && totalSharedValue > 0 && !(isMemberCheckboxes[0].checked && isMemberCheckboxes[1].checked)) {
        openPopup(`Invalid proposal: the group budget is zero when Players ${player_names['P1']} and ${player_names['P2']} are not included`, 'error');
        return;
    }
    if (totalSharedValue > totalShareableValue) {
        openPopup('Invalid proposal: total amount exceeds the budget available to this group', 'error');
        return;
    }
    for (let i = 0; i < numPlayers; i++) {
        if (isMemberCheckboxes[i].checked && allocationTextBoxes[i].value === '') {
            openPopup('Invalid proposal: please choose an amount for each group member', 'error');
            return;
        }
    }
    for (let i = 0; i < numPlayers; i++) {
        if (isMemberCheckboxes[i].checked && allocationTextBoxes[i].value === '0') {
            openPopup('Invalid proposal: all group members must receive a positive amount', 'error');
            return;
        }
    }

    newPastOffers.push(newOffer);
    updatePastOffers(newPastOffers);
    openPopup('Proposal submitted successfully', 'success');
    updateTasks(newOffer);
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
    totalSharedValue = allocationTextBoxes.reduce(
        (acc, curr) => acc + (curr.disabled || curr.value == '' ? 0 : parseInt(curr.value)), 0
    );
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

function updateTasks(newOffer) {

    let completedTasks = [];

    if (newOffer.members.every((member) => member)) {
        tasks["grand-coalition"] = true;
        completedTasks.push(document.getElementById('proposal-grand-coalition'));
    }

    if (!(newOffer.members.every((member) => member))) {
        tasks["sub-coalition"] = true;
        completedTasks.push(document.getElementById('proposal-sub-coalition'));
    }

    if (totalShareableValue == totalSharedValue) {
        tasks["efficient"] = true;
        completedTasks.push(document.getElementById('proposal-efficient'));
    }

    if (totalShareableValue > totalSharedValue) {
        tasks["inefficient"] = true;
        completedTasks.push(document.getElementById('proposal-inefficient'));
    }

    completedTasks.forEach((element) => acceptTask(element));
    let taskList = completedTasks.map((element) => `<li>${element.innerHTML}</li>`).join('');
    openPopup(`This proposal satisfies the following tasks:<br><ul>${taskList}</ul>`, 'success');


    if (Object.values(tasks).every(element => element) && !canContinue) {
        let next_buttons = document.getElementsByClassName('otree-btn-next');
        for (let i = 0; i < next_buttons.length; i++) {
            next_buttons[i].style.visibility = '';
            next_buttons[i].disabled = false;
        }
        document.getElementById('exercises-remaining-text').style.visibility = 'hidden';
        canContinue = true;
        openPopup('You have completed all tasks. Feel free to experiment some more with these interactive controls if you\'d like. When you are done, click "Next" to continue.', 'success');
    }
}

function acceptTask(element) {
    element.style.color = 'green';
    checkmarks = element.getElementsByClassName('checkmark');
    for (let i = 0; i < checkmarks.length; i++) {
        checkmarks[i].style.visibility = '';
    }
}

document.addEventListener("DOMContentLoaded", function () {
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

    let next_buttons = document.getElementsByClassName('otree-btn-next');
    for (let i = 0; i < next_buttons.length; i++) {
        next_buttons[i].style.visibility = 'hidden';
    }

    $('html').bind('keypress', function (e) {
        if (e.keyCode === 13 || e.key == 'Enter') {
            return false;
        }
    });

})