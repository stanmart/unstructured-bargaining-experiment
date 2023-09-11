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

let totalShareable = document.getElementById('total-shareable');
let totalShared = document.getElementById('total-shared');

let totalShareableValue = 0;

let pieByEntrants = {
    0: 0,
    1: 60,
    2: 80,
    3: 95,
    4: 100,
};

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
allocation1.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        allocation1.value = Math.floor(Math.max(0, allocation1.value));
        updateTotalShared();
    }
});

allocation2.addEventListener('change', function () {
    allocation1.value = Math.floor(Math.max(0, allocation1.value));
    updateTotalShared();
});
allocation2.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        allocation2.value = Math.floor(Math.max(0, allocation2.value));
        updateTotalShared();
    }
});

allocation3.addEventListener('change', function () {
    allocation1.value = Math.floor(Math.max(0, allocation1.value));
    updateTotalShared();
});
allocation3.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        allocation3.value = Math.floor(Math.max(0, allocation3.value));
        updateTotalShared();
    }
});

allocation4.addEventListener('change', function () {
    allocation1.value = Math.floor(Math.max(0, allocation1.value));
    updateTotalShared();
});
allocation4.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        allocation4.value = Math.floor(Math.max(0, allocation4.value));
        updateTotalShared();
    }
});

allocation5.addEventListener('change', function () {
    allocation1.value = Math.floor(Math.max(0, allocation1.value));
    updateTotalShared();
});
allocation5.addEventListener("keyup", function(event) {
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
    liveSend({'type': 'propose', 'members': members, 'allocations': allocations})
    my_offer.value = '';
}

function sendAccept() {
    liveSend({'type': 'accept', 'amount': otherProposal})
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
                btnAccept.style.display = 'block';
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
        totalShareableValue = pieByEntrants[total];
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

window.addEventListener('DOMContentLoaded', (event) => {
    liveSend({});
});
