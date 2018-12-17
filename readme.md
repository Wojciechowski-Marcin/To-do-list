# To-do list

Simple project that shows a list of tasks, which can be added or edited with sending specific HTML methods.

## Built With

* [Python3](https://www.python.org/) - Programming language
* [Flask](http://flask.pocoo.org/) - The web framework used
* [SQLite3](https://www.sqlite.org/index.html) - Local database used to store tasks

## Usage

Method GET on /todolist returns a HTML page, where all tasks are listed

Method POST on /todolist with JSON in format:
```
{ 
	"title" = "given title", 
	"done" = false/true
}
```
where "done" is optional adds a task to the database with current date and ip of the sender

Method GET on /todolist/<task_number> returns a JSON response in given format:
```
{
	"title" = "title",
	"done" = "true/false",
	"author_ip" = "author_ip",
	"created_date" = "created_date"
}
```
or code 404 if task is not found

Method PATCH on /todolist/<task_number> with JSON in format: 
```
{ 
	"title" = "given title", 
	"done" = false/true
}
```
where both keys are optional, updates task with given task_number and returns code 204 if completed successfully or 404 if task is not found.
