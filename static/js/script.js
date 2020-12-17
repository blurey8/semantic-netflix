$(document).ready(function () {
    var table = $('#myTable').DataTable({
        "columnDefs": [
            { "searchable": false, "targets": 0 },
            { "searchable": false, "targets": 5 },
            { "orderable": false, "targets": 5 },
            { "name": "title", "targets": 1 },
            { "name": "category", "targets": 2 },
            { "name": "year", "targets": 3 },
            { "name": "director", "targets": 4 },
        ],
        initComplete: function () {
            // Apply the search
            columnNames = ["title", "category", "year", "director"];

            columnNames.forEach(function (name, key, columnNames) {
                console.log(name);
                $('#' + name + '-search').on('keyup change clear', function () {
                    var that = table.column(name + ":name");
                    if (that.search() !== this.value) {
                        that.search(this.value).draw();
                    }
                });
            });
        }
    });
});