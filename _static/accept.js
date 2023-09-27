let pastOffersTable = document.getElementById('past-offers-table');

function populatePastOffers(pastOffers) {
    pastOffers.forEach(function (offer) {
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

    });
}

function populateAcceptances(acceptances, coalition_members, payoffs) {
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

populatePastOffers(js_vars.past_offers);
populateAcceptances(
    js_vars.acceptances,
    js_vars.coalition_members,
    js_vars.payoffs
)

let thisPlayerHeaders = document.getElementsByClassName(`player-${js_vars.my_id}`);
for (let i = 0; i < thisPlayerHeaders.length; i++) {
    thisPlayerHeaders[i].style.color = '#056fb7';
}
