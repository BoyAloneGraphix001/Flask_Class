from flask import Blueprint, flash, redirect, render_template, url_for

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(413)
def file_too_large(e):
    flash('That file is too large. Maximum size is 5MB.', 'danger')
    return redirect(url_for('users.account'))

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500