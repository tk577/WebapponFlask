
from flask import render_template, redirect, url_for, flash, request
from .app import app, db, basic_auth
from .model import Profiles, Items, Comment, OrderItem, SubmitOrder
from .user_forms import LoginForm, RegisterForm, EditProfile, Post
from flask_login import login_user, logout_user, login_required, current_user
from .app.setup.order_form import AddToCart, OrderData
from .app.setup.render_picture import RenderPicture
from .dbtools import products_in_cart, SubmitData, DataException
from .app.setup.calculating import CountTotalPrice
from .app.admin.add_items import AddItem
from .app.setup.card_payment_config import checkout_session_func, PaymentRouteException
from .app.setup.hard_psw import ValidatePsw


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/product/<id>', methods=['POST', 'GET'])
def product(id):
    product = Items.query.filter_by(id=id).first()
    comment = Comment.query.filter_by(items_id=product.item_name).all()
    form = AddToCart()
    return render_template('view_product.html', product=product, form=form, comment=comment)


@app.route('/product/<id>/post', methods=['POST', 'GET'])
@login_required
def add_post(id):
    product = Items.query.filter_by(id=id).first()
    post = Post()
    if post.validate_on_submit():

        user_commenting = Comment(comment=post.comment.data, items_id=product.item_name, profiles_id=current_user.name)
        try:
            SubmitData(user_commenting).add_data()
            flash(f"Отзыв отправлен!", category='success')
            return redirect(url_for('product', id=product.id))
        except DataException:
            flash(f"Ошибка при добавлении отзыва!", category='danger')

    return render_template('add_post.html', title='Оставьте отзыв о товаре!', post=post)


@app.route('/add_to_cart/<id>', methods=['POST', 'GET'])
@login_required
def add_to_cart(id):
    product = Items.query.filter_by(id=id).first()
    form = AddToCart()
    if form.validate_on_submit():
        quick_add = OrderItem(
            profiles_id=current_user.email,
            items_id=product.item_name,
            item_name=product.item_name,
            item_brand=product.item_brand,
            barcode=product.barcode,
            price=product.price
        )
        try:
            SubmitData(quick_add).add_data()
            flash(f"Товар {product.item_name} добавлен в корзину!", category='success')
            return redirect(url_for('store'))
        except DataException:
            flash(f"Ошибка при добавлении товара!", category='danger')

    return render_template('store.html')


@app.route('/cart/<id>', methods=['POST', 'GET'])
@login_required
def cart_page(id):
    form = AddToCart()
    products = products_in_cart._sort_order_item_all(current_user.email)
    total_price = CountTotalPrice(products).calculate_price()

    return render_template('cart.html', products=products, form=form, total_price=total_price)


@app.route('/remove-from-cart')
@login_required
def remove_from_cart():
    item_del = OrderItem.query.filter_by(profiles_id=current_user.email).first()

    try:
        SubmitData(item_del).delete_data()
        flash(f'Товар {item_del.item_name} убран из корзины', category='success')
        return redirect(url_for('cart_page', id=current_user.id))
    except DataException:
        flash(f'Произошла ошибка при удалении товара', category='danger')


@app.route('/cart/order_checkout', methods=['POST', 'GET'])
@login_required
def order_checkout():
    form = OrderData()
    products = products_in_cart._sort_order_item_all(current_user.email)
    total_price = CountTotalPrice(products).calculate_price()
    item_del = OrderItem.query.filter_by(profiles_id=current_user.email).first()
    if form.validate_on_submit():
        receipt = SubmitOrder(
            profiles_id=current_user.id,
            client_name=form.client_name.data,
            email=form.email.data,
            phone=form.phone.data,
            payment=form.payment.data,
            total_price=total_price
        )
        if form.payment.data == 'Наличными при получении':
            try:
                SubmitData(receipt).add_data()
                SubmitData(item_del).delete_data()
                flash(f'Заказ оформлен!', category='success')
                return redirect(url_for('cart_page', id=current_user.id))
            except DataException:
                flash(f'Произошла ошибка при заказе', category='danger')

        elif form.payment.data == 'Онлайн оплата':
            success_url = 'order/success'
            cancel_url = 'order/cancel'
            try:
                checkout_session = checkout_session_func(total_price, success_url, cancel_url)
                return redirect(checkout_session.url)
            except PaymentRouteException:
                flash(f'Произошла ошибка при онлайн оплате', category='danger')

        else:
            flash(f'Произошла ошибка при выборе оплаты', category='danger')

    return render_template('order_page.html', title='Оформление заказа', form=form, total_price=total_price)


@app.route('/order/success')
def success():
    products = products_in_cart._sort_order_item_all(current_user.email)
    total_price = CountTotalPrice(products).calculate_price()
    item_del = products_in_cart._sort_order_item_first(current_user.email)
    receipt = SubmitOrder(
        profiles_id=current_user.id,
        client_name=current_user.name,
        email=current_user.email,
        phone=current_user.phone,
        payment='Онлайн оплата',
        total_price=total_price
    )
    try:
        SubmitData(receipt).add_data()
        SubmitData(item_del).delete_data()
        flash(f'Оплата прошла успешно! Заказ оформлен!', category='success')
        return redirect(url_for('index'))
    except DataException:
        flash(f'Произошла ошибка после онлайн оплаты.\n'
              f'Обратитесь в техподдержку', category='danger')
        return redirect(url_for('cart_page', id=current_user.id))


@app.route('/order/cancel')
def cancel():
    flash(f'Онлайн оплата отменена', category='danger')
    return redirect(url_for('cart_page', id=current_user.id))


