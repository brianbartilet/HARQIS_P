import * as path from 'path';
import * as express from 'express';
import * as morgan from 'morgan';
import * as config from 'config';

let app;
let result;

async function bootstrap() {
  app = express();
  app.use(morgan('dev'));

  // Point static path to dist
  app.use(express.static(path.join(__dirname, '..', 'uploads')));
  app.use(express.static(path.join(__dirname, '..', 'vendor')));
  app.use(express.static(path.join(__dirname, '..', 'public')));
  app.use(express.static(path.join(__dirname, '..', 'dist')));

  const application_card = config.get('routes').map((link) => {
    const link_id = link.replace(/\s/g, '');

    const environment_card = config.get('environments').map((env) => {
      const fs = require('fs');
      try {
        if (fs.existsSync('uploads/' + link + '/' + env)) {
        } else {
          // console.log('uploads/' + link + '/' + env + " not found.");
          return ``;
        }

      } catch (err) {
        // console.log('uploads/' + link + '/' + env + " not found.");
        return ``;
      }

      const bgroup_chart = config.get('bgroups').map((bgroup) => {
        // tslint:disable-next-line:no-shadowed-variable
        const fs = require('fs');

        // @ts-ignore
        let data;

        try {
          data = fs.readFileSync('uploads/' + link + '/' + env + '/' + bgroup + '/widgets/summary.json', 'utf8');
          result = JSON.parse(data);
          // console.log(result);

        } catch (err) {
          result = JSON.parse('{}');

        }
        let lastRunDate = '';
        let passed = 0;
        let failed = 0;
        let broken = 0;
        let skipped = 0;
        let unknown = 0;
        let no_data = 1;
        let total = 0;

        if (Object.keys(result).length > 0) {

          lastRunDate = new Date(result['time']['stop']).toUTCString();
          var dropSecs = lastRunDate.substring(0, lastRunDate.lastIndexOf(":"));

          passed = result['statistic']['passed'];
          failed = result['statistic']['failed'];
          broken = result['statistic']['broken'];
          skipped = result['statistic']['skipped'];
          unknown = result['statistic']['unknown'];
          total = passed + failed + broken;
          no_data = 0;

          return `
                    <div id="chartdiv${link}${env}${bgroup}" style="width: 160px; height: 200px;">
                    </div>
                    <script>
                    // Create chart instance
                    var chart = am4core.create("chartdiv${link}${env}${bgroup}", am4charts.PieChart);
                    chart.innerRadius = am4core.percent(50);
                    var title = chart.titles.create();
                    title.text = "${bgroup}";
                    title.fontWeight = "bold";
                    title.fontSize = 12;
                    title.marginBottom = 0;
                    // title.url = "${link}/${env}/${bgroup}";
                    title.fill = am4core.color("#E8E8E8");
                    title.fontFamily = "Consolas";

                    // Create pie series
                    var series = chart.series.push(new am4charts.PieSeries());
                    series.dataFields.value = "COUNT";
                    series.dataFields.category = "RESULT";
                    series.ticks.template.disabled = true;
                    series.labels.template.disabled = true;
                    series.slices.template.propertyFields.fill = "color";
                    series.slices.template.stroke = am4core.color("#FFFFFF");
                    series.slices.template.strokeWidth = 1;
                    series.slices.template.strokeOpacity = 1;
                    series.slices.template.propertyFields.url = "url";
                    series.slices.template.urlTarget = "_blank";
                    var label = series.createChild(am4core.Label);
                    label.text = "${total}";
                    label.horizontalCenter = "middle";
                    label.verticalCenter = "middle";\
                    if (${total} === 0){
                        label.tooltipText = "Waiting for results...";}
                    else{
                        label.tooltipText = "Total Tests: ${total}\\n\\nLast Update:\\n${dropSecs} GMT";
                    }
                    label.tooltipPosition = "pointer";
                    label.fontSize = 50;
                    label.fill = am4core.color("#E8E8E8");
                    label.fontFamily = "Calibri";
                    chart.data = [{
                      "RESULT": "Passed",
                      "COUNT": ${passed},
                      "color": am4core.color("#97cc64"),
                      "url": "${link}/${env}/${bgroup}",
                    }, {
                      "RESULT": "Failed",
                      "COUNT": ${failed},
                      "color": am4core.color("#fd5a3e"),
                      "url": "${link}/${env}/${bgroup}",
                    }, {
                      "RESULT": "Broken",
                      "COUNT": ${broken},
                      "color": am4core.color("#ffd050"),
                      "url": "${link}/${env}/${bgroup}",
                    }, {
                      "RESULT": "Unknown",
                      "COUNT": ${unknown},
                      "color": am4core.color("#d35ebe"),
                      "url": "${link}/${env}/${bgroup}",
                    }, {
                      "RESULT": "No Data",
                      "COUNT": ${no_data},
                      "color": am4core.color("#aaa"),
                      "url": "${link}/${env}/${bgroup}",
                    }];
                    </script>
                    `;
        }
      }).join('');

      return `
            <div class="card text-white bg-primary mb-1" id="appdivCard${link_id}${env}">
              <div class="card-header text-left" id="headingCard${link_id}${env}">
                <h5 class="mb-0">
                    <button class="btn btn-link text-white bg-primary mb-1" data-toggle="collapse" data-target="#collapse${link_id}${env}" aria-expanded="false" aria-controls="collapse${link_id}${env}">
                    ${env}
                    </button>
                </h5>
              </div>
              <div id="collapse${link_id}${env}" class="collapse hidden" aria-labelledby="headingCard${link_id}${env}" data-parent="#accordion">
                <div class="card-body text-center">
                  <div class="row">
                      ${bgroup_chart}
                  </div>
                </div>
              </div>
           </div>
        `;
    }).join('');

    return `
              <div class="col-sm-3 col-md-4" style="padding-top: 10px; padding-left: 30px; padding-right: 30px; padding-bottom: 10px">
                <div class="card text-white bg-secondary mb-3" id="appdivCard${link_id}">
                  <div class="card-header" id="headingCard${link_id}">
                    <h5 class="mb-0">
                        <button class="btn btn-link text-white bg-secondary mb-3" data-toggle="collapse" data-target="#collapse${link_id}" aria-expanded="false" aria-controls="collapse${link_id}">
                        ${link}
                        </button>
                    </h5>
                  </div>
                  <div id="collapse${link_id}" class="collapse hidden" aria-labelledby="headingCard${link_id}" data-parent="#accordion">
                    <div class="card-body text-center">
                      <div class="container">
                        <div class="accordion">
                            ${environment_card}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>`;

  }).join('');

  // main route
  app.get('/', (req, res) => {
    // res.send(path.resolve(`
    res.send(`
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <base href="/">

        <title>HARQIS Reports</title>
        <link href="https://bootswatch.com/4/superhero/bootstrap.min.css" rel="stylesheet">
        <link href="https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/superhero/bootstrap.min.css" rel="stylesheet" integrity="sha384-FnujoHKLiA0lyWE/5kNhcd8lfMILbUAZFAT89u11OhZI7Gt135tk3bGYVBC2xmJ5" crossorigin="anonymous">

        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js" integrity="sha384-b/U6ypiBEHpOf/4+1nzFpr53nxSS+GLCkfwBdFNTxtclqqenISfwAzpKaMNFNmj4" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js" integrity="sha384-6khuMg9gaYr5AxOqhkVIODVIvm9ynTT5J4V1cfthmT+emCG6yVmEZsRHdxlotUnm" crossorigin="anonymous"></script>

        <script src="https://www.amcharts.com/lib/4/core.js"></script>
        <script src="https://www.amcharts.com/lib/4/charts.js"></script>
      </head>

      <body class="bg-light">
        <nav class="navbar navbar-expand-lg navbar-dark bg-light" id="navBar">
          <a class="navbar-brand" href="#">HARQIS HOME</a>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarColor01" aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarColor01">
              <ul class="nav navbar-nav mr-auto">
                <!--<li id="li_home" class="nav-item">
                  <a class="nav-link" href="#"><span class="sr-only">HOME</span></a>
                </li>-->
                <!--
                <li id="li_trading" class="nav-item">
                  <a class="nav-link" href="#trading">PSEI Screener</a>
                </li>
                <li id="li_psei_live" class="nav-item">
                  <a class="nav-link" href="#psei_live">PSEI Trades</a>
                </li>
                <li id="li_trading" class="nav-item">
                  <a class="nav-link" href="#forex">FOREX</a>
                </li>
                -->
                <!--
                <li id="li_operational" class="nav-item">
                  <a class="nav-link" href="#operational">Operational</a>
                </li>
                <li id="li_project" class="nav-item">
                  <a class="nav-link" href="#project">Project</a>
                </li>
                -->
                <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">PSEI</a>
                <div class="dropdown-menu">
                  <a class="dropdown-item" href="#trading">Screener</a>
                  <a class="dropdown-item" href="#psei_live">Trading</a>
                  <!--<div class="dropdown-divider"></div>-->
                </div>
                </li>
                <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">WORKFLOWS</a>
                <div class="dropdown-menu">
                  <a class="dropdown-item" href="#harqis_metrics">Automated Jobs Metrics</a>
                  <a class="dropdown-item" href="#habits">Daily Tasks Metrics</a>

                </div>
                </li>
              </ul>
              <p class="text-muted"><small><span id="time" class="pull-left"></span></small></p>
          </div>
        </nav>
        <div class="page" id="home">
          <div class="jumbotron">
            <!--<h1 class="display-3">Man is something that shall be overcome.</h1>-->
            <h1 class="display-3">HARQIS</h1>
            <!--<p class="lead">Select a dashboard to view</p>-->
            <p class="lead">hopefully another rather quite intelligent system</p>
            <hr class="my-4">
            <p></p>

            <div class="row">
              <div class="col-sm-4">
                <div class="ard card border-primary">
                  <div class="card-body">
                    <h4 class="card-title">PSEI</h4>
                    <p class="card-text">PSEI Metrics, Analysis and Live Trading</p>
                    <a href="#trading" class="btn btn-outline-warning">View Screener</a>
                    <a href="#psei_live" class="btn btn-outline-warning">View Trades</a>
                  </div>
                </div>
              </div>
              <div class="col-sm-4">
                <div class="ard card border-primary">
                  <div class="card-body">
                    <h4 class="card-title">WORKFLOWS</h4>
                    <p class="card-text">Reliability Metrics</p>
                    <a href="#harqis_metrics" class="btn btn-outline-warning">View Jobs</a>
                  </div>
                </div>
              </div>
              <div class="col-sm-4">
                <div class="ard card border-primary">
                  <div class="card-body">
                    <h4 class="card-title">FOREX</h4>
                    <p class="card-text">Forex Trading Analysis</p>
                    <a href="#trading" class="btn btn-outline-warning">View Dashboard</a>
                  </div>
                </div>
              </div>

            </div>
          </div>

        </div>

        <div class="page" id="trading">
          <div class="embed-responsive embed-responsive-21by9">
            <div class="row" style="padding: 0px 10px 0px 10px;">
                <iframe src="https://7854e3b6326545c983580dd605cf191e.eastus2.azure.elastic-cloud.com:9243/app/dashboards#/view/00b164f0-5a3e-11eb-b6aa-c98103f025ac?embed=true&_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow-90d%2Cto%3Anow))&hide-filter-bar=true" height="1000" width="100%"></iframe>
            </div>
          </div>
        </div>
        <div class="page" id="psei_live">
          <div class="embed-responsive embed-responsive-21by9">
            <div class="row" style="padding: 0px 10px 0px 10px;">
                <iframe src="https://7854e3b6326545c983580dd605cf191e.eastus2.azure.elastic-cloud.com:9243/app/dashboards#/view/a97d72c0-6a9e-11eb-b6aa-c98103f025ac?embed=true&_g=(filters%3A!()%2Cquery%3A(language%3Akuery%2Cquery%3A'')%2CrefreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow-1y%2Cto%3Anow))&hide-filter-bar=true" height="1000" width="100%"></iframe>
            </div>
          </div>
        </div>
        <div class="page" id="harqis_metrics">
          <div class="embed-responsive embed-responsive-21by9">
            <div class="row" style="padding: 0px 10px 0px 10px;">
              <iframe src="https://7854e3b6326545c983580dd605cf191e.eastus2.azure.elastic-cloud.com:9243/app/dashboards#/view/99df0fe0-a8e2-11eb-b6aa-c98103f025ac?embed=true&_g=(filters:!(),refreshInterval:(pause:!f,value:10000),time:(from:now-90d,to:now))&_a=(description:'',filters:!(),fullScreenMode:!f,options:(hidePanelTitles:!f,useMargins:!t),query:(language:kuery,query:''),timeRestore:!f,title:'HARQIS%20Metrics',viewMode:view)&hide-filter-bar=true" height="1000" width="100%"></iframe>
            </div>
          </div>
        </div>
        <!--
        <div class="page" id="peon">
          <div class="embed-responsive embed-responsive-21by9">
            <div class="row" style="padding: 0px 10px 0px 10px;">
              <iframe class="embed-responsive-item" src="http://10.71.48.57:5601/app/kibana#/dashboard/568cb4e0-1dff-11eb-b76a-57e9fb8f7fd5?embed=true&_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!f%2Cvalue%3A900000)%2Ctime%3A(from%3Anow%2Fw%2Cto%3Anow%2Fw))" height=100% width=100%></iframe>
            </div>
          </div>
        </div>
        -->
        <div class="page" id="habits">
          <div class="embed-responsive embed-responsive-21by9">
            <div class="row" style="padding: 0px 10px 0px 10px;">
              <iframe src="https://7854e3b6326545c983580dd605cf191e.eastus2.azure.elastic-cloud.com:9243/app/dashboards#/view/13194100-35ce-11ec-8514-09a50147d145?embed=true&_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow-1y%2Cto%3Anow))&hide-filter-bar=true" height="1000" width="100%"></iframe>
            </div>
          </div>
        </div>
        <div class="page" id="project">
          <div class="row" style="padding: 0px 10px 0px 10px;">
            <iframe src="http://10.71.48.57:5601/app/kibana#/dashboard/5e9cc6f0-c816-11ea-8f9c-2163bb31fc0d?embed=true&_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!f%2Cvalue%3A900000)%2Ctime%3A(from%3Anow%2Fd%2Cto%3Anow%2Fd))" height="380" width=100%></iframe>
          </div>
          <div class="accordion">
            <div class="row" id="application_card">
                ${application_card}
            </div>

          </div>

        </div>
        <script src="static/js/main.js"></script>
        <script>
          document.addEventListener("DOMContentLoaded", onDOMLoaded);
        </script>

      </body>

</html>
    `);
  });

  // set dynamic routes for allure reports
  await
  config.get('routes').forEach(project => {
    config.get('environments').forEach(env => {
      // console.log(`project: ${project} - ${env} loaded`);
      app.use(`/${project}/${env}`, (req, res) => {
            res.sendFile(path.resolve(path.join(__dirname, '../uploads', `${project}/`, `${env}/index.html`)));
      });
    });
  });

  await app.listen(config.get('port'));
}

bootstrap();