$('input').bind('keypress', function (e) {
    if (e.keyCode === 13 || e.key == 'Enter') {
        return false;
    }
});


function showAndHideField(field_to_hide, field_determining_hidden, shown_if_value, radio=true) {
    const div_to_hide_selector = $(`#id_${field_to_hide}`).parent().parent();
    div_to_hide_selector.hide();
    if (radio) {
        const field_determining_hidden_selector = $(`input[name="${field_determining_hidden}"]`);
        field_determining_hidden_selector.change(function () {
            if ($(field_determining_hidden_selector).filter(':checked').val() == shown_if_value) {
                div_to_hide_selector.show();
            } else {
                div_to_hide_selector.hide();
                $(`[name="${field_to_hide}"]`).val('');
            }
        });
    } else {
        const field_determining_hidden_selector = $(`select[name="${field_determining_hidden}"]`);
        field_determining_hidden_selector.change(function () {
            if ($(field_determining_hidden_selector).val() == shown_if_value) {
                div_to_hide_selector.show();
            } else {
                div_to_hide_selector.hide();
                $(`[name="${field_to_hide}"]`).val('');
            }
        });
    }
}

showAndHideField('gender_other', 'gender', 'Other');
showAndHideField('degree_other', 'degree', 'Other');
showAndHideField('study_field_other', 'study_field', 'Other', false);
showAndHideField('second_nationality', 'has_second_nationality', 'True');
