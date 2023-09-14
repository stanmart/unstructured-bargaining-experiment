
function populateAcceptances(acceptances, coalition_members, payoffs) {
    for (let i = 0; i < 5; i++) {
        let thisAccepted = document.getElementById(`accepted-${i + 1}`);
        let thisPayoff = document.getElementById(`payoff-${i + 1}`);
        if (acceptances[i] === 0) {
            thisAccepted.value = '';
        } else {
            thisAccepted.value = acceptances[i];
        }
        if (coalition_members[i]) {
            thisPayoff.innerHTML = payoffs[i];
            thisPayoff.style.color = 'green';
            thisPayoff.style.fontWeight = 'bold';
        } else {
            thisPayoff.innerHTML = '—';
            thisPayoff.style.color = 'black';
            thisPayoff.style.fontWeight = 'normal';
        }
    } 
}

populateAcceptances(
    js_vars.acceptances,
    js_vars.coalition_members,
    js_vars.payoffs
)