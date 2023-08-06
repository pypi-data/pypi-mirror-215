import os, requests, datetime, time, queue, threading, asyncio
from copy import deepcopy as dc
from threading import Lock
from typing import Dict, List, Callable, Generic, TypeVar
from abc import ABC, abstractmethod
from fileinput import FileInput as finput
import mystring,splittr
import pause
from github import Github, Repository
import git2net
import pygit2 as git2
from contextlib import suppress

GRepo_Saving_Progress_Lock = threading.Lock()

class niceghapi(object):
	def __init__(self):
		self.cur_status = None
		self.now = None
		self.resetdate = None

	@property
	def status(self):
		# curl -I https://api.github.com/users/octocat|grep x-ratelimit-reset
		self.cur_status, self.now = requests.get("https://api.github.com/users/octocat").headers, datetime.datetime.now()
		return {
			'Reset': self.cur_status['X-RateLimit-Reset'],
			'Used': self.cur_status['X-RateLimit-Used'],
			'Total': self.cur_status['X-RateLimit-Limit'],
			'Remaining': self.cur_status['X-RateLimit-Remaining'],
			'RemainingDate':datetime.datetime.fromtimestamp(int(self.cur_status['X-RateLimit-Reset'])),
			'WaitFor':datetime.datetime.fromtimestamp(int(self.cur_status['X-RateLimit-Reset'])) - self.now,
			'WaitForSec':(datetime.datetime.fromtimestamp(int(self.cur_status['X-RateLimit-Reset'])) - self.now).seconds,
			'WaitForNow':lambda :(datetime.datetime.fromtimestamp(int(self.cur_status['X-RateLimit-Reset'])) - datetime.datetime.now()).seconds,
		}

	@property
	def timing(self):
		import time
		if not hasattr(self, 'remaining') or self.remaining is None:
			stats = self.status
			print(stats)
			self.remaining = int(stats['Remaining'])
			self.wait_until = stats['WaitForNow']
			self.resetdate = stats['RemainingDate']
			self.timing
		elif self.remaining >= 10:
			self.remaining = self.remaining - 1
		else:
			print("Waiting until: {0}".format(self.resetdate))
			pause.until(self.resetdate)
			delattr(self, 'remaining')
			delattr(self, 'wait_until')
		return

