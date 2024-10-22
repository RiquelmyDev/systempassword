from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import create_user, get_user_by_username, add_email, get_emails_by_user_id, create_users_table, create_emails_table
from functools import wraps

# Criação do Blueprint para as rotas
bp = Blueprint('auth', __name__)

# decorador para proteger as rotas que requerem login