document.addEventListener("DOMContentLoaded", function () {

    function updateChained(selectSelector, targetSelector, childModel, parentField) {
        const select = $(selectSelector); // jQuery needed for select2
        const target = $(targetSelector);

        if (!select.length || !target.length) return;

        select.on('change', function () {
            const parent_ids = $(this).val(); // array of selected values
            target.empty();  // clear previous options

            if (!parent_ids || parent_ids.length === 0) return;

            parent_ids.forEach(parent_id => {
                $.ajax({
                    url: `/api/chained-options/`,
                    data: {
                        child_model: childModel,
                        parent_field: parentField,
                        parent_id: parent_id
                    },
                    success: function(data) {
                        data.forEach(item => {
                            target.append(new Option(item.name, item.id));
                        });
                        target.trigger('change'); // notify select2 of update
                    }
                });
            });
        });
    }

    // Chained fields
    updateChained("#id_states", "#id_districts", "master.District", "state");
    updateChained("#id_districts", "#id_offices", "master.Office", "district");
});
