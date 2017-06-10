# Tentacle

**Tentacle is a sample terminal tool for querying detailed information of repositories in Docker Hub.**

###  Main Features

* Support most of operation for querying repositories
* Display result set in table
* Sort result set with custome order
* Filter result set by custome list
* Pthon 2.6, 2.7 and 3.X support
* Support Linux and Mac OSX

### Installation

Tentacle can be installed using git and python, for example:

```
git  clone https://github.com/faycheng/tentacle.git
cd tentacle
python setup.py install
```

### Usage

Options:

```
$ tentacle
Usage: tentacle [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Options:
  --help  Show this message and exit.

Commands:
  login   Use username and password to obtain an access...
  repo    List repositories
  reset   'Reset config
  search  Search for repositories from Docker Hub by...
  show    Show detailed information of repository
  star    List, star, or unstar repositories
  tag     List tags of repository
```

Docker Hub Login lets people query more privated information of repositories.So, best priactice is to perform a login operation before using tentacle:

```
$ tentacle login
Username: your_username
Password: your_password
Login success
```

Search for repositories about nginx:

```
$ tentacle search nginx
Count:18524
| repo_name               | pull_count | is_automated | star_count | is_official |
|-------------------------|------------|--------------|------------|-------------|
| nginx                   | 671232837  | False        | 6157       | True        |
| jwilder/nginx-proxy     | 13273278   | True         | 1044       | False       |
| richarvey/nginx-php-fpm | 1649688    | True         | 383        | False       |
| 1science/nginx          | 1236160    | True         | 4          | False       |
| bitnami/nginx           | 234468     | True         | 29         | False       |
| blacklabelops/nginx     | 139141     | True         | 5          | False       |
| webdevops/php-nginx     | 128517     | True         | 78         | False       |
| webdevops/nginx         | 51778      | True         | 7          | False       |
| xutongle/nginx          | 16432      | True         | 1          | False       |
| watsco/nginx            | 11699      | True         | 0          | False       |
| dock0/nginx             | 5955       | True         | 2          | False       |
| xataz/nginx             | 3431       | True         | 2          | False       |
| tozd/nginx              | 3237       | True         | 1          | False       |
| drupaldocker/nginx      | 1982       | True         | 2          | False       |
| frekele/nginx           | 1942       | True         | 3          | False       |
```

Show the datailed information of reporitory that named `faycheng/nginx`:

```
$ tentacle show faycheng/nginx
Name: nginx
Starred: False
User: faycheng
Namespace: faycheng
Repository Type: image
Private: False
Automated: False
Star Count: 1
Pull Count: 1
Last Updated: 2017-06-08T14:28:30.286399Z
Permissions: {u'read': True, u'write': False, u'admin': False}
Full Description:
Dockerfile:

FROM nginx
MAINTAINER FayCheng <fay.cheng.cn@gmail.com>

ENV MYSQL_ROOT_PASSWORD dangerous
COPY ./nginx.conf /etc/nginx/nginx.conf
RUN ln -s /usr/share/nginx/html /html
WORKDIR /usr/share/nginx/html

Usage:
docker run -v ./html:/html -d faycheng/nginx:gzip
```

List all tags of repository that name `library/nginx`:

```
$ tentacle tag library/nginx
Count:105
| name               | id       | full_size | v2   | last_updated                |
|--------------------|----------|-----------|------|-----------------------------|
| stable-perl        | 10128273 | 54721847  | True | 2017-05-30T17:53:35.603830Z |
| stable-alpine-perl | 10128355 | 18168458  | True | 2017-05-30T17:58:24.923640Z |
| stable-alpine      | 2255508  | 6737521   | True | 2017-05-30T17:55:43.415078Z |
| 1.12.0-perl        | 10128266 | 54721847  | True | 2017-05-30T17:52:55.050569Z |
| 1.12.0-alpine-perl | 10128345 | 18168458  | True | 2017-05-30T17:57:27.886502Z |
| 1.12.0-alpine      | 10128298 | 6737521   | True | 2017-05-30T17:55:08.063236Z |
| 1.12-perl          | 10128285 | 54721847  | True | 2017-05-30T17:54:17.505205Z |
| 1.12-alpine-perl   | 10128368 | 18168458  | True | 2017-05-30T17:59:07.647187Z |
| 1.12-alpine        | 10128335 | 6737521   | True | 2017-05-30T17:56:25.553743Z |
| 1.12               | 10128336 | 44807014  | True | 2017-05-30T17:52:12.812253Z |
```

List all repositories that belong to current logged in user:

```
$ tentacle repo
| namespace | name                   |
|-----------|------------------------|
| faycheng  | nginx                  |
| faycheng  | mysql                  |
| faycheng  | py3                    |
| faycheng  | alpine_benchmark_flask |
| faycheng  | sloth_backend          |
| faycheng  | wren                   |
| faycheng  | wren_bata              |
| faycheng  | ubuntu-dev             |
```

Star repository that named `library/redis`:

```
$ tentacle star --repo=library/redis
Star library/redis success
```

Unstar repository that name `library/redis`:

```
$ tentacle star -d --repo=library/redis
UnStar library/redis success
```

List all starred repositories that belong to current logged in user:

```
$ tentacle star -l
Count:3
| name  | namespace | is_private | is_automated | star_count | pull_count | last_updated                |
|-------|-----------|------------|--------------|------------|------------|-----------------------------|
| py3   | faycheng  | False      | False        | 1          | 34         | 2017-06-01T15:46:10.702646Z |
| nginx | faycheng  | False      | False        | 1          | 1          | 2017-06-08T14:28:30.286399Z |
| mysql | faycheng  | False      | False        | 1          | 1          | 2017-06-08T14:01:15.687302Z |
```



### Contribute

If you'd like to contribute, fork this repository, commit your changes to the develop branch, and send a pull request.

