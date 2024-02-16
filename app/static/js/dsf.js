/**
 * Файл: dsf.js
 * Автор: Андрей Пшеничный
 * Дата создания: 13 февраля 2024 г.
 * 
 * Описание: Данный файл содержит обработчики событий и функции для управления интерактивными 
 *           элементами формы. Он используется для поддержки динамической обработки пользовательского 
 *           ввода и отображения значений выбора.
 * 
 * Глобальные объекты:
 *  - document: Объект, представляющий веб-страницу
 *  - fetch: Функция для отправки сетевых запросов
 */

// Обработчик события "DOMContentLoaded" для инциализации скрипта после загрузки документа
document.addEventListener('DOMContentLoaded', function() {
    // Получение формы по идентификатору 'formDinamic'
    var form = document.getElementById('formDinamic');
    
    // Проверка наличия формы на странице
    if (form) {
        // Назначение обработчика для события "input" на форму
        form.addEventListener('input', function(event) {
            // Проверка, что событие произошло на элементе с классом 'form-input'
            if (event.target.classList.contains('form-input')) {
                var inputField = event.target; // Получение поля ввода
                inputField.setAttribute('autocomplete', 'off'); // Отключение автозаполнения поля
                var tableName = inputField.parentElement.getAttribute('data-table-name'); // Получение имени таблицы из родительского элемента поля ввода
                var selectField = event.target.parentElement.querySelector('.form-select'); // Получение соседнего поля выбора, если оно присутствует
                
                // Отображение поля выбора, если оно было найдено
                if (selectField) {
                    selectField.style.display = 'block';
                } else {
                    console.log('Соседнее поле выбора не найдено');
                }

                // Выполнение запроса на сервер для получения значений выбора и их присвоение
                fetchDataFromServerAndAssign(inputField, selectField, tableName);
            }
        });
    }
});

/**
 * Функция для выполнения запроса на сервер и присвоения значений выбора.
 * @param {HTMLElement} inputField - Поле ввода
 * @param {HTMLElement} selectField - Поле выбора
 * @param {string} tableName - Название таблицы для запроса на сервер
 */
function fetchDataFromServerAndAssign(inputField, selectField, tableName) {
    var currentChoices = []; // Создаем пустой массив для текущих выбранных значений
    
    fetch(`/get_choices?table_name=${tableName}`) // Запрашиваем список значений на сервере
        .then(function(response) {
        if (!response.ok) { 
            throw new Error('Ошибка: ' + response.status);
        }  
        return response.json(); // Преобразуем ответ в JSON
        })
        .then(function(data) {
            var choices = data; // Получаем список значений
            // console.log('get_choices => ' + data);
            var value = inputField.value.toLowerCase(); // Получаем значение поля ввода и приводим его к нижнему регистру
            
            choices.forEach(function(choice) {
            if (choice.toLowerCase().includes(value)) { // Если текущее значение включает в себя введенное значение
                var option = document.createElement('option'); // Создаем новый элемент option
                option.value = choice; // Устанавливаем значение элемента option равным текущему значению
                option.text = choice; // Устанавливаем текст элемента option равным текущему значению
                selectField.appendChild(option); // Добавляем элемент option в список выбора значений
                currentChoices.push(choice); // Добавляем текущее значение в массив текущих выбранных значений
            }
            });
            
            // Код для управления размером поля выбора
            if (value !== '' && currentChoices.length > 0) {
              selectField.size = Math.min(currentChoices.length, 4); // Изменение размера списка выбора
            } else {
              selectField.style.display = 'none'; // Скрываем поле выбора значений
            };
            // присваиваем полю inputField значение выбора из selectField
            selectField.addEventListener('change', function() {
              inputField.value = selectField.value;
            });
      
           // -----------   изменяем стандартное поведение клавиш   -----------  

                                // ---- для полей inputField   ---- 

            inputField.addEventListener('keydown', function(event) {
              if (event.key === 'ArrowDown') { // Событие для клавиши стрелки вниз
                event.preventDefault(); // Предотвращаем стандартное поведение клавиши "ArrowDown"
                selectField.style.display = 'block'; // Показываем поле выбора значений
                selectField.size = Math.min(currentChoices.length, 6); // Изменяем размер списка выбора
            
                // Переводим фокус на первую запись в поле выбора
                if (selectField.options.length > 0) {  // если значений в списке > 0
                    selectField.selectedIndex = 0; // выбираем индех первого значения
                    selectField.focus(); // Переводим фокус на поле выбора значений
                }
              }else if(event.key === 'Enter') {// Событие для клавиши 'Enter'
                event.preventDefault(); // Предотвращаем стандартное поведение клавиши 'Enter'
                selectField.style.display = 'none'; // Показываем поле выбора значений
              }else if(event.key === 'Escape') {// Событие для клавиши 'Escape'
                selectField.style.display = 'none'; // Показываем поле выбора значений
              }else if(event.key === 'Tab') {// Событие для клавиши 'Tab'
                selectField.style.display = 'none'; // Показываем поле выбора значений
              }
            });
            
                                // ---- для полей selectField   ---- 

            selectField.addEventListener('keydown', function(event) {
                if (event.code === 'Enter' || event.code === 'Space') {
                    event.preventDefault(); // Предотвращаем действие по умолчанию
                    inputField.value = selectField.value; // Присваиваем значение из поля выбора полю ввода
                    inputField.focus(); // Переводим фокус на поле ввода
                    selectField.style.display = 'none'; // Скрываем поле выбора
                }else if(event.key === 'Escape') {// Событие для клавиши 'Escape'
                    selectField.style.display = 'none'; // Показываем поле выбора значений
                    inputField.focus(); // Переводим фокус на поле ввода
                  }else if(event.key === 'Tab') {// Событие для клавиши 'Tab'
                    event.preventDefault(); // Предотвращаем стандартное поведение клавиши 'Enter'
                  }
            });

            // -----------   изменяем стандартное поведение мышки   для полей selectField  -----------  

            selectField.addEventListener('dblclick', function() {
              inputField.value = selectField.value; // Обновляем значение поля ввода
              selectField.value = selectField.value; // Обновляем значение поля выбора
              selectField.style.display = 'none'; // Скрываем поле выбора
              inputField.focus(); // Переводим фокус на поле ввода
            });                   
        })
        .catch(function(error) {
            console.log('Произошла ошибка при выполнении запроса:', error);
            console.log('Error:', error);
        });
};