@app.route('/admin/')
@basic_auth.required
def admin():
    items = Items.query.order_by(Items.price).all()
    return render_template('admin/index.html', data=items)


@app.route('/admin/list_items')
@basic_auth.required
def list_items():
    list_items_all = Items.query.order_by(Items.id).all()
    return render_template('admin/list_items.html', list=list_items_all, title='Зарегистрированные товары')


@app.route('/admin/add', methods=['POST', 'GET'])
@basic_auth.required
def add_item():
    form = AddItem()
    if form.validate_on_submit():
        file_image = form.image.data
        data = file_image.read()
        render_file = RenderPicture(data).render_picture()
        new_item = Items(item_brand=form.item_brand.data,
                         item_name=form.item_name.data,
                         category=form.category.data,
                         barcode=form.barcode.data,
                         display=form.display.data,
                         cpu=form.cpu.data,
                         rom=form.rom.data,
                         ram=form.ram.data,
                         date=form.date.data,
                         price=form.price.data,
                         description=form.description.data,
                         quantity=form.quantity.data,
                         image=data, rendered_data=render_file)
        try:
            SubmitData(new_item).add_data()
            flash(f'{new_item} успешно добавлен!', category='success')
            return redirect(url_for('list_items'))
        except DataException:
            #db.session.rollback()
            flash('Ошибка при добавлении товара', category='danger')

    return render_template('admin/add_item.html', form=form)


@app.route('/admin/del_item/<id>')
@basic_auth.required
def del_item(id):
    item_check = Items.query.filter_by(id=id).first()

    try:
        SubmitData(item_check).delete_data()
        flash(f'Товар {item_check.item_name} {item_check.barcode} удален', category='success')
        return redirect(url_for('list_items'))
    except DataException:
        flash(f'Произошла ошибка при удалении товара', category='danger')


@app.route('/admin/list_users')
@basic_auth.required
def list_users():
    list_users_all = Profiles.query.order_by(Profiles.id).all()
    return render_template('admin/list_users.html', list=list_users_all, title='Зарегистрированные пользователи')


@app.route('/admin/list_users/del/<id>')
@basic_auth.required
def del_user(id):
    user_check = Profiles.query.filter_by(id=id).first()

    try:
        SubmitData(user_check).delete_data()
        flash(f'Пользователь {user_check.email} удален', category='success')
        return redirect(url_for('list_users'))
    except DataException:
        flash(f'Произошла ошибка при удалении пользователя', category='danger')


@app.route('/admin/list_orders')
@basic_auth.required
def list_orders():
    orders = SubmitOrder.query.all()
    return render_template('admin/list_orders.html', list=orders, title='Оформленные заказы')


@app.route('/admin/list_orders/del/<id>')
@basic_auth.required
def del_order(id):
    order_check = SubmitOrder.query.filter_by(id=id).first()

    try:
        SubmitData(order_check).delete_data()
        flash(f'Заказ №{order_check.id} удален', category='success')
        return redirect(url_for('list_orders'))
    except DataException:
        flash(f'Произошла ошибка при удалении заказа', category='danger')


@app.route('/admin/product')
@basic_auth.required
def del_comment():
    comment_del = Comment.query.first()

    try:
        SubmitData(comment_del).delete_data()
        flash(f'Отзыв удален', category='success')
        return redirect(url_for('list_users'))
    except DataException:
        flash(f'Произошла ошибка при удалении отзыва', category='danger')


@app.route('/profile')
@login_required
def profile_page():
    profile = Profiles.query.all()
    return render_template('profile.html', profile=profile)


@app.route('/register', methods=["POST", "GET"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        if len(form.password1.data) >= 8:
            validate_psw = ValidatePsw(form.password1.data)
            if validate_psw.check_psw():
                user_to_create = Profiles(name=form.name.data,
                                          lastname=form.lastname.data,
                                          email=form.email.data,
                                          phone=form.phone.data,
                                          password=form.password1.data,
                                          date=form.date.data,
                                          city=form.city.data
                                          )
                try:
                    SubmitData(user_to_create).add_data()
                    login_user(user_to_create)
                    flash(f"Вы успешно зарегистрировались!", category='success')
                    return redirect(url_for('profile_page'))
                except DataException:
                    flash(f'{DataException(user_to_create)}')

            else:
                flash("Пароль должен состоять из цифр, латинских букв верхнего и нижнего регистров", category='danger')

        else:
            flash('Длина пароля должна быть больше 8 символов', category='danger')

    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'Ошибка при создании пользователя: {err_msg}', category='danger')

    return render_template('register.html', title='Регистрация', form=form)


@app.route('/profile/edit', methods=['POST', 'GET'])
@login_required
def edit_profile():
    edit_user = Profiles.query.first()
    form = EditProfile()
    if form.validate_on_submit():
        edit_user.name = form.name.data
        edit_user.lastname = form.lastname.data
        edit_user.email = form.email.data

        try:

            db.session.commit()
            flash(f"Изменения сохранены!", category='success')
            return redirect(url_for('edit_profile'))
        except DataException:
            flash(f"Ошибка!", category='danger')

    return render_template('profile_edit.html', title='Изменение профиля', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Profiles.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password1.data
        ):
            rm = form.remember.data
            login_user(attempted_user, remember=rm)
            flash(f"Вы вошли в профиль как: {attempted_user.email}", category='info')
            return redirect(request.args.get("next") or url_for("profile_page"))
        else:
            flash("Неверные данные! Попробуйте снова", category='danger')

    return render_template('login.html', title="Авторизация", form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("Вы вышли из профиля!", category='info')
    return redirect(url_for("index"))
