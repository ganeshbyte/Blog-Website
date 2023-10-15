
from flask import make_response, render_template, request, url_for, flash, redirect
from sqlalchemy import desc
from flasknotes import app, db
from flasknotes.forms import NoteForm
from flasknotes.models import Post
from flask_login import current_user, login_required
from datetime import datetime


@app.route("/mypost")
@login_required
def mypost():

    page = request.args.get('page', 1, type=int)

    per_page = 1  # You can adjust the number of posts per page here

    # posts_query = Post.query.filter_by(user_id=current_user.id).order_by(desc(Post.date_note))

    posts_query = Post.query.order_by(desc(Post.date_note))

    posts = posts_query.paginate(page=page, per_page=per_page)

    return render_template('mypost.html', title='mypost', posts=posts)


@app.route("/")
@app.route("/home", methods=['POST', 'GET'])
def home():
    form = NoteForm()

    if form.validate_on_submit():

        new_entry_id = int(datetime.now().timestamp())

        post = Post(id=new_entry_id, title=form.title.data, date_note=form.date_note.data,
                    content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        print(current_user.posts)
        flash('Your Post has been created!', 'success')
        return make_response(redirect(url_for('mypost')))

    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(
                f'There was an error with creating a note: {err_msg}', category='danger')

    return render_template('home.html', title='Home', form=form)


@app.route('/posts/<int:post_id>', methods=['POST', 'GET'])
@login_required
def update(post_id):

    form = NoteForm()

    if form.validate_on_submit():

        post = Post.query.filter_by(id=post_id).first()

        post.title = form.title.data
        post.date_note = form.date_note.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post has been updated!', 'success')
        return make_response(redirect(url_for('home')))

    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(
                f'There was an error with updating a note: {err_msg}', category='danger')
    return render_template('update.html', title='Update', form=form, postId=post_id)


@app.route("/delete/<int:post_id>", methods=['GET', 'POST'])
@login_required
def delete(post_id):

    post = Post.query.get_or_404(post_id)

    if post != None:
        db.session.delete(post)
        db.session.commit()
        flash("Successfully Deleted Post!")
    else:
        flash("Post is not there to delete!")

    return redirect(url_for('mypost'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@app.errorhandler(Exception)
def not_found_error(e):
    return make_response(render_template('error.html'))
