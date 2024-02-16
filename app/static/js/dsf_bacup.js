// app/static/js/dsf_bacup.js


document.addEventListener('DOMContentLoaded', function() {
  var form = document.getElementById('formDinamic');
  if (form) {
      form.addEventListener('input', function(event) {
          if (event.target.classList.contains('form-input')) {
              var inputField = event.target;
              inputField.setAttribute('autocomplete', 'off');
              var tableName = inputField.parentElement.getAttribute('data-table-name'); 
              var selectField = event.target.parentElement.querySelector('.form-select'); 
              if (selectField) {
                  selectField.style.display = 'block'; // Показываем поле выбора значений
              } else{
                  console.log('Соседнее поле выбора не найдено');
              }
          fetchDataFromServerAndAssign(inputField, selectField, tableName);
          }
      });
  }
});

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