class githuburl(object):
	def __init__(self,url,token=None,verify=True,commit=None,tag=None):
		self.url = mystring.string(dc(url))
		self.token = mystring.string(token)
		self.verify = verify
		self.stringurl = mystring.string(dc(url))
		self.commit = None
		self.tag = None
		self.api_watch = niceghapi()

		url = mystring.string(url).repsies('https://','http://','github.com/').repsies_end('.git', "/")
		self.owner, self.reponame = url.split("/")
		self.owner, self.reponame = mystring.string(self.owner), mystring.string(self.reponame)

		if not mystring.string(tag).empty:
			self.tag = mystring.string(tag)
			self.stringurl += f"<b>{tag}"
		if not mystring.string(self.commit).empty:
			self.commit = mystring.string(commit)
			self.stringurl += f"<#>{self.commit}"

	@property
	def dir(self):
		return mystring.string(self.reponame+"/")

	@property
	def core(self):
		return mystring.string("{0}/{1}".format(self.owner, self.reponame))

	@property
	def furl(self):
		return mystring.string("https://github.com/{0}".format(self.core))

	def filewebinfo(self, filepath, lineno=None):
		baseurl = "https://github.com/{0}/blob/{1}/{2}".format(self.core, self.commit,
															filepath.replace(str(self.reponame) + "/", '', 1))
		if lineno:
			baseurl += "#L{0}".format(int(lineno))

		return mystring.string(baseurl)

	#Transforming this into a cloning function
	def __call__(self,return_error=False, json=True, baserun=False,headers = {}):
		mystring.string("git clone {}".format(self.furl)).exec(True)

		if self.commit:
			with mystring.foldentre()(self.dir):
				mystring.string(f"git checkout {self.commit}").exec(True)
		return self.dir

	def __enter__(self):
		self()
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		mystring.string("yes|rm -r {0}".format(self.dir)).exec(True)
		return self

	def find_asset(self,asset_check=None, accept="application/vnd.github+json", print_info=False):
		if asset_check is None:
			asset_check = lambda x:False

		def req(string, verify=self.verify, accept=accept, auth=self.token, print_info=print_info):
			try:
				output = requests.get(string, verify=verify, headers={
					"Accept": accept,
					"Authorization":"Bearer {}".format(auth)
				})
				if print_info:
					print(output)
				return output.json()
			except Exception as e:
				if print_info:
					print(e)
				pass

		latest_version = req("https://api.github.com/repos/{}/releases/latest".format(self.core))
		release_information = req(latest_version['url'])
		for asset in release_information['assets']:
			if asset_check(asset['name']):
				return asset
		return None

	def download_asset(self, url, save_path, chunk_size=128, accept="application/vnd.github+json"):
		r = requests.get(url, stream=True, verify=self.verify, headers={
			"Accept": accept,
			"Authorization":"Bearer {}".format(self.token)
		})
		with open(save_path, 'wb') as fd:
			for chunk in r.iter_content(chunk_size=chunk_size):
				fd.write(chunk)
		return save_path

	def get_date_from_commit_url(self, accept="application/vnd.github+json"):
		req = requests.get(self.furl, headers={
			"Accept": accept,
			"Authorization":"Bearer {}".format(self.token)
		}).json()
		return datetime.datetime.strptime(req['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")

	def get_commits_of_repo(self, from_date=None, to_date=None, accept="application/vnd.github+json"):
		params = []
		if from_date:
			params += ["since={0}".format(from_date)]
		if from_date:
			params += ["until={0}".format(to_date)]
		request_url = "https://api.github.com/repos/{0}/commits?{1}".format(self.core, '&'.join(params))
		req = requests.get(request_url, headers={
			"Accept": accept,
			"Authorization":"Bearer {}".format(self.token)
		})
		return req.json()

	@property
	def zip_url(self):
		url_builder = self.furl + "/archive"
		if self.commit:
			url_builder += f"/{self.commit}.zip"
		elif self.tag:
			url_builder += f"/{self.tag}.zip"

		self.zip_url_base = url_builder
		return self.zip_url_base

	@property
	def webarchive_save_url(self,):
		return mystring.string("https://web.archive.org/save/" + self.zip_url)

T = TypeVar('T')
class GRepo_Seed_Metric(ABC, Generic[T]):
	@abstractmethod
	def name(self) -> str:
		pass

	@abstractmethod
	def metric(self, filename: str, source_code: str) -> T:
		pass

	@abstractmethod
	def diff(self, latest: T, previous: T):
		pass

	def __call__(self):
		setattr(self.metric, 'diff', self.diff)
		return self.metric


class GRepo_Pod(object):
	def __init__(self, metrics:List[GRepo_Seed_Metric], token:str=None,num_processes:int = None, delete_paths:bool=False):
		self.metrics = metrics
		self.token = token
		if "GH_TOKEN" not in os.environ:
			self.login()

		self.g = Github(self.token)
		self.processor = mystring.MyThreads(10)
		self.processed_paths = queue.Queue()
		setattr(self.processed_paths, 'lock', threading.Lock())

		self.current_repo_itr = None
		self.total_repo_len = None
		self.num_processes = num_processes

		def appr(string: mystring.string):
			with open("mapping_file_{0}.csv".format(string.tobase64()), "a+") as writer:
				writer.write(string)
		self.appr = appr
		self.api_watch = niceghapi()
		self.delete_paths = delete_paths
		self.query_string = None
		self.tracking_repos = None
		self.tracking_name = None
		asyncio.run(self.handle_history())

	@property
	def localfilename(self):
		if self.tracking_name is None:
			self.tracking_name = mystring.string("query_progress_{0}.csv".format(
				mystring.string("{query_string}".format(query_string=self.query_string)).tobase64())
			)
		return self.tracking_name


	@property
	def repos(self):
		if self.tracking_repos is None:
			self.tracking_repos = []
			if os.path.exists(self.localfilename):
				with open(self.localfilename, "r") as reader:
					for line in reader:
						ProjectItr, ProjectURL, ProjectScanned = line.split(",")
						if ProjectScanned == "false":
							self.tracking_repos.append(ProjectURL)
			else:
				self.tracking_repos = [x.clone_url for x in self.g.search_repositories(query=self.query_string)]
		return self.tracking_repos

	def save(self, current_project_url:str=None):
		#Make Thread Safe
		with GRepo_Saving_Progress_Lock:
			if not os.path.exists(self.localfilename):
				with open(self.localfilename, "w+") as writer:
					writer.write("ProjectItr,ProjectURL,ProjectScanned\n")
					for proj_itr, proj in enumerate(self.repos):
						writer.write("{0},{1},false\n".format(proj_itr, proj))

			if current_project_url is not None:
				found = False
				with finput(self.localfilename, inplace=True) as reader:
					for line in reader:
						if not found and current_project_url in line:
							line = line.replace("false", "true")
						print(line, end='')
		return

	@property
	def timing(self):
		self.api_watch.timing

		extra_rate_limiting = self.g.get_rate_limit()
		if hasattr(extra_rate_limiting, "search"):
			search_limits = getattr(extra_rate_limiting, "search")
			if search_limits.remaining < 2:
				print("Waiting until: {0}".format(search_limits.reset))
				pause.until(search_limits.reset)
	
	def repair(self,path,create:bool=True):
		if self.delete_paths and os.path.exists(path):
			os.system("yes|rm -r "+str(path))
		if create:
			os.makedirs(path, exist_ok=True)

	def __call__(self, search_string:str):
		self.timing
		search_string = mystring.string(search_string)

		def process_prep(repo_itr:int, repo_clone_url:str, search_string:str, appr:Callable, fin_queue:queue.Queue):
			self.query_string = search_string
			def process():
				name = mystring.string("ITR>{0}_URL>{1}_STR>{2}\n".format(
					repo_itr, repo_clone_url, search_string
				))
				repo_dir = "repo_" + str(name.tobase64())
				results_dir = "results_" + str(name.tobase64())

				self.repair(repo_dir, create=False)
				self.repair(results_dir)

				sqlite_db_file = os.path.join(results_dir, "git_to_net.sqlite")

				git2.clone_repository(repo_clone_url, repo_dir)  # Clones a non-bare repository

				if self.num_processes is None:
					git2net.mine_git_repo(repo_dir, sqlite_db_file)
				else:
					git2net.mine_git_repo(repo_dir, sqlite_db_file, no_of_processes=self.num_processes)
				
				git2net.mining_state_summary(repo_dir, sqlite_db_file)
				git2net.disambiguate_aliases_db(sqlite_db_file)
				git2net.compute_complexity(repo_dir, sqlite_db_file, no_of_processes=1, extra_eval_methods=self.metrics)

				if os.stat(sqlite_db_file).st_size > 100_000_000:
					with mystring.foldentre(new_path=results_dir):
						raw_db_file = sqlite_db_file.replace(results_dir, '')
						splittr.hash(raw_db_file)
						splittr.split(raw_db_file, 50_000_000)
						splittr.template(raw_db_file+".py")

				appr(mystring.string(name.replace(',',';').replace('_',',').strip()))
				fin_queue.put(repo_clone_url)

			return process

		if len(self.repos) > 0:
			for repo_itr, repo_url in enumerate(self.repos):
				self.processor += process_prep(repo_itr, repo_url, search_string, self.appr, self.processed_paths)
				self.current_repo_itr = repo_itr
		else:
			print("No Repos Found")

	def login(self):
		os.environ['GH_TOKEN'] = self.token
		with suppress(Exception):
			with open("~/.bashrc", "a+") as writer:
				writer.write("GH_TOKEN={0}".format(self.token))

	@property
	def complete(self):
		return self.total_repo_len == self.current_repo_itr and self.processor.complete

	async def handle_history(self):
		while not self.complete:
			# Get up to 5 strings from the queue
			paths,num_waiting = [], 5
			while len(paths) < num_waiting:
				try:
					path = self.processed_paths.get()
					paths.append(path)
				except queue.Empty:
					time.sleep(10)
					num_waiting -= 1

			# Process the strings
			for path in paths:
				mystring.string("git add {0}".format(path)).exec()
			mystring.string("git commit -m \"Added multiple paths\"").exec()
			mystring.string("git push").exec()
			for path in paths:
				mystring.string("yes|rm -r {0}".format(path)).exec()

			for path in paths:
				self.save(path)