import urllib.request
import bs4
import git
import os
import datetime

from __init__ import RESULT_PATH
from __init__ import RESULT_REMOTE_URL

def log_file(fname, content):
    f = open("./{}".format(fname), 'w', encoding="UTF-8")
    f.write(content)
    f.close()


def append_result(fname, content):
    # f = open("./result/{}".format(fname), 'w', encoding="UTF-8")
    # f.write(content)
    # f.close()
    if not os.path.exists(RESULT_PATH):
        os.makedirs(RESULT_PATH)
    try:
        git.Repo(RESULT_PATH)
    except git.InvalidGitRepositoryError:
        git.Repo.init(RESULT_PATH)
    repo = git.Repo(RESULT_PATH)
    remote_name = ""
    if RESULT_REMOTE_URL not in [remote.config_reader.get("url") for remote in repo.remotes]:
        candidate_names = ["origin", "github", "xiamubobby"]
        for name in candidate_names:
            try:
                remote_name = name
                repo.create_remote(name, RESULT_REMOTE_URL)
                break
            except RuntimeError:
                pass
    else:
        the_remote = [remote for remote in repo.remotes if remote.config_reader.get("url") == RESULT_REMOTE_URL]
        assert len(the_remote) == 1
        remote_name = the_remote[0].name

    remote = repo.remote(remote_name)
    commit_message = str(datetime.datetime.now()).replace('-', '_').replace(' ','_').replace('.','_').replace(':','_')
    repo.index.commit(commit_message)
    remote.fetch()
    print(str(remote))
    # repo.active_branch.set_tracking_branch(remote.)
    # remote.pull()
    # repo.index.commit(commit_message)
    # remote.push()
    # git.Remote.create()
    # print(str(repo.remotes))


# url = "http://toutiao.io/"
# user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
# headers = { 'User-Agent' : user_agent }
# req = urllib.request.Request(url, headers=headers)
# with urllib.request.urlopen(req) as response:
#     html = response.read()
#
# soup = bs4.BeautifulSoup(html)
# daily = soup.find(id="daily")
# daily_contents = daily.find_all("div", class_="content")
# result = [{"link" : content.h3.a['href'], "title":content.h3.a.string} for content in daily_contents]
#
# result_strs = ["{} : {}".format(content["title"], content["link"]) for content in result]
# result_str = '\n'.join(result_strs)
#
# # log_file("test_result.html", result_str)
result_str = ""

append_result("Toutiao", result_str)
print(result_str)
