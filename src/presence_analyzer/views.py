# -*- coding: utf-8 -*-
"""
Defines views.
"""

import calendar

from flask import redirect, render_template, redirect, url_for

from presence_analyzer.main import app
from presence_analyzer.utils import jsonify
from presence_analyzer import utils

import logging

log = logging.getLogger(__name__)  # pylint: disable-msg=C0103


@app.route('/')
def mainpage():
    """
    Redirects to front page.
    """
    return render_template('presence_weekday.html')


@app.route('/presence-weekday')
def presence_weekday():
    """
    Redirects to presence weekday page.
    """
    return render_template('presence_weekday.html')


@app.route('/mean-time-weekday')
def mean_time_weekday():
    """
    Redirects to mean time weekday page.
    """
    return render_template('mean_time_weekday.html')


@app.route('/presence-start-end')
def presence_start_end():
    """
    Redirects to presence start end page.
    """
    return render_template('presence_start_end.html')


@app.route('/api/v1/users', methods=['GET'])
@jsonify
def users_view():
    """
    Users listing for dropdown.
    """
    data = utils.get_data()
    return [{'user_id': i, 'name': 'User {0}'.format(str(i))}
            for i in data.keys()]


@app.route('/api/v1/mean_time_weekday/<int:user_id>', methods=['GET'])
@jsonify
def mean_time_weekday_view(user_id):
    """
    Returns mean presence time of given user grouped by weekday.
    """
    data = utils.get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        return []

    weekdays = utils.group_by_weekday(data[user_id])
    result = [
        (
            calendar.day_abbr[weekday], utils.mean(intervals)
        )
        for weekday, intervals in weekdays.items()
    ]

    return result


@app.route('/api/v1/presence_weekday/<int:user_id>', methods=['GET'])
@jsonify
def presence_weekday_view(user_id):
    """
    Returns total presence time of given user grouped by weekday.
    """
    data = utils.get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        return []

    weekdays = utils.group_by_weekday(data[user_id])
    result = [
        (
            calendar.day_abbr[weekday], sum(intervals)
        )
        for weekday, intervals in weekdays.items()
    ]

    result.insert(0, ('Weekday', 'Presence (s)'))
    return result


@app.route('/api/v1/presence_start_end/<int:user_id>', methods=['GET'])
@jsonify
def presence_start_end_view(user_id):
    """
    Returns time of given user grouped by mean start and end job.
    """
    import ipdb; ipdb.set_trace()
    data = utils.xml_parser()
    
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        return []
    weekdays = utils.group_times_by_weekday(data[user_id])



    data = utils.get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        return []

    weekdays = utils.group_times_by_weekday(data[user_id])
    result = [
        (
            calendar.day_abbr[weekday],
            utils.mean(times['start']),
            utils.mean(times['end']),
        )
        for weekday, times in weekdays.items()
    ]
    return result


@app.route('/api/v1/presence_xml_parser/<int:user_id>', methods=['GET'])
@jsonify
def xml_parser_view(user_id):
    """
    Return something nice
    """
    data = utils.xml_parser()
    import ipdb; ipdb.set_trace()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        return []
    weekdays = utils.group_times_by_weekday(data[user_id])
