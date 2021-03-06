
from flask import Blueprint, current_app, jsonify, request

api_routes = Blueprint("v0_routes", __name__)

@api_routes.route("/api/v0/user_details/<screen_name>")
def user_details(screen_name=None):
    #print(f"USER DETAILS: '{screen_name}'")
    if "@" in screen_name or ";" in screen_name: # just be super safe about preventing sql injection. there are no screen names with semicolons
        return jsonify({"message": f"Oh, expecting a screen name like 'politico'. Please try again."}), 400

    response = list(current_app.config["BQ_SERVICE"].fetch_user_details_api_v0(screen_name))
    try:
        return jsonify(dict(response[0]))
    except IndexError as err:
        print(err)
        return jsonify({"message": f"Oh, couldn't find user with screen name '{screen_name}'. Please try again."}), 404

@api_routes.route("/api/v0/user_tweets/<screen_name>")
def user_tweets(screen_name=None):
    #print(f"USER TWEETS: '{screen_name}'")
    if "@" in screen_name or ";" in screen_name: # just be super safe about preventing sql injection. there are no screen names with semicolons
        return jsonify({"message": f"Oh, expecting a screen name like 'politico'. Please try again."}), 400

    response = list(current_app.config["BQ_SERVICE"].fetch_user_tweets_api_v0(screen_name))
    try:
        return jsonify([dict(row) for row in response])
    except IndexError as err:
        print(err)
        return jsonify({"message": f"Oh, couldn't find user with screen name '{screen_name}'. Please try again."}), 404

@api_routes.route("/api/v0/users_most_retweeted")
def users_most_retweeted():
    query_params = {"metric": request.args.get("metric"), "limit": request.args.get("limit")}
    print("QUERY PARAMS:", query_params)
    response = list(current_app.config["BQ_SERVICE"].fetch_users_most_retweeted_api_v0(**query_params))
    return jsonify([dict(row) for row in response])

@api_routes.route("/api/v0/statuses_most_retweeted")
def statuses_most_retweeted():
    query_params = {"metric": request.args.get("metric"), "limit": request.args.get("limit")}
    print("QUERY PARAMS:", query_params)
    response = list(current_app.config["BQ_SERVICE"].fetch_statuses_most_retweeted_api_v0(**query_params))
    return jsonify([dict(row) for row in response])

@api_routes.route("/api/v0/top_profile_tokens")
def top_profile_tokens():
    query_params = {"limit": request.args.get("limit")}
    print("QUERY PARAMS:", query_params)
    response = list(current_app.config["BQ_SERVICE"].fetch_top_profile_tokens_api_v0(**query_params))
    return jsonify([dict(row) for row in response])

@api_routes.route("/api/v0/top_profile_tags")
def top_profile_tags():
    query_params = {"limit": request.args.get("limit")}
    print("QUERY PARAMS:", query_params)
    response = list(current_app.config["BQ_SERVICE"].fetch_top_profile_tags_api_v0(**query_params))
    return jsonify([dict(row) for row in response])

@api_routes.route("/api/v0/top_status_tokens")
def top_status_tokens():
    query_params = {"limit": request.args.get("limit")}
    print("QUERY PARAMS:", query_params)
    response = list(current_app.config["BQ_SERVICE"].fetch_top_status_tokens_api_v0(**query_params))
    return jsonify([dict(row) for row in response])

@api_routes.route("/api/v0/top_status_tags")
def top_status_tags():
    query_params = {"limit": request.args.get("limit")}
    print("QUERY PARAMS:", query_params)
    response = list(current_app.config["BQ_SERVICE"].fetch_top_status_tags_api_v0(**query_params))
    return jsonify([dict(row) for row in response])
