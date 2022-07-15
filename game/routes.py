from datetime import date, time
from game import app, db
from flask import render_template, request, session
from random import randint
from game.rock_paper_scissors import game_backend
from . import User, Game


@app.route("/", methods=["GET", "POST"])
def mainPage():
    if request.method == "GET":
        """Creating a new user and counting a today cumlative record and time"""
        user = User()
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        today_players = User.query.filter_by(date_created=date.today()).all()
        today_wins = 0
        today_draws = 0
        today_loses = 0
        for player in today_players:
            today_wins += player.wins
        for player in today_players:
            today_draws += player.draws
        for player in today_players:
            today_loses += player.loses
        cumulative_record = (today_wins, today_draws, today_loses)
        cumulative_time = time(0, 0, 0)
        for player in today_players:
            games = Game.query.filter_by(user_id=player.id).all()
            for game in games:
                duration = game.gametime
                hours = cumulative_time.hour + duration.hour
                minutes = cumulative_time.minute + duration.minute
                seconds = cumulative_time.second + duration.second
                hours += minutes // 60
                minutes %= 60
                minutes += seconds // 60
                seconds %= 60
                cumulative_time = time(
                    hour=hours, minute=minutes, second=seconds
                )

        return render_template(
            "main_page.html",
            user_id=session["user_id"],
            today_players=today_players,
            cumulative_record=cumulative_record,
            credits=user.credits,
            cumulative_time=cumulative_time,
        )
    if request.method == "POST":
        """Draw an item that the computer will choose"""
        pc_item = randint(1, 3)
        current_user_id = session["user_id"]
        user = User.query.filter_by(id=current_user_id).first()
        today_players = User.query.filter_by(date_created=date.today()).all()
        user_choice = 0
        """"Counting a today cumlative record and time when user must buy new 10 credits"""
        today_wins = 0
        today_draws = 0
        today_loses = 0
        for player in today_players:
            today_wins += player.wins
        for player in today_players:
            today_draws += player.draws
        for player in today_players:
            today_loses += player.loses
        cumulative_record = (today_wins, today_draws, today_loses)
        cumulative_time = time(0, 0, 0)
        for player in today_players:
            games = Game.query.filter_by(user_id=player.id).all()
            for game in games:
                duration = game.gametime
                hours = cumulative_time.hour + duration.hour
                minutes = cumulative_time.minute + duration.minute
                seconds = cumulative_time.second + duration.second
                hours += minutes // 60
                minutes %= 60
                minutes += seconds // 60
                seconds %= 60
                cumulative_time = time(
                    hour=hours, minute=minutes, second=seconds
                )
        """Not starting a game when user buy credits"""
        if request.form["submit_button"] == "Set credits to 10":
            user.credits = 10
            db.session.commit()
            record = (user.wins, user.draws, user.loses)
            cumulative_record = (today_wins, today_draws, today_loses)
            return render_template(
                "main_page.html",
                result="You have 10 credits",
                pc_item=pc_item,
                user_id=current_user_id,
                credits=user.credits,
                record=record,
                today_players=today_players,
                cumulative_record=cumulative_record,
                cumulative_time=cumulative_time,
            )
        """Check user choice and start a game"""
        if request.form["submit_button"] == "Rock":
            user_choice = 1
        elif request.form["submit_button"] == "Paper":
            user_choice = 2
        elif request.form["submit_button"] == "Scissors":
            user_choice = 3
        result = game_backend(user_choice, pc_item)
        """Change amount of credits along with player and cumulative record"""
        if user.credits > 3:
            user.credits -= 3
        else:
            user.credits = 0
        db.session.commit()
        if result == "You won, and you get 4 credits":
            user.credits += 4
            user.wins += 1
            game_result = 1
            db.session.commit()
        if result == "Draw":
            user.draws += 1
            game_result = 2
            db.session.commit()
        if result == "You lose":
            user.loses += 1
            game_result = 3
            db.session.commit()
        record = (user.wins, user.draws, user.loses)
        today_wins = 0
        today_draws = 0
        today_loses = 0
        for player in today_players:
            today_wins += player.wins
        for player in today_players:
            today_draws += player.draws
        for player in today_players:
            today_loses += player.loses
        cumulative_record = (today_wins, today_draws, today_loses)
        """Checking a game time and add a game statistic to database"""
        inputminutes = int(request.form["inputminutes"])
        inputseconds = int(request.form["inputseconds"])
        game_duration = time(0, inputminutes, inputseconds)
        game = Game(
            user_id=current_user_id,
            credits=user.credits,
            result=game_result,
            gametime=game_duration,
        )
        db.session.add(game)
        db.session.commit()
        cumulative_time = time(0, 0, 0)
        for player in today_players:
            games = Game.query.filter_by(user_id=player.id).all()
            for game in games:
                duration = game.gametime
                hours = cumulative_time.hour + duration.hour
                minutes = cumulative_time.minute + duration.minute
                seconds = cumulative_time.second + duration.second
                hours += minutes // 60
                minutes %= 60
                minutes += seconds // 60
                seconds %= 60
                cumulative_time = time(
                    hour=hours, minute=minutes, second=seconds
                )
        return render_template(
            "main_page.html",
            result=result,
            pc_item=pc_item,
            user_id=current_user_id,
            credits=user.credits,
            record=record,
            today_players=today_players,
            cumulative_record=cumulative_record,
            cumulative_time=cumulative_time,
        )
