import flask
import json
import requests
import settings
import scraper

app = flask.Flask(__name__)

@app.route("/")
def route():
    # s = scraper.Scraper()
    wins = []
    # windows = s.scrape()
    with open('windows.json', 'r') as f:
        windows = json.load(f)
    for window in windows:
        w = json.loads(window)
        wins.append(w)
    return flask.render_template('index.html', windows=wins, google_maps_key=settings.GOOGLE_MAPS_KEY)

if __name__ == "__main__":
    app.run(debug=True)
