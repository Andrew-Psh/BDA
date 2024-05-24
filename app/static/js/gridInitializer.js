// import { ruRU } from "gridjs/l10n";
// import { Grid, html } from "gridjs";
const Grid = window.gridjs.Grid;
const html = window.gridjs.html;

const queryFilterString = document.getElementById('table').getAttribute('query-filter');
const queryFilterObject = JSON.parse(queryFilterString);
const tableLabel = queryFilterObject.table_label;
const modelName = queryFilterObject.model_name;

console.log(queryFilterObject.column); // Вывод значения свойства "column"
console.log(queryFilterObject.value); // Вывод значения свойства "value"


console.log('typeof queryFilterObject:', typeof queryFilterObject);
console.log('Контрольная точка: Получение значения queryFilterObject:', queryFilterObject);

// console.log('Контрольная точка: Получение значения tableName:', tableName);
// console.log('Название таблицы:', tableLabel);

// Функция для обновления URL с параметрами запроса
const updateUrl = (prev, query) => {
    return (
        prev +
        (prev.indexOf("?") >= 0 ? "&" : "?") +
        new URLSearchParams(query).toString()
    );
};
 
var columns;
fetch(`/api/data`, {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json',
    },
    body: JSON.stringify(queryFilterObject),
    })
    .then(response => response.json())
    .then(data => {
        columns = data.columns;
        const columnList = columns.map(column => column.id);

        // Логирование названий и назначений полей
        console.log('Названия и назначения полей:');
        columns.forEach(column => {
            console.log(`Название: ${column.name}, Назначение: ${column.header}`);
        });

        const tableTitle = document.createElement('div');
        tableTitle.textContent = tableLabel;
        tableTitle.className = 'table-title';
        document.getElementById('table').insertAdjacentElement('beforebegin', tableTitle);

        data.data.forEach(row => {
            console.log(row);
        });
        

        // Функция для форматирования даты и времени
        function formatDateTime(date) {
            return date.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' }) + '   ' + date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
        };

        function convertBooleanFields(isChecked) {
            console.log('Тип переменной item:', typeof isChecked);
            console.log('Значение item:', isChecked);
            const formattedValue = isChecked ? '<span class="icon-checkmark">✔️</span>' : '<span class="icon-checkmark">❌</span>';

            // Применение форматирования HTML внутри функции
            return html(formattedValue);
        }

        // Список полей для форматирования дат
        const dateFields = ['d_edit', 'd_prod','timestamp'];

        // Список полей boolean для форматирования      
        const booleanFields = ['is_admin', 'is_active', 'new_password'];

        new gridjs.Grid({
            columns: columns,
            server: {
                url: '/api/data',
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify(queryFilterObject),
                
                then: (results) => {
                    results.data.forEach(row => {
                        // Форматирование даты
                        dateFields.forEach(field => {
                            if (row[field]) {
                                row[field] = formatDateTime(new Date(row[field]));
                            }
                        });

                        // // Форматирование булевых значений True и False
                        // booleanFields.forEach(field => {
                        //         row[field] = convertBooleanFields(row[field]);   
                        // });

                        // Форматирование только булевого  значения True
                        booleanFields.forEach(field => {
                            if (row[field]) {
                                row[field] = convertBooleanFields(row[field]); 
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
