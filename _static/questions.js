$('input').bind('keypress', function (e) {
    if (e.keyCode === 13 || e.key == 'Enter') {
        return false;
    }
});


function showAndHideField(field_to_hide, field_determining_hidden, hidden_if_value) {
    const field_determining_hidden_selector = $(`input[name="${field_determining_hidden}"]`);
    const div_to_hide_selector = $(`#id_${field_to_hide}`).parent().parent();
    div_to_hide_selector.hide();
    field_determining_hidden_selector.change(function () {
        if (field_determining_hidden_selector.filter(':checked').val() == hidden_if_value) {
            div_to_hide_selector.show();
        } else {
            div_to_hide_selector.hide();
        }
    });
}

showAndHideField('gender_other', 'gender', 'Other');
showAndHideField('degree_other', 'degree', 'Other');
showAndHideField('second_nationality', 'has_second_nationality', 'True');
