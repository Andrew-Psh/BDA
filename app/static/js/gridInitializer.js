// import { ruRU } from "gridjs/l10n";



// Получение значения table_key с контрольной точкой
const tableName = document.getElementById('table').getAttribute('table-name');
const tableKey = document.getElementById('table').getAttribute('table-key');
console.log('Контрольная точка: Получение значения tableKey:', tableKey);
console.log('Название таблицы:', tableName);

// Функция для обновления URL с параметрами запроса
const updateUrl = (prev, query) => {
    return (
        prev +
        (prev.indexOf("?") >= 0 ? "&" : "?") +
        new URLSearchParams(query).toString()
    );
};

var columns;
fetch(`/api/data?table_key=${tableKey}`)
    .then(response => response.json())
    .then(data => {
        columns = data.columns;
        const columnList = columns.map(column => column.id);

        const tableTitle = document.createElement('div');
        tableTitle.textContent = tableName;
        tableTitle.className = 'table-title';
        document.getElementById('table').insertAdjacentElement('beforebegin', tableTitle);

        data.data.forEach(row => {
            console.log(row);
        });

        // Функция для форматирования даты и времени
        function formatDateTime(date) {
            return date.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' }) + '   ' + date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
        }

        // Список полей для форматирования дат
        const dateFields = ['d_edit', 'd_prod'];

        new gridjs.Grid({
            columns: columns,
            server: {
                url: `/api/data?table_key=${tableKey}`,
                then: (results) => {
                    results.data.forEach(row => {
                        dateFields.forEach(field => {
                            if (row[field]) {
                                row[field] = formatDateTime(new Date(row[field]));
                            }
                        });
                    });
                    return results.data;
                },
                total: (results) => {
                    return results.total;
                },
            },
            search: {
                enabled: true,
                data: data.date,
            },
            sort: {
                enabled: true,
                multiColumn: true,
                data: data.date,
            },
            pagination: {
                server: {
                    url: (prev, page, limit) => {
                        return updateUrl(prev, { start: page * limit, length: limit });
                    },
                },
            },
            language: {
                'search': {
                    'placeholder': '🔍 Поиск...'
                },
                'pagination': {
                    'previous': '⬅️',
                    'next': '➡️',
                    'results': () => 'Записи'
                }
            },
            fixedHeader: true,
            resizable: true,
        }).render(document.getElementById("table"));
    })
    .catch(error => console.error('Ошибка при загрузке данных:', error));
