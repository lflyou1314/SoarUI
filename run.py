#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import subprocess

import flask
from flask import jsonify
from flask import render_template
from flask import request

SoarUI = flask.Flask(__name__, template_folder='templates')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@SoarUI.route('/')
def server_status():
    logger.info("index.html")
    return render_template("index.html", content="")


@SoarUI.route('/soar-ui', methods=['GET'])
def index():
    data = {}
    logger.info("SoarUI")
    data['ret'] = 200
    data['data'] = 'Serving Flask app - SoarUI'
    data['msg'] = 'success'
    return jsonify(data)


@SoarUI.route('/v1/connect', methods=['POST'])
def check_connect():
    data = {}
    if request.method == 'POST':
        logger.info("connection post method")
        dsn_url = request.form.get('dsn_url', type=str, default=None)
        if dsn_url:
            commandline = "echo 'select now()'   | ./soar/soar -test-dsn '{}' -allow-online-as-test |grep -i explain".format(
                dsn_url)
            (status, output) = subprocess.getstatusoutput(commandline)
            logger.info("/v1/connect status {}".format(status))
            logger.info("/v1/connect output {}".format(output))
            data['status'] = status
            data['result'] = "Connection success!" if "Explain" in output else "connection failed!!!"
        else:
            logger.info("parameter error")
            data['result'] = "parameter error"
    return jsonify(data)


@SoarUI.route('/v1/fingerprint', methods=['POST'])
def sql_fingerprint():
    data = {}
    if request.method == 'POST':
        logger.info("fingerprint post method")
        sql_from_user = request.form.get('sql', type=str, default=None).replace("`", "")
        if sql_from_user:
            commandline = "echo \"" + sql_from_user + "\" | ./soar/soar -report-type=fingerprint"
            (status, output) = subprocess.getstatusoutput(commandline)
            logger.info("/v1/fingerprint status {}".format(status))
            logger.info("/v1/fingerprint output {}".format(output))
            data['status'] = status
            data['result'] = output
        else:
            logger.info("parameter error")
            data['result'] = "parameter error"
    return jsonify(data)


@SoarUI.route('/v1/beautifysql', methods=['POST'])
def sql_beautify():
    data = {}
    if request.method == 'POST':
        logger.info("sql beautify post method")
        sql_from_user = request.form.get('sql', type=str, default=None).replace("`", "")
        if sql_from_user:
            commandline = "echo \"" + sql_from_user + "\" | ./soar/soar -report-type=pretty | tail -n +2"
            (status, output) = subprocess.getstatusoutput(commandline)
            logger.info("/v1/beautifysql status {}".format(status))
            logger.info("/v1/beautifysql output {}".format(output))
            data['status'] = status
            data['result'] = output
        else:
            logger.info("parameter error")
            data['result'] = "parameter error"
    return jsonify(data)


@SoarUI.route('/v1/syntax_check', methods=['POST'])
def sql_syntax_check():
    data = {}
    logger.info("syntax check")
    if request.method == 'POST':
        logger.info("syntax_check post method")
        sql_from_user = request.form.get('sql', type=str, default=None).replace("`", "")
        if sql_from_user:
            commandline = "echo \"" + sql_from_user + "\" | ./soar/soar -only-syntax-check"
            (status, output) = subprocess.getstatusoutput(commandline)
            logger.info("/v1/syntax_check status {}".format(status))
            logger.info("/v1/syntax_check output {}".format(output))
            data['status'] = status
            data['result'] = "Your SQL syntax is OK! " if output == '' else output
        else:
            logger.info("parameter error")
            data['result'] = "parameter error"
    return jsonify(data)


@SoarUI.route('/v1/merge_alter', methods=['POST'])
def sql_merge_alter():
    data = {}
    logger.info("merge alter")
    if request.method == 'POST':
        logger.info("merge alter sql  post method")
        sql_from_user = request.form.get('sql', type=str, default=None).replace("`", "")
        if sql_from_user:
            commandline = "echo \"" + sql_from_user + "\" | ./soar/soar -report-type rewrite -rewrite-rules mergealter"
            (status, output) = subprocess.getstatusoutput(commandline)
            logger.info("/v1/merge_alter status {}".format(status))
            logger.info("/v1/merge_alter output {}".format(output))
            data['status'] = status
            data['result'] = output
        else:
            logger.info("parameter error")
            data['result'] = "parameter error"
    return jsonify(data)


@SoarUI.route('/v1/score', methods=['POST'])
def sql_score():
    data = {}
    if request.method == 'POST':
        logger.info("score sql  post method")
        sql_from_user = request.form.get('sql', type=str, default=None).replace("`", "")
        if sql_from_user:
            commandline = "echo  '{}' | ./soar/soar |head -n 4|tail -n 2".format(sql_from_user)
            (status, output) = subprocess.getstatusoutput(commandline)
            logger.info("/v1/score status {}".format(status))
            logger.info("/v1/score output {}".format(output))
            data['status'] = status
            data['result'] = output
        else:
            logger.info("parameter error")
            data['result'] = "parameter error"
    return jsonify(data)


@SoarUI.route('/v1/explain', methods=['POST'])
def sql_explain():
    data = {}
    if request.method == 'POST':
        logger.info("explain sql  post method")
        sql_from_user = request.form.get('sql', type=str, default=None).replace("`", "")
        if sql_from_user:
            commandline = "echo  '{}' | ./soar/soar |head -n 4|tail -n 2".format(sql_from_user)
            (status, output) = subprocess.getstatusoutput(commandline)
            logger.info("/v1/explain status {}".format(status))
            logger.info("/v1/explain output {}".format(output))
            data['status'] = status
            data['result'] = output
        else:
            logger.info("parameter error")
            data['result'] = "parameter error"
    return jsonify(data)


if __name__ == '__main__':
    SoarUI.debug = True
    SoarUI.run(host="0.0.0.0", port=8080)
