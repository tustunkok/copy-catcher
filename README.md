# CopyCATcher
CopyCATcher is a web-based wrapper for the [JPlag Plagiarism Detection Software](https://github.com/jplag/jplag) written with the [Django Framework](https://www.djangoproject.com/).

## Getting Started
A live instance of the project can be found in http://copycatcher.toliga.com/. Those folks who want to run their own instances in self-hosted servers can follow the instructions below.

### Prerequisites
There are no special prerequisites since the whole project is [Dockerized](https://www.docker.com/) other than the Docker's itself.

### Installing
1. Clone the project to a directory (e.g. `/home/<username>/Downloads/copy-catcher`).
2. Run the docker build command: `docker build --rm -t copycatcher ./`
3. Create an empty folder in a different path (e.g. `/home/<username>/copycatcher_data`) and create two subfolders with names `persist` and `static`.
4. Put a text file inside the `persist` directory called `secret_key.txt`. Inside the file write any garbage you want. This will be the secret key of the underlying Django application.
5. From inside the directory, run the following command: `docker run -d --name copycatcher -v "$(pwd)"/persist:/copy_catcher/persist -v "$(pwd)"/static:/static -p 8000:8000 -e DJANGO_SUPERUSER_USERNAME=<username> -e DJANGO_SUPERUSER_PASSWORD=<password> -e DJANGO_SUPERUSER_EMAIL="<email>" copycatcher` **!!!Do not for get to change the variables inside <>!!!**

With the last command, a uWSGI server is serving the application on port 8000. You can use the application either with a proxy server like NGINX or as it is.

## Versioning
[SemVer](https://semver.org/) is used for versioning. But, do not count on that.

## Authors
* [Tolga Üstünkök](https://github.com/tustunkok) - *Initial work*

## License
This project is under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Acknowledgements
* Thanks to @burcia1711 for the name of the project.
