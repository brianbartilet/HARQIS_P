const path = require("path");
const config = require("config");
let result;


module ApplicationCard{
  export const application_card = function() {
  config.get('routes').map((link) => {
    let link_id = link.replace(/\s/g, "");

    let environment_card = config.get('environments').map((env) => {
      const fs = require('fs');
      try {
        if (fs.existsSync('uploads/' + link + '/' + env)) {
        } else {
          console.log('uploads/' + link + '/' + env + " not found.");
          return ``
        }

      } catch (err) {
        console.log('uploads/' + link + '/' + env + " not found.");
        return ``
      }

      var bgroup_chart = config.get('bgroups').map((bgroup) => {
        const fs = require('fs');

        var data;

        try {
          data = fs.readFileSync('uploads/' + link + '/' + env + '/' + bgroup + '/widgets/summary.json', 'utf8');
          result = JSON.parse(data);
          console.log(result);

        } catch (err) {
          result = JSON.parse('{}');

        }
        let lastRunDate = "";
        var passed = 0;
        var failed = 0;
        var broken = 0;
        var skipped = 0;
        var unknown = 0;
        var no_data = 1;
        var total = 0;

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
        `

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
                  
                  <div id="collapse${link_id}" class="collapse show" aria-labelledby="headingCard${link_id}" data-parent="#accordion">
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
};


}
