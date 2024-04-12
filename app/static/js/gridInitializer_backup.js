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

// Запрос данных о столбцах с контрольной точкой
// var columnList;
var columns;
fetch(`/api/data?table_key=${tableKey}`)
    .then(response => response.json())
    .then(data => {
        columns = data.columns;
        // var columns = [{hidden: false, id: "id", name: "id"}, {id: "city", name: "Город"}, {id: "comment", name: "Комментарии", sort: false}];
        const columnList = columns.map(column => column.id);
        console.log('Контрольная точка: columnList:', columnList);
        // Форматирование даты и времени в столбцах данных
        data.data.forEach(row => {
            if (row.d_edit) {
                let dateEdit = new Date(row.d_edit);
                row.d_edit = dateEdit.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' }) + ', ' + dateEdit.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
            }
            if (row.d_prod) {
                let dateProd = new Date(row.d_prod);
                row.d_prod = dateProd.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' }) + ', ' + dateProd.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
            }
        });


        // Установка названия таблицы из атрибута
        const tableTitle = document.createElement('div');
        tableTitle.textContent = tableName;
        tableTitle.className = 'table-title';
        // tableTitle.style.textAlign = 'right';
        document.getElementById('table').insertAdjacentElement('beforebegin', tableTitle);
        console.log('Контрольная точка: Загрузка данных columns:', columns);

        
        // Вывод преобразованных данных
        console.log('data.data:', data.data);
        data.data.forEach(row => {
            console.log(row);
        });
                
        
        
        new gridjs.Grid({
            // localized: ruRU, 
            columns: columns,
            data: data.data, // Передача отформатированных данных
            server: {
                url: `/api/data?table_key=${tableKey}`,
                then: (results) => {
                    console.log('Контрольная точка: Получение данных с сервера:', results);
                    return results.data;
                },
                total: (results) => {
                    console.log('Контрольная точка: Общее количество элементов:', results.total);
                    return results.total;
                },
            },
            search: {
                enabled: true,
                server: {
                    url: (prev, search) => {
                        return updateUrl(prev, { search });
                    },
                },
            },

            sort: {
                enabled: true,
                multiColumn: true,
                
                server: {
                    url: (prev, columns) => {
                        console.log("Prev before function:", prev);
                        console.log("Columns before function:", columns);

                        const columnIds = columnList;
                        console.log('Значения columnIds:', columnIds); // Вывод array в консоль с помощью console.log


                        const sort = columns.map(col => (col.direction === 1 ? "+" : "-") + columnIds[col.index]);
                        const result = updateUrl(prev, {sort});
                        console.log("Prev after function:", prev);
                        console.log("Columns after function:", columns);
                        console.log("Result after updateUrl:", result);
   

                        return result;

                        
                    },
                },
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
                  'placeholder': '🔍 Search...'
                },
                'pagination': {
                  'previous': '⬅️',
                  'next': '➡️',
                //   'showing': '😃 Displaying',
                  'results': () => 'Records'
                }
              },



            fixedHeader: true,
            resizable: true,
        }).render(document.getElementById("table"));
    })
    .catch(error => console.error('Ошибка при загрузке данных:', error));
