import datetime

from flask import Blueprint, flash, redirect, render_template, url_for, session
from flask.ext.security import current_user
from flask.ext.security.registerable import register_user
from flask.ext.security.utils import login_user, logout_user, encrypt_password, verify_password, verify_and_update_password
from eveask.app import app, db, bcrypt
from eveask.forms import LoginForm, RegisterApiForm, RegisterAccountForm
from eveask.models import user_datastore
from evetools import EveTools

users = Blueprint('users', __name__, template_folder='templates/users')


@users.route('/login', defaults={'redirect_to': '/'}, methods=['GET', 'POST'])
@users.route('/login?next=<redirect_to>', methods=['GET', 'POST'])
def login(redirect_to):
    if current_user.is_authenticated():
        return redirect(url_for('home'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = user_datastore.find_user(username=login_form.username.data)
        if user is not None and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            flash('Welcome back {} !'.format(user.character_name), 'success')
            return redirect(redirect_to)
    if login_form.is_submitted() is True:
        flash('There was an error logging you in, please check your credentials', 'danger')
    return render_template('login.html', form=login_form)


@users.route('/register', methods=['GET', 'POST'])
def register_api():
    if current_user.is_authenticated():
        return redirect(url_for('home'))
    register_api_form = RegisterApiForm()
    if register_api_form.validate_on_submit():
        session['key_id'] = register_api_form.key_id.data
        session['vcode'] = register_api_form.vcode.data
        evetools = EveTools(session['key_id'], session['vcode'], cache=False)
        try:
            evetools.check_key()
        except Exception as e:
            flash('There was an error verifying your API Key: {}'.format(e.message), 'danger')
        else:
            return redirect(url_for('users.register_account'))
    return render_template('register_api.html', form=register_api_form)


@users.route('/register/account', methods=['GET', 'POST'])
def register_account():
    if current_user.is_authenticated():
        return redirect(url_for('home'))
    register_account_form = RegisterAccountForm()
    evetools = EveTools(session['key_id'], session['vcode'])
    try:
        characters = evetools.get_characters()
    except Exception as e:
        flash('There was an error while fetching your characters\' informations', 'danger')
        session.clear()
        return redirect(url_for('users.register_api'))
    register_account_form.character_id.choices = [(c.characterID, c.characterName) for c in characters]
    if register_account_form.validate_on_submit():
        character = [c for c in characters if c.characterID == register_account_form.character_id.data][0]
        eve_data = {
            'corporation_id': character.corporationID,
            'corporation_name': character.corporation
        }
        if character.allianceID:
            eve_data['alliance_id'] = character.allianceID
            eve_data['alliance_name'] = character.alliance
        try:
            user = register_user(
                username=register_account_form.username.data,
                email=register_account_form.email.data,
                password=register_account_form.password.data,
                character_id=register_account_form.character_id.data,
                character_name=character.characterName,
                created_at=datetime.datetime.utcnow(),
                key_id=session['key_id'],
                vcode=session['vcode'],
                **eve_data
            )
            user.password = bcrypt.generate_password_hash(register_account_form.password.data)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            app.logger.exception(e)
            flash('There was an error creating your account, please try again', 'danger')
            return render_template('register_account.html', form=register_account_form)
        login_user(user)
        flash('Thanks you for joining EveAsk ! You can now answer or ask questions', 'success')
        return redirect(url_for('home'))
    if register_account_form.is_submitted() is True:
        flash('We could not validate the informations you gave', 'danger')
    return render_template('register_account.html', form=register_account_form)


@users.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out with success', 'info')
    return redirect('/')
