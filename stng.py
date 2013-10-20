from flask import Flask, render_template, request, url_for, redirect, Response
from flask.ext.restful import reqparse, abort, Api, Resource
from git import *

app = Flask(__name__)
app.config.from_object('stng_config')
api = Api(app)

PAGES = {}

wiki_repo = Repo(app.config['REPO_PATH'])
print wiki_repo
tree = wiki_repo.heads.master.commit.tree
for blob in tree.blobs:
    print blob, blob.mime_type, blob.data_stream.read()

def abort_if_page_doesnt_exist(page_id):
    if page_id not in PAGES:
        abort(404, message="Page {} doesn't exist".format(page_id))

parser = reqparse.RequestParser()
parser.add_argument('title', type=str)
parser.add_argument('body', type=str)


# Page
#   shows a single page and lets you delete them
class Page(Resource):
    def get(self, page_id):
        abort_if_page_doesnt_exist(page_id)
        return PAGES[page_id]

    def delete(self, page_id):
        abort_if_page_doesnt_exist(page_id)
        del PAGES[page_id]
        return '', 204

    def put(self, page_id):
        args = parser.parse_args()
        page = {'title': args['title'], 'body': args['body'] }
        PAGES[page_id] = page
        return page, 201


# PageList
#   shows a list of all todos, and lets you POST to add new pages
class PageList(Resource):
    def get(self):
        return PAGES

    def post(self):
        args = parser.parse_args()
        page_id = args['title']
        PAGES[page_id] = {'title': page_id, 'body': args['body'] }
        return PAGES[page_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(PageList, '/pages')
api.add_resource(Page, '/pages/<string:page_id>')

# Volunteer list
@app.route("/", methods=['GET'])
def volunteers_page():
    pages = PAGES

    return render_template('index.html',
                           pages=pages)

if __name__ == '__main__':
    app.run(debug=True)