# QA Dashboard

Simple server to host ELK visualizations + Allure Reports

Hosts Allure Reports for multiple projects on the same server.

# Dependencies

* nodejs
* npm

# How to use

install dependencies:

```bash
npm install
```

configure routes for server: (see `Config` section)

start web server
```bash
npm start
```

access via: `yourIPorDomainName:3000`


## Config

1) add routes (links) to routes array in `config/default.json`:

```json
{
  "routes": ["project1", "project2", "project3"]

}
```

2) create folder inside `uploads` folder with same name as route:

* `uploads/project1`
* `uploads/project2`
* `uploads/project3`

3) upload all data from generated `allure-report` folder to that project's folder (possible via `scp` or similar).

**note: `uploads/project1/` should contain `index.html` and all files from `allure-report`**

**Server restarted after uploading and you can access to report via direct link:**  `localhost:3000/project1` or `localhost:3000/project2` or `yourIPorDomainName:3000/project1` and etc

**note: webserver port is 3000 by default, and can be configured in `config/default.json`:**
```json
{
  "port": 3000
}
```
