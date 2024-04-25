let numPlayers = 3;

let player_names = js_vars.player_names;

let totalShareable = document.getElementById('total-shareable');
let totalShared = document.getElementById('total-shared');

let pastOffersTable = document.getElementById('past-offers-table');

let pastOffers = []

let popupFull = document.getElementById('popup-full');
let popupTitle = document.getElementById('popup-title');
let popupContent = document.getElementById('popup-content');

let preferredDropdwon = document.getElementById('offer-select')
let allocationDropdowns = document.getElementsByClassName('allocation-dropdown');
let offerSelect = document.getElementById('offer-select');

let tasks_coalitions = {
    "grand-coalition": false,
    "sub-coalition": false,
    "no-coalition": false,
}

tasks_coordination = {
    "send-preferred": false,
    "clear-preferred": false,
}

let canContinue = false;

exampleOffers = [
    {
        'offer_id': 1,
        'player': 1,
        'members': [true, false, true],
        'allocations': [40, 0, 10],
    },
    {
        'offer_id': 2,
        'player': 3,
        'members': [true, true, true],
        'allocations': [30, 40, 30],
    },
    {
        'offer_id': 3,
        'player': 1,
        'members': [true, true, true],
        'allocations': [80, 20, 0],
    },
    {
        'offer_id': 4,
        'player': 1,
        'members': [true, true, false],
        'allocations': [25, 15, 0],
    },
]

preferredOffers = [0, 2, 1]

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

        for (let i = 0; i < allocationDropdowns.length; i++) {
            let option = document.createElement("option");
            option.text = offer.offer_id;
            allocationDropdowns[i].add(option);
        }
        let option = document.createElement("option");
        option.text = offer.offer_id;
        offerSelect.add(option);

    });
}

function updatePayoffsCoalitions() {

    let choices = [];
    for (let i = 0; i < allocationDropdowns.length; i++) {
        value = allocationDropdowns[i].value;
        if (value !== '—') {
            choices.push(parseInt(value));
        } else {
            choices.push(0);
        }
    }

    let results = computePayoffs(choices);

    for (let i = 0; i < numPlayers; i++) {
        let cell = document.getElementById(`payoff-${i + 1}`);
        if (results.members[i] === true) {
            cell.style.color = 'green';
            cell.style.fontWeight = 'bold';
        } else {
            cell.style.color = 'black';
            cell.style.fontWeight = 'normal';
        }
        cell.innerHTML = results.payoffs[i];
    }

    let coalitionFormed;
    if (results.members[0] === true) {
        coalitionFormed = choices[0];
    } else {
        coalitionFormed = 0;
    }
    updateCoalitionTasks(choices, coalitionFormed, results.members)

}

function sendAccept() {
    if (preferredDropdwon.value !== '') {
        preferredOffers[0] = parseInt(preferredDropdwon.value);
        updatePayoffsPreferred();
        openPopup(`Proposal ${preferredDropdwon.value} marked as preferred`, 'success');

        tasks_coordination["send-preferred"] = true
        acceptTask(document.getElementById('task-submit-preferred'));
        checkCompletion()
    }
}

function sendRevert() {
    preferredOffers[0] = 0;
    updatePayoffsPreferred();
    openPopup('Preferred proposal cleared', 'success');

    tasks_coordination["clear-preferred"] = true
    acceptTask(document.getElementById('task-clear-preferred'));
    checkCompletion()
}

function updatePayoffsPreferred() {

    let results = computePayoffs(preferredOffers)

    for (let i = 0; i < numPlayers; i++) {
        let preferred = document.getElementById(`preferred-${i + 1}`);
        if (preferredOffers[i] == 0) {
            preferred.innerHTML = '—';
        } else {
            preferred.innerHTML = preferredOffers[i];
        }

        let payoff = document.getElementById(`payoff-${i + 1}-preferred`);
        if (results.members[i] === true) {
            payoff.style.color = 'green';
            payoff.style.fontWeight = 'bold';
        } else {
            payoff.style.color = 'black';
            payoff.style.fontWeight = 'normal';
        }
        payoff.innerHTML = results.payoffs[i];
    }

}

function computePayoffs(choices) {

    let P1Choice = choices[0];
    let agreement;
    if (P1Choice == 0) {
        agreement = false;
    } else {
        offer = pastOffers.find(element => element.offer_id === P1Choice);
        agreement = true;
        for (let i = 1; i < choices.length; i++) {
            if (offer.members[i] === true && choices[i] !== P1Choice) {
                agreement = false;
                break;
            }
        }
    }

    let payoffs;
    let members;
    if (agreement) {
        payoffs = offer.allocations;
        members = offer.members;
    } else {
        payoffs = Array(numPlayers).fill(0);
        members = Array(numPlayers).fill(false);
    }

    return {
        "payoffs": payoffs,
        "members": members
    }

}

function updateCoalitionTasks(choices, coalitionFormed, members) {

    let task;
    if (coalitionFormed === 0) {
        tasks_coalitions['no-coalition'] = true;
        task = document.getElementById('no-coalition');
    } else if (members.every((member) => member)) {
        tasks_coalitions['grand-coalition'] = true;
        task = document.getElementById('grand-coalition');
    } else if (coalitionFormed !== 0 && new Set(choices).size > 1) {
        tasks_coalitions['sub-coalition'] = true;
        task = document.getElementById('sub-coalition');
    } else {
        return;
    }

    acceptTask(task);
    openPopup("Task completed: " + task.innerHTML, 'success');

    checkCompletion()

}

function checkCompletion() {
    let coalitionTasksComplete = Object.values(tasks_coalitions).every(element => element);
    let coordinationTasksComplete = Object.values(tasks_coordination).every(element => element);

    if (coalitionTasksComplete === true && coordinationTasksComplete === true && canContinue === false) {
        let next_buttons = document.getElementsByClassName('otree-btn-next');
        for (let i = 0; i < next_buttons.length; i++) {
            next_buttons[i].style.visibility = '';
        }
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

    updatePastOffers(exampleOffers);
    updatePayoffsPreferred();

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