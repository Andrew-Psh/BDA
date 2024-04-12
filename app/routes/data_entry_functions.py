from app import app, db
from flask import render_template, url_for, flash, redirect
from app.models import Accum
from app.forms import AddNode, AddModel, AddAccum, AddCity
from app.models import City, Node, Accum


@app.route('/add_accum', methods=['GET', 'POST'])
def add_accum():
    '''вывод формы "AddAccum" '''

    form = AddAccum()
    fields_data = form.to_dict_field_attr()
    print('in add_(): fields_data =', fields_data)
    if form.validate_on_submit(): 
        flash(f"Форма {form.__class__.__name__} валидна!")
        try:
            
            accum_obj = Accum(
                model_rel = form.add_model.input_field.data,
                No = form.add_No.data,
                d_prod = form.add_d_prod.data,
                states_rel = form.add_state.input_field.data, 
                node_rel = form.add_node.input_field.data, 
                d_edit = form.add_d_edit.data, 
                equips_rel = form.add_equip.input_field.data, 

                comment = form.comment.data
                )

            db.session.add(accum_obj)
            db.session.rollback()  # Отменить все неподтвержденные изменения
            # db.session.commit()
            
            flash("Аккумулятор модели {} No {}, произведенный {}. Статус {} внесен в БД.".format(accum_obj.model_rel, accum_obj.No, accum_obj.d_prod, accum_obj.state, ))
            return redirect(url_for('add_accum'))    
         
        except ValueError as e:
            flash(f"Произошла ошибка: {e}")
            raise ValueError('Узел связи не внесен в БД') 
        
    link_buttom = 'get_table_accs'
    buttom_name = 'Аккумуляторы'
  
    return render_template('forms/add_accum.html', 
                           title="Add Accum", 
                           form=form, 
                           fields_data=fields_data, 
                           link_buttom=link_buttom,
                           buttom_name=buttom_name                           
    )


@app.route('/add_node', methods=['GET', 'POST'])
def add_node():
    '''вывод формы "AddNode" '''

    form = AddNode()
    fields_data = form.to_dict_field_attr()
    print('in add_node(): fields_data =', fields_data)
    if form.validate_on_submit(): 
        flash(f"Форма {form.__class__.__name__} валидна!")
        try:
            city_data = form.city_name.input_field.data
            city_obj = City.query.filter_by(city=city_data).first()
            if not city_obj:
                city_obj = City(city = city_data)
                db.session.add(city_obj)
                db.session.rollback()
                # db.session.commit()
            existing_city = City.query.filter_by(city=city_data).first()

            node_obj = Node(
                street = form.street_name.input_field.data, 
                house = form.house.data, 
                place = form.place.data, 
                city_rel = existing_city, 
                comment = form.comment.data
                )
            node_obj.addr = f'{node_obj.street}, \
                              {node_obj.house}, \
                              {node_obj.place}'  # Формирование адреса на основе других полей

            db.session.add(node_obj)
            db.session.rollback()  # Отменить все неподтвержденные изменения
            # db.session.commit()
            
            flash("Узел связи в городе {}, по адресу {} внесен в БД.".format(city_data, node_obj.addr))
            return redirect(url_for('add_node'))    
         
        except ValueError as e:
            flash(f"Произошла ошибка: {e}")
            raise ValueError('Узел связи не внесен в БД') 

    link_buttom = 'get_table_nodes_srv'
    buttom_name = 'Узлы связи'

    return render_template('forms/add_node.html', 
                           title="Add Node", 
                           form=form, 
                           fields_data=fields_data,
                           link_buttom=link_buttom,
                           buttom_name=buttom_name
    )


@app.route('/add_model', methods=['GET', 'POST'])
def add_model():
    '''вывод формы "AddModel" '''

    form = AddModel()
    fields_data = form.to_dict_field_attr()
    print("in @app.route(/add_model) fields_data =", fields_data)
    if form.validate_on_submit(): 
        flash(f"Форма {form.__class__.__name__} валидна!")
        try:
            model_obj = form(
                model = form.add_model.input_field.data, 
                manuf = form.add_manuf.input_field.data, 
                charge = form.add_charge.data, 
                comment = form.comment.data
                )
    
            db.session.add(model_obj)
            db.session.rollback()  # Отменить все неподтвержденные изменения
            # db.session.commit()
            
            flash("Модель аккумулятора {} {}, емкостью {} A/h внесен в БД.".format(model_obj.model, model_obj.manuf, model_obj.charge))
            return redirect(url_for('add_model'))    
         
        except ValueError as e:
            flash(f"Произошла ошибка: {e}")
            raise ValueError('Модель аккумулятора не внесена в БД') 

    link_buttom = 'get_table_models'
    buttom_name = 'Модели аккумуляторов'

    return render_template('forms/add_model.html', 
                           title="Add ModelAcc", 
                           form=form, 
                           fields_data=fields_data, 
                           link_buttom=link_buttom,
                           buttom_name=buttom_name                           
    )


@app.route('/add_city', methods=['GET', 'POST'])
def add_city():
    '''вывод формы "AddCity" '''

    form = AddCity()
    fields_data = form.to_dict_field_attr()
    print('in add_node(): fields_data =', fields_data)
    if form.validate_on_submit(): 
        flash(f"Форма {form.__class__.__name__} валидна!")
        try:
            city_data = form.city_name.input_field.data
            city_comment =form.comment.data
            city_obj = City.query.filter_by(city=city_data).first()
            if not city_obj:
                city_obj = City(city = city_data,
                                comment= city_comment)
                db.session.add(city_obj)
                # db.session.rollback()
                db.session.commit()
                flash("Город {}, внесен в БД.".format(city_data))

            else:
                flash("Город {}, уже есть в БД.".format(city_data))
            return redirect(url_for('add_city'))    
         
        except ValueError as e:
            flash(f"Произошла ошибка: {e}")
            raise ValueError('Город не внесен в БД') 

    link_buttom = 'get_table_cities'
    buttom_name = 'Города'

    return render_template('forms/add_city.html', 
                           title="Add City", 
                           form=form, 
                           fields_data=fields_data,
                           link_buttom=link_buttom,
                           buttom_name=buttom_name
    